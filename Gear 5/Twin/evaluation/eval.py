"""
Evaluation for the digital twin RAG pipeline.

Retrieval  : LLM-graded chunk relevance (0/1/2) -> MRR, nDCG, Precision@k, average first rank.
             Gold-section recall + gold MRR (objective cross-check, from `gold_sections` in tests.jsonl).
             Keyword coverage is kept as a DIAGNOSTIC only.
Answers    : LLM judge -> accuracy, completeness, relevance, plus a separate faithfulness check.
Run        : parallel, retried, error-isolated, persisted. One retrieval call per test (reused for the answer).

CLI (from the project root):
    python -m evaluation.eval <test_row_number>   # one test, verbose
    python -m evaluation.eval retrieval           # retrieval only (all tests with keywords)
    python -m evaluation.eval all                 # retrieval + answers + faithfulness, saved to evaluation/results/

Dashboard-compatible API (same shapes as the previous twin evaluator):
    evaluate_retrieval(test) -> RetrievalEval
    evaluate_answer(test)    -> (AnswerEval, generated_answer, retrieved_docs)
    evaluate_all_retrieval() / evaluate_all_answers() -> yield (test, result, progress)
"""

import csv
import hashlib
import json
import math
import os
import re
import statistics
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import litellm
from dotenv import load_dotenv
from litellm import completion
from pydantic import BaseModel, Field

from evaluation.test import TestQuestion, load_tests
import answer as twin_module
from answer import answer_question, fetch_context

load_dotenv(override=True)
litellm.drop_params = True  # some models reject temperature=0 etc.; drop unsupported params instead of failing

# ----------------------------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------------------------
# The judge should be at least as strong as the model that writes the answers. Override with JUDGE_MODEL.
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "gpt-5.4-mini")
JUDGE_TEMPERATURE = 0.0
RETRIEVAL_K = 5  # the twin retrieves 5 chunks (see answer.py)
MAX_WORKERS = int(os.getenv("EVAL_MAX_WORKERS", "4"))
JUDGE_RETRIES = 3

RESULTS_DIR = Path(__file__).parent / "results"
CACHE_FILE = RESULTS_DIR / "relevance_cache.json"
HISTORY_FILE = RESULTS_DIR / "history.jsonl"


# ----------------------------------------------------------------------------------------------
# Models
# ----------------------------------------------------------------------------------------------
class ChunkGrade(BaseModel):
    chunk: int = Field(description="1-based number of the chunk being graded")
    relevance: int = Field(description="0 = irrelevant, 1 = somewhat relevant, 2 = highly relevant")


class ChunkGrades(BaseModel):
    grades: list[ChunkGrade] = Field(description="One grade per chunk, in order")


class RetrievalEval(BaseModel):
    """Retrieval metrics for one test."""

    # LLM-graded (primary)
    mrr: float = Field(description="Reciprocal rank of the first chunk graded >= 1")
    ndcg: float = Field(description="nDCG with graded gains (0/1/2)")
    precision_at_k: float = Field(description="Fraction of retrieved chunks graded >= 1")
    avg_first_rank: Optional[float] = Field(default=None, description="Rank of first relevant chunk (None if none)")
    relevance_grades: list[int] = Field(default_factory=list, description="LLM grade per retrieved chunk, in order")
    grading: str = Field(default="llm", description="'llm' or 'keyword' (fallback when LLM grading is off)")
    # Gold labels (objective cross-check; None when the test has no gold_sections)
    recall_at_k: Optional[float] = Field(default=None, description="Fraction of gold information needs covered")
    gold_mrr: Optional[float] = Field(default=None, description="Reciprocal rank of first gold chunk")
    # Keywords (diagnostic only)
    keywords_found: int
    total_keywords: int
    keyword_coverage: float = Field(description="Percentage of keywords found in the retrieved chunks")
    retrieved_sections: list[str] = Field(default_factory=list, description="Headers of the retrieved chunks")


