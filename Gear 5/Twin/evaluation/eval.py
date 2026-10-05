import sys
import math
import time
from pydantic import BaseModel, Field
from litellm import completion
from dotenv import load_dotenv
from evaluation.test import TestQuestion, load_tests
from pro_implementation.answer import answer_question, fetch_context


load_dotenv(override=True)

# The judge should be at least as strong as the model that writes the answers (gpt-5.4-mini in answer.py).
# If you have access to a larger model, use it here for stricter, less noisy scoring.
JUDGE_MODEL = "gpt-5.4-mini"

# The twin retrieves 5 chunks (see answer.py), so that is all there is to score.
RETRIEVAL_K = 5


class RetrievalEval(BaseModel):
    """Evaluation metrics for retrieval performance."""

    mrr: float = Field(description="Mean Reciprocal Rank - average across all keywords")
    ndcg: float = Field(description="Normalized Discounted Cumulative Gain (binary relevance)")
    keywords_found: int = Field(description="Number of keywords found in top-k results")
    total_keywords: int = Field(description="Total number of keywords to find")
    keyword_coverage: float = Field(description="Percentage of keywords found")


class AnswerEval(BaseModel):
    """LLM-as-a-judge evaluation of answer quality."""

    feedback: str = Field(
        description="Concise feedback on the answer quality, comparing it to the reference answer"
    )
    accuracy: float = Field(
        description="How factually correct is the answer compared to the reference answer? 1 (wrong. any wrong or invented fact must score 1) to 5 (ideal - perfectly accurate). An acceptable answer would score 3."
    )
    completeness: float = Field(
        description="How complete is the answer in addressing all aspects of the question? 1 (very poor - missing key information) to 5 (ideal - all the information from the reference answer is provided completely). Only answer 5 if ALL information from the reference answer is included."
    )
    relevance: float = Field(
        description="How relevant is the answer to the specific question asked? 1 (very poor - off-topic) to 5 (ideal - directly addresses the question and stays on topic; brief markdown styling or a one-line pointer to related work is fine)."
    )


def calculate_mrr(keyword: str, retrieved_docs: list) -> float:
    """Calculate reciprocal rank for a single keyword (case-insensitive)."""
    keyword_lower = keyword.lower()
    for rank, doc in enumerate(retrieved_docs, start=1):
        if keyword_lower in doc.page_content.lower():
            return 1.0 / rank
    return 0.0


def calculate_dcg(relevances: list[int], k: int) -> float:
    """Calculate Discounted Cumulative Gain."""
    dcg = 0.0
    for i in range(min(k, len(relevances))):
        dcg += relevances[i] / math.log2(i + 2)  # i+2 because rank starts at 1
    return dcg


def calculate_ndcg(keyword: str, retrieved_docs: list, k: int = RETRIEVAL_K) -> float:
    """Calculate nDCG for a single keyword (binary relevance, case-insensitive)."""
    keyword_lower = keyword.lower()

    # Binary relevance: 1 if keyword found, 0 otherwise
    relevances = [
        1 if keyword_lower in doc.page_content.lower() else 0 for doc in retrieved_docs[:k]
    ]

    # DCG
    dcg = calculate_dcg(relevances, k)

    # Ideal DCG (best case: relevant chunks ranked first)
    ideal_relevances = sorted(relevances, reverse=True)
    idcg = calculate_dcg(ideal_relevances, k)

    return dcg / idcg if idcg > 0 else 0.0


def evaluate_retrieval(test: TestQuestion, k: int = RETRIEVAL_K) -> RetrievalEval:
    """
    Evaluate retrieval performance for a test question.

    Runs the same path as production (query rewrite + MMR retrieval), then scores the
    chunks it returns. Note: after MMR the order is selection order, not pure similarity
    rank, so read MRR / nDCG as rough signals and keyword coverage as the main number.

    Args:
        test: TestQuestion object containing question, keywords and optional history
        k: Number of top chunks to score (the twin retrieves 5)

    Returns:
        RetrievalEval object with MRR, nDCG, and keyword coverage metrics
    """
    retrieved_docs = fetch_context(test.question, test.history)

    # Calculate MRR (average across all keywords)
    mrr_scores = [calculate_mrr(keyword, retrieved_docs) for keyword in test.keywords]
    avg_mrr = sum(mrr_scores) / len(mrr_scores) if mrr_scores else 0.0

    # Calculate nDCG (average across all keywords)
    ndcg_scores = [calculate_ndcg(keyword, retrieved_docs, k) for keyword in test.keywords]
    avg_ndcg = sum(ndcg_scores) / len(ndcg_scores) if ndcg_scores else 0.0

    # Calculate keyword coverage
    keywords_found = sum(1 for score in mrr_scores if score > 0)
    total_keywords = len(test.keywords)
    keyword_coverage = (keywords_found / total_keywords * 100) if total_keywords > 0 else 0.0

    return RetrievalEval(
        mrr=avg_mrr,
        ndcg=avg_ndcg,
        keywords_found=keywords_found,
        total_keywords=total_keywords,
        keyword_coverage=keyword_coverage,
    )


