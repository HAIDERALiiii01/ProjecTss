# Twin evaluator: changes vs the old evaluator

Bugs fixed
- `notify=False` restored in `answer_question` (no real ntfy alerts while evaluating); `history` restored in TestQuestion.
- Keyword matching: `\b` could never match `$50`, `80%`, `10%`, `answer_question()`; now uses `(?<!\w)...(?!\w)`.
- CLI crash (`load_tests("tests.jsonl")`): `load_tests` now takes an optional path.
- k = 5 (what the twin retrieves), not 10.
- `litellm.drop_params = True` so models that reject temperature=0 don't fail.
- Failed tests are counted and reported (`LAST_RUN_FAILURES`, "Failed: n"), not silently dropped.

Retrieval
- MRR / nDCG / Precision@k / first rank now come from LLM-graded chunk relevance (0/1/2, judged with the reference answer, cached).
- nDCG's ideal ranking accounts for needs the retriever missed, not only re-sorting what it returned.
- `recall_at_k` and `gold_mrr` use `gold_sections` in tests.jsonl (groups of alternative "file.md::Header" chunks).
- Keyword coverage kept as a diagnostic only.

Answers
- Accuracy no longer collapses to 1 for any missing detail (that is completeness).
- Completeness = all IMPORTANT information needed, not every reference detail.
- Relevance wording allows short pointers to related work.
- Faithfulness is a separate judge call; it sees the twin's system prompt (if found in answer.py) plus the chunks.

Kept: parallel runs (EVAL_MAX_WORKERS, default 4), retries, error isolation, persistence (results/run-*.csv worst-first,
results/history.jsonl with config), single retrieval call per test.

Dashboard API unchanged: evaluate_retrieval / evaluate_answer (3-tuple) / evaluate_all_retrieval / evaluate_all_answers.
AnswerEval gains `faithfulness`; RetrievalEval gains precision_at_k, recall_at_k, gold_mrr, avg_first_rank, relevance_grades.