class AnswerJudgement(BaseModel):
    """What the judge returns for answer quality."""

    feedback: str = Field(description="Concise feedback comparing the answer to the reference answer")
    accuracy: float = Field(
        description="1-5. 5: every fact correct. 4: tiny inaccuracy on a minor detail. 3: mostly correct but one notable "
        "error or vague claim. 2: significant error. 1: the core fact is wrong or invented. Missing information does NOT "
        "lower accuracy (that is completeness)."
    )
    completeness: float = Field(
        description="1-5. How completely does the answer give all the IMPORTANT information needed to answer the question "
        "(not every incidental detail of the reference)? 5 = everything important is present."
    )
    relevance: float = Field(
        description="1-5. How directly the answer addresses the question asked. Brief markdown styling or a one-line "
        "pointer to related work is fine."
    )


class FaithfulnessJudgement(BaseModel):
    feedback: str = Field(description="Which claims (if any) are not supported by the context")
    faithfulness: float = Field(
        description="1-5. 5: every claim is supported by the provided context. 1: major claims are invented or contradict it."
    )


class AnswerEval(AnswerJudgement):
    """Answer quality including the separate faithfulness check."""

    faithfulness: float = 0.0
    faithfulness_feedback: str = ""


class FullResult(BaseModel):
    test: TestQuestion
    retrieval: RetrievalEval
    answer: AnswerEval
    generated_answer: str
    seconds: float


# ----------------------------------------------------------------------------------------------
# Matching helpers
# ----------------------------------------------------------------------------------------------
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def keyword_in_text(keyword: str, text: str) -> bool:
    """Case-insensitive, whole-token match that also works for '$50', '80%', 'answer_question()'."""
    return re.search(r"(?<!\w)" + re.escape(keyword.lower()) + r"(?!\w)", text.lower()) is not None


def chunk_header(doc) -> str:
    m = re.match(r"\s*##\s+([^\n]+)", doc.page_content)
    if m:
        return m.group(1).strip()
    return _norm(doc.page_content)[:50]


def chunk_matches_section(doc, section: str) -> bool:
    """`section` is 'file.md::Header'; chunks are '## Header' sections, and headers are unique in the KB."""
    header = section.split("::", 1)[-1]
    return ("## " + _norm(header)) in _norm(doc.page_content)


# ----------------------------------------------------------------------------------------------
# Judge plumbing: retries + structured output
# ----------------------------------------------------------------------------------------------
def call_judge(messages: list[dict], response_format):
    last_error = None
    for attempt in range(1, JUDGE_RETRIES + 1):
        try:
            response = completion(
                model=JUDGE_MODEL,
                messages=messages,
                response_format=response_format,
                temperature=JUDGE_TEMPERATURE,
            )
            return response_format.model_validate_json(response.choices[0].message.content)
        except Exception as e:  # network, rate limit, bad JSON...
            last_error = e
            time.sleep(1.5 * attempt)
    raise RuntimeError(f"Judge failed after {JUDGE_RETRIES} attempts: {last_error}")


_cache_lock = threading.Lock()
_cache: dict = {}
if CACHE_FILE.exists():
    try:
        _cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        _cache = {}


def _cache_get(key: str):
    with _cache_lock:
        return _cache.get(key)


def _cache_put(key: str, value) -> None:
    with _cache_lock:
        _cache[key] = value
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(json.dumps(_cache), encoding="utf-8")