def evaluate_answer(test: TestQuestion) -> tuple[AnswerEval, str, list]:
    """
    Evaluate answer quality using an LLM judge.

    Args:
        test: TestQuestion object containing question, reference answer and optional history

    Returns:
        Tuple of (AnswerEval object, generated_answer string, retrieved_docs list)
    """
    t0 = time.perf_counter()
    # notify=False: tools are stubbed, so no real ntfy alerts are sent during evaluation
    generated_answer, retrieved_docs = answer_question(test.question, test.history, notify=False)
    t1 = time.perf_counter()
    print(f"[TIMING] answer_question: {t1 - t0:.2f}s")

    # LLM judge prompt
    judge_messages = [
        {
            "role": "system",
            "content": (
                "You are an expert evaluator assessing answers given by a digital twin of a person, "
                "speaking in the first person about their career, projects, skills and background. "
                "Evaluate the generated answer by comparing it to the reference answer. "
                "Only give 5/5 scores for perfect answers. Do not penalize friendly tone or markdown styling."
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

Please evaluate the generated answer on three dimensions:
1. Accuracy: How factually correct is it compared to the reference answer? Only give 5/5 scores for perfect answers.
2. Completeness: How thoroughly does it address all aspects of the question, covering all the information from the reference answer?
3. Relevance: How well does it directly answer the specific question asked? Brief styling or a one-line pointer to related work is fine; unrelated content is not.

Special case: if the reference answer says the information is not available, an answer that clearly says it doesn't know, without inventing facts, scores 5 on all three dimensions. Any invented fact scores 1 for accuracy.

Provide detailed feedback and scores from 1 (very poor) to 5 (ideal) for each dimension. If the answer is wrong, then the accuracy score must be 1.""",
        },
    ]

    t2 = time.perf_counter()
    # Call LLM judge with structured outputs
    judge_response = completion(model=JUDGE_MODEL, messages=judge_messages, response_format=AnswerEval)
    t3 = time.perf_counter()
    print(f"[TIMING] judge completion: {t3 - t2:.2f}s")

    answer_eval = AnswerEval.model_validate_json(judge_response.choices[0].message.content)
    t4 = time.perf_counter()
    print(f"[TIMING] parse + total: {t4 - t3:.2f}s parse, {t4 - t0:.2f}s total")

    return answer_eval, generated_answer, retrieved_docs


def evaluate_all_retrieval():
    """Evaluate retrieval for all tests that have keywords (unanswerable / off-topic ones are skipped)."""
    tests = [t for t in load_tests() if t.keywords]
    total_tests = len(tests)
    for index, test in enumerate(tests):
        result = evaluate_retrieval(test)
        progress = (index + 1) / total_tests
        yield test, result, progress


def evaluate_all_answers():
    """Evaluate answers for all tests, one after another."""
    tests = load_tests()
    total_tests = len(tests)
    for index, test in enumerate(tests):
        result = evaluate_answer(test)[0]
        progress = (index + 1) / total_tests
        yield test, result, progress


def run_cli_evaluation(test_number: int):
    """Run evaluation for a specific test (CLI helper)."""
    tests = load_tests()

    if test_number < 0 or test_number >= len(tests):
        print(f"Error: test_row_number must be between 0 and {len(tests) - 1}")
        sys.exit(1)

    # Get the test
    test = tests[test_number]

    # Print test info
    print(f"\n{'=' * 80}")
    print(f"Test #{test_number}")
    print(f"{'=' * 80}")
    print(f"Question: {test.question}")
    if test.history:
        print(f"History: {test.history}")
    print(f"Keywords: {test.keywords}")
    print(f"Category: {test.category}")
    print(f"Reference Answer: {test.reference_answer}")

    # Retrieval Evaluation
    print(f"\n{'=' * 80}")
    print("Retrieval Evaluation")
    print(f"{'=' * 80}")

    if test.keywords:
        retrieval_result = evaluate_retrieval(test)
        print(f"MRR: {retrieval_result.mrr:.4f}")
        print(f"nDCG: {retrieval_result.ndcg:.4f}")
        print(f"Keywords Found: {retrieval_result.keywords_found}/{retrieval_result.total_keywords}")
        print(f"Keyword Coverage: {retrieval_result.keyword_coverage:.1f}%")
    else:
        print("No keywords for this test (unanswerable / off-topic), skipping retrieval metrics.")

    # Answer Evaluation
    print(f"\n{'=' * 80}")
    print("Answer Evaluation")
    print(f"{'=' * 80}")

    answer_result, generated_answer, retrieved_docs = evaluate_answer(test)

    print(f"\nGenerated Answer:\n{generated_answer}")
    print(f"\nFeedback:\n{answer_result.feedback}")
    print("\nScores:")
    print(f"  Accuracy: {answer_result.accuracy:.2f}/5")
    print(f"  Completeness: {answer_result.completeness:.2f}/5")
    print(f"  Relevance: {answer_result.relevance:.2f}/5")
    print(f"\n{'=' * 80}\n")


def main():
    """CLI to evaluate a specific test by row number (0-based)."""
    if len(sys.argv) != 2:
        print("Usage (from the project root): python -m evaluation.eval <test_row_number>")
        sys.exit(1)

    try:
        test_number = int(sys.argv[1])
    except ValueError:
        print("Error: test_row_number must be an integer")
        sys.exit(1)

    run_cli_evaluation(test_number)


if __name__ == "__main__":
    main()