# ----------------------------------------------------------------------------------------------
# Retrieval metrics
# ----------------------------------------------------------------------------------------------
def grade_chunks(test: TestQuestion, docs: list, k: int = RETRIEVAL_K) -> list[int]:
    """LLM relevance grade (0/1/2) for each of the top-k chunks, in one call. Cached for stable reruns."""
    top = docs[:k]
    if not top:
        return []
    chunks_text = "\n\n".join(f"[Chunk {i}]\n{d.page_content}" for i, d in enumerate(top, start=1))
    key = hashlib.sha1(
        "|".join([JUDGE_MODEL, test.question, test.reference_answer, chunks_text]).encode("utf-8")
    ).hexdigest()
    cached = _cache_get(key)
    if cached is not None:
        return cached

    messages = [
        {
            "role": "system",
            "content": (
                "You grade retrieval for a RAG system that powers a digital twin of a person. "
                "For each retrieved chunk, decide how useful it is for answering the question."
            ),
        },
        {
            "role": "user",
            "content": f"""Question:
{test.question}

Reference answer (what a good answer needs to say):
{test.reference_answer}

Retrieved chunks:
{chunks_text}

Grade EACH chunk:
2 = highly relevant: contains key information needed to produce the reference answer.
1 = somewhat relevant: related or partially helpful, but does not contain the key information.
0 = irrelevant.

Return one grade per chunk, numbered as above.""",
        },
    ]
    result = call_judge(messages, ChunkGrades)
    by_chunk = {g.chunk: g.relevance for g in result.grades}
    grades = [min(2, max(0, int(by_chunk.get(i, 0)))) for i in range(1, len(top) + 1)]
    _cache_put(key, grades)
    return grades


def _dcg(grades: list[int], k: int) -> float:
    return sum(g / math.log2(i + 2) for i, g in enumerate(grades[:k]))


def metrics_from_grades(grades: list[int], n_needs: int, k: int = RETRIEVAL_K) -> tuple[float, float, float, Optional[float]]:
    """MRR, nDCG, Precision@k, first relevant rank from graded relevance."""
    first_rank = next((r for r, g in enumerate(grades, start=1) if g >= 1), None)
    mrr = 1.0 / first_rank if first_rank else 0.0
    precision = sum(1 for g in grades if g >= 1) / len(grades) if grades else 0.0
    # Ideal list accounts for needs the retriever missed (not only re-sorting what it returned).
    extra = max(0, n_needs - sum(1 for g in grades if g == 2))
    ideal = sorted(grades + [2] * extra, reverse=True)[:k]
    idcg = _dcg(ideal, k)
    ndcg = _dcg(grades, k) / idcg if idcg > 0 else 0.0
    return mrr, min(ndcg, 1.0), precision, float(first_rank) if first_rank else None


def score_retrieval(test: TestQuestion, docs: list, k: int = RETRIEVAL_K, use_llm: bool = True) -> RetrievalEval:
    top = docs[:k]

    # Keywords: diagnostic only
    found = sum(1 for kw in test.keywords if any(keyword_in_text(kw, d.page_content) for d in top))
    total = len(test.keywords)
    coverage = found / total * 100 if total else 0.0

    # Gold labels: objective recall + MRR
    recall = gold_mrr = None
    if test.gold_sections:
        need_hit = [any(chunk_matches_section(d, s) for d in top for s in group) for group in test.gold_sections]
        recall = sum(need_hit) / len(need_hit)
        rank = next(
            (r for r, d in enumerate(top, start=1) if any(chunk_matches_section(d, s) for g in test.gold_sections for s in g)),
            None,
        )
        gold_mrr = 1.0 / rank if rank else 0.0

    # Primary metrics: LLM-graded relevance (falls back to keywords if LLM grading is off)
    if use_llm:
        grades, grading = grade_chunks(test, top, k), "llm"
    else:
        grades = [1 if any(keyword_in_text(kw, d.page_content) for kw in test.keywords) else 0 for d in top]
        grading = "keyword"
    n_needs = len(test.gold_sections) or 1
    mrr, ndcg, precision, first_rank = metrics_from_grades(grades, n_needs, k)

    return RetrievalEval(
        mrr=mrr,
        ndcg=ndcg,
        precision_at_k=precision,
        avg_first_rank=first_rank,
        relevance_grades=grades,
        grading=grading,
        recall_at_k=recall,
        gold_mrr=gold_mrr,
        keywords_found=found,
        total_keywords=total,
        keyword_coverage=coverage,
        retrieved_sections=[chunk_header(d) for d in top],
    )


def evaluate_retrieval(test: TestQuestion, k: int = RETRIEVAL_K, use_llm: bool = True) -> RetrievalEval:
    """Run the production retrieval path (query rewrite + MMR) and score the chunks it returns."""
    docs = fetch_context(test.question, test.history)
    return score_retrieval(test, docs, k, use_llm)


# ----------------------------------------------------------------------------------------------
# Answer metrics
# ----------------------------------------------------------------------------------------------
_warned_no_prompt = False


def _twin_prompt_text() -> str:
    """The twin's system prompt (resume + personal summary). Needed so faithfulness doesn't flag grounded claims."""
    global _warned_no_prompt
    for name in ("SYSTEM_PROMPT", "system_prompt", "PERSONA", "persona_prompt"):
        value = getattr(twin_module, name, None)
        if isinstance(value, str) and value.strip():
            return value
    for name in ("build_system_prompt", "get_system_prompt"):
        fn = getattr(twin_module, name, None)
        if callable(fn):
            try:
                value = fn()
                if isinstance(value, str) and value.strip():
                    return value
            except Exception:
                pass
    if not _warned_no_prompt:
        _warned_no_prompt = True
        print("[eval] WARNING: twin system prompt not found in answer.py (looked for SYSTEM_PROMPT / build_system_prompt). "
              "Faithfulness will only see retrieved chunks, so facts grounded in the prompt may be flagged.")
    return ""


def judge_answer(test: TestQuestion, generated_answer: str) -> AnswerJudgement:
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert evaluator assessing answers given by a digital twin of a person, speaking in the first "
                "person about their career, projects, skills and background. Compare the generated answer to the reference "
                "answer. Do not penalize friendly tone or markdown styling. Reserve 5/5 for answers with nothing to improve."
            ),
        },
        {
            "role": "user",
            "content": f"""Question:
{test.question}

Generated Answer:
{generated_answer}

Reference Answer:
{test.reference_answer}

Evaluate the generated answer on three separate dimensions:
1. Accuracy: are the facts correct compared to the reference? A wrong or invented core fact scores 1. A missing detail does NOT lower accuracy.
2. Completeness: does it give all the IMPORTANT information needed to answer the question? Do not require every incidental detail of the reference.
3. Relevance: does it directly answer the question asked? Brief styling or a one-line pointer to related work is fine; unrelated content is not.

Special case: if the reference answer says the information is not available, an answer that clearly says it doesn't know, without inventing facts, scores 5 on all three.

Give concise feedback and scores from 1 (very poor) to 5 (ideal) for each dimension.""",
        },
    ]
    return call_judge(messages, AnswerJudgement)


def judge_faithfulness(test: TestQuestion, generated_answer: str, docs: list) -> FaithfulnessJudgement:
    chunks_text = "\n\n".join(f"[Chunk {i}]\n{d.page_content}" for i, d in enumerate(docs, start=1)) or "(no chunks retrieved)"
    prompt_text = _twin_prompt_text()
    context = (f"TWIN SYSTEM PROMPT (persona and resume):\n{prompt_text}\n\n" if prompt_text else "") + f"RETRIEVED CHUNKS:\n{chunks_text}"
    messages = [
        {
            "role": "system",
            "content": (
                "You check whether an answer is faithful to the context the system had available. "
                "A claim is supported if the context states it or it follows directly from it."
            ),
        },
        {
            "role": "user",
            "content": f"""Context available to the twin:
{context}

Question:
{test.question}

Generated Answer:
{generated_answer}

Is every factual claim in the answer supported by the context above? Ignore tone and style. If the answer says it doesn't know / lacks the information, it is faithful.
Score 1-5: 5 = every claim supported; 3 = some unsupported detail; 1 = major claims invented or contradicting the context.""",
        },
    ]
    return call_judge(messages, FaithfulnessJudgement)


def evaluate_full(test: TestQuestion, k: int = RETRIEVAL_K, use_llm_relevance: bool = True) -> FullResult:
    """Everything for one test from a SINGLE retrieval call (the docs the answer actually used)."""
    t0 = time.perf_counter()
    # notify=False: tools are stubbed, so no real ntfy alerts are sent during evaluation
    generated_answer, docs = answer_question(test.question, test.history, notify=False)
    retrieval = score_retrieval(test, docs, k, use_llm_relevance) if test.keywords else _empty_retrieval(test, docs)
    judgement = judge_answer(test, generated_answer)
    faith = judge_faithfulness(test, generated_answer, docs)
    answer = AnswerEval(
        **judgement.model_dump(), faithfulness=faith.faithfulness, faithfulness_feedback=faith.feedback
    )
    return FullResult(test=test, retrieval=retrieval, answer=answer, generated_answer=generated_answer,
                      seconds=time.perf_counter() - t0)


def _empty_retrieval(test: TestQuestion, docs: list) -> RetrievalEval:
    return RetrievalEval(mrr=0.0, ndcg=0.0, precision_at_k=0.0, relevance_grades=[], grading="skipped",
                         keywords_found=0, total_keywords=0, keyword_coverage=0.0,
                         retrieved_sections=[chunk_header(d) for d in docs[:RETRIEVAL_K]])


def evaluate_answer(test: TestQuestion) -> tuple[AnswerEval, str, list]:
    """Dashboard-compatible: (AnswerEval, generated_answer, retrieved_docs)."""
    generated_answer, docs = answer_question(test.question, test.history, notify=False)
    judgement = judge_answer(test, generated_answer)
    faith = judge_faithfulness(test, generated_answer, docs)
    result = AnswerEval(**judgement.model_dump(), faithfulness=faith.faithfulness, faithfulness_feedback=faith.feedback)
    return result, generated_answer, docs


# ----------------------------------------------------------------------------------------------
# Parallel runner with error isolation
# ----------------------------------------------------------------------------------------------
LAST_RUN_FAILURES: list[str] = []  # "question -> error" for tests that failed in the last batch


def _run_parallel(tests: list[TestQuestion], fn: Callable[[TestQuestion], object]):
    """Yield (test, result, progress) as tests finish. One failing test never stops the run, and is recorded."""
    LAST_RUN_FAILURES.clear()
    total = len(tests)
    done = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(fn, t): t for t in tests}
        for future in as_completed(futures):
            test = futures[future]
            done += 1
            try:
                result = future.result()
            except Exception as e:
                LAST_RUN_FAILURES.append(f"{test.question} -> {e}")
                print(f"[eval] FAILED ({done}/{total}): {test.question!r}: {e}")
                continue
            yield test, result, done / total


def evaluate_all_retrieval():
    """Retrieval for all tests with keywords (unanswerable / off-topic ones are skipped). Yields (test, RetrievalEval, progress)."""
    tests = [t for t in load_tests() if t.keywords]
    yield from _run_parallel(tests, evaluate_retrieval)


def evaluate_all_answers():
    """Answers + faithfulness for all tests. Yields (test, AnswerEval, progress)."""
    yield from _run_parallel(load_tests(), lambda t: evaluate_answer(t)[0])


def evaluate_all_full():
    """Retrieval + answers + faithfulness from one retrieval call per test. Yields (test, FullResult, progress)."""
    yield from _run_parallel(load_tests(), evaluate_full)


# ----------------------------------------------------------------------------------------------
# Summaries, persistence
# ----------------------------------------------------------------------------------------------
RETRIEVAL_METRICS = ["mrr", "ndcg", "precision_at_k", "recall_at_k", "gold_mrr", "keyword_coverage"]
ANSWER_METRICS = ["accuracy", "completeness", "relevance", "faithfulness"]


def _mean(values) -> Optional[float]:
    values = [v for v in values if v is not None]
    return statistics.fmean(values) if values else None


def summarize(results: list[FullResult], failed: int = 0) -> dict:
    with_kw = [r for r in results if r.test.keywords]
    summary = {"tests": len(results), "failed": failed, "retrieval": {}, "answer": {}, "by_category": {}}
    for m in RETRIEVAL_METRICS:
        summary["retrieval"][m] = _mean(getattr(r.retrieval, m) for r in with_kw)
    summary["retrieval"]["avg_first_rank"] = _mean(r.retrieval.avg_first_rank for r in with_kw)
    for m in ANSWER_METRICS:
        summary["answer"][m] = _mean(getattr(r.answer, m) for r in results)
    for cat in sorted({r.test.category for r in results}):
        rs = [r for r in results if r.test.category == cat]
        summary["by_category"][cat] = {
            "n": len(rs),
            **{m: _mean(getattr(r.answer, m) for r in rs) for m in ANSWER_METRICS},
            "mrr": _mean(r.retrieval.mrr for r in rs if r.test.keywords),
            "recall_at_k": _mean(r.retrieval.recall_at_k for r in rs if r.test.keywords),
        }
    return summary


def save_run(results: list[FullResult], summary: dict) -> Path:
    """Write per-question CSV + append the summary (with config) to history.jsonl."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    csv_path = RESULTS_DIR / f"run-{run_id}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["category", "question", "mrr", "ndcg", "precision_at_k", "recall_at_k", "gold_mrr", "keyword_coverage",
                    "grades", "retrieved_sections", "accuracy", "completeness", "relevance", "faithfulness",
                    "generated_answer", "reference_answer", "feedback", "faithfulness_feedback"])
        for r in sorted(results, key=lambda r: r.answer.accuracy):  # worst first
            rt, an = r.retrieval, r.answer
            w.writerow([r.test.category, r.test.question, f"{rt.mrr:.3f}", f"{rt.ndcg:.3f}", f"{rt.precision_at_k:.3f}",
                        "" if rt.recall_at_k is None else f"{rt.recall_at_k:.3f}",
                        "" if rt.gold_mrr is None else f"{rt.gold_mrr:.3f}", f"{rt.keyword_coverage:.1f}",
                        rt.relevance_grades, " | ".join(rt.retrieved_sections),
                        an.accuracy, an.completeness, an.relevance, an.faithfulness,
                        r.generated_answer, r.test.reference_answer, an.feedback, an.faithfulness_feedback])
    config = {"judge_model": JUDGE_MODEL, "k": RETRIEVAL_K, "workers": MAX_WORKERS, "tests_file": "tests.jsonl"}
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"run_id": run_id, "config": config, "summary": summary}, ensure_ascii=False) + "\n")
    return csv_path


def _fmt(x: Optional[float], digits: int = 3) -> str:
    return "n/a" if x is None else f"{x:.{digits}f}"


def print_summary(summary: dict) -> None:
    print(f"\n{'=' * 70}\nTests: {summary['tests']}   Failed: {summary['failed']}")
    r, a = summary["retrieval"], summary["answer"]
    print("\nRetrieval (LLM-graded):  MRR %s | nDCG %s | P@k %s | first rank %s" % (
        _fmt(r["mrr"]), _fmt(r["ndcg"]), _fmt(r["precision_at_k"]), _fmt(r["avg_first_rank"], 2)))
    print("Retrieval (gold):        recall@k %s | gold MRR %s" % (_fmt(r["recall_at_k"]), _fmt(r["gold_mrr"])))
    print("Keyword coverage (diagnostic): %s%%" % _fmt(r["keyword_coverage"], 1))
    print("\nAnswers: accuracy %s | completeness %s | relevance %s | faithfulness %s" % (
        _fmt(a["accuracy"], 2), _fmt(a["completeness"], 2), _fmt(a["relevance"], 2), _fmt(a["faithfulness"], 2)))
    print("\nBy category (n, accuracy, completeness, faithfulness, MRR, gold recall):")
    for cat, c in summary["by_category"].items():
        print(f"  {cat:13s} n={c['n']:3d}  acc {_fmt(c['accuracy'],2)}  comp {_fmt(c['completeness'],2)}  "
              f"faith {_fmt(c['faithfulness'],2)}  mrr {_fmt(c['mrr'])}  recall {_fmt(c['recall_at_k'])}")
    print("=" * 70)


# ----------------------------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------------------------
def run_cli_evaluation(test_number: int):
    tests = load_tests()
    if test_number < 0 or test_number >= len(tests):
        print(f"Error: test_row_number must be between 0 and {len(tests) - 1}")
        sys.exit(1)
    test = tests[test_number]
    print(f"\n{'=' * 80}\nTest #{test_number}  [{test.category}]\n{'=' * 80}")
    print(f"Question: {test.question}\nKeywords: {test.keywords}\nGold: {test.gold_sections}\nReference: {test.reference_answer}")
    result = evaluate_full(test)
    rt, an = result.retrieval, result.answer
    print(f"\nRetrieved: {rt.retrieved_sections}\nGrades (0-2): {rt.relevance_grades}")
    print(f"MRR {rt.mrr:.3f} | nDCG {rt.ndcg:.3f} | P@k {rt.precision_at_k:.3f} | recall {_fmt(rt.recall_at_k)} | keywords {rt.keywords_found}/{rt.total_keywords}")
    print(f"\nGenerated Answer:\n{result.generated_answer}\n\nFeedback:\n{an.feedback}\n\nFaithfulness feedback:\n{an.faithfulness_feedback}")
    print(f"\nAccuracy {an.accuracy:.1f} | Completeness {an.completeness:.1f} | Relevance {an.relevance:.1f} | Faithfulness {an.faithfulness:.1f}\n")


def run_batch(retrieval_only: bool = False):
    if retrieval_only:
        rows = []
        for test, result, progress in evaluate_all_retrieval():
            rows.append(result)
            print(f"[{progress:4.0%}] mrr {result.mrr:.2f} recall {_fmt(result.recall_at_k, 2)}  {test.question}")
        print(f"\nRetrieval-only: {len(rows)} ok, {len(LAST_RUN_FAILURES)} failed")
        for m in ("mrr", "ndcg", "precision_at_k", "recall_at_k", "gold_mrr", "keyword_coverage"):
            print(f"  {m}: {_fmt(_mean(getattr(r, m) for r in rows))}")
        return
    results = []
    for test, result, progress in evaluate_all_full():
        results.append(result)
        print(f"[{progress:4.0%}] acc {result.answer.accuracy:.0f} comp {result.answer.completeness:.0f} "
              f"faith {result.answer.faithfulness:.0f}  {test.question}")
    summary = summarize(results, failed=len(LAST_RUN_FAILURES))
    print_summary(summary)
    print("Saved:", save_run(results, summary))
    for line in LAST_RUN_FAILURES:
        print("FAILED:", line)


def main():
    if len(sys.argv) != 2:
        print("Usage (from the project root): python -m evaluation.eval <test_row_number> | retrieval | all")
        sys.exit(1)
    arg = sys.argv[1].lower()
    if arg == "all":
        run_batch()
    elif arg == "retrieval":
        run_batch(retrieval_only=True)
    else:
        try:
            run_cli_evaluation(int(arg))
        except ValueError:
            print("Error: argument must be an integer, 'retrieval', or 'all'")
            sys.exit(1)


if __name__ == "__main__":
    main()
