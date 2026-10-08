"""
Digital Twin Evaluation Dashboard (Gradio)
==========================================
- "Full Evaluation": retrieval + answer quality + faithfulness off a single retrieval call per test
  (see evaluation/eval.py). Saves JSON + CSV to evaluation/results/ and adds a row to the run history.
- "Retrieval Only": retrieval metrics only, no answers generated. Uses one cheap, cached LLM
  relevance call per test (untick the box for a keyword-only fallback with zero judge cost).
- "Run History": every saved Full Evaluation run, to spot regressions.

Run from the project root:  python evaluator.py
"""

from __future__ import annotations
from collections import defaultdict

import gradio as gr
import pandas as pd
from dotenv import load_dotenv

from evaluation.eval import (
    evaluate_all_full,
    evaluate_all_retrieval,
    load_run_history,
    save_full_run,
)

load_dotenv(override=True)

# ---------------------------------------------------------------------------
# Color-coding thresholds (single source of truth): (green >= first, amber >= second)
# Precision@5 is naturally low for a twin: most answers live in ONE chunk, so ~0.2-0.4 is healthy.
# ---------------------------------------------------------------------------
THRESHOLDS = {
    "mrr": (0.90, 0.75),
    "ndcg": (0.90, 0.75),
    "precision": (0.40, 0.25),
    "recall": (0.90, 0.75),
    "coverage": (90.0, 75.0),
    "accuracy": (4.5, 4.0),
    "completeness": (4.5, 4.0),
    "relevance": (4.5, 4.0),
    "faithfulness": (4.5, 4.0),
}


def get_color(value: float, metric_type: str) -> str:
    green, amber = THRESHOLDS.get(metric_type, (0.9, 0.75))
    if value >= green:
        return "green"
    if value >= amber:
        return "orange"
    return "red"


def format_metric_html(
    label: str,
    value: float,
    metric_type: str,
    is_percentage: bool = False,
    score_format: bool = False,
    stdev: float | None = None,
) -> str:
    color = get_color(value, metric_type)
    if is_percentage:
        value_str = f"{value:.1f}%"
    elif score_format:
        value_str = f"{value:.2f}/5"
    else:
        value_str = f"{value:.4f}"

    stdev_str = ""
    if std := stdev:
        stdev_str = f'<div style="font-size: 12px; color: #999; margin-top: 2px;">± {std:.3f}</div>'

    return f"""
    <div style="margin: 10px 0; padding: 15px; background-color: #f5f5f5;
                border-radius: 8px; border-left: 5px solid {color};">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">{label}</div>
        <div style="font-size: 26px; font-weight: bold; color: {color};">{value_str}</div>
        {stdev_str}
    </div>
    """


def completion_banner(count: int, failed: int = 0) -> str:
    failed_html = ""
    if failed:
        failed_html = (
            f' · <span style="color:#a94442;">{failed} test(s) failed and are NOT in the averages '
            f"(see the console)</span>"
        )
    return f"""
    <div style="margin-top: 20px; padding: 10px; background-color: #d4edda; border-radius: 5px;
                text-align: center; border: 1px solid #c3e6cb;">
        <span style="font-size: 14px; color: #155724; font-weight: bold;">
            ✓ Evaluation complete · {count} tests{failed_html}
        </span>
    </div>
    """


EMPTY_HTML = "<div style='color:red;padding:20px;'>No tests completed — check the console for errors.</div>"


# ---------------------------------------------------------------------------
# Retrieval-only tab
# ---------------------------------------------------------------------------
def run_retrieval_evaluation(use_llm: bool = True, progress=gr.Progress()):
    totals = defaultdict(float)
    category_mrr = defaultdict(list)
    count = 0

    for test, result, prog_value in evaluate_all_retrieval(use_llm=use_llm):
        count += 1
        totals["mrr"] += result.mrr
        totals["ndcg"] += result.ndcg
        totals["precision"] += result.precision_at_k
        totals["recall"] += result.recall_at_k
        totals["coverage"] += result.keyword_coverage
        category_mrr[test.category].append(result.mrr)
        progress(prog_value, desc=f"Evaluating retrieval · test {count}...")

    if count == 0:
        return EMPTY_HTML, pd.DataFrame()

    mode = "LLM-graded relevance" if use_llm else "keyword fallback (no LLM)"
    final_html = f"""
    <div style="padding: 0;">
        <div style="font-size: 13px; color: #666; margin-bottom: 6px;">Relevance mode: {mode}</div>
        {format_metric_html("Mean Reciprocal Rank (MRR)", totals["mrr"] / count, "mrr")}
        {format_metric_html("Normalized DCG (nDCG)", totals["ndcg"] / count, "ndcg")}
        {format_metric_html("Precision@k", totals["precision"] / count, "precision")}
        {format_metric_html("Recall@k (gold chunks)", totals["recall"] / count, "recall")}
        {format_metric_html("Keyword Coverage (diagnostic)", totals["coverage"] / count, "coverage", is_percentage=True)}
        {completion_banner(count)}
    </div>
    """

    category_data = [
        {"Category": category, "Average MRR": sum(scores) / len(scores)}
        for category, scores in category_mrr.items()
    ]
    return final_html, pd.DataFrame(category_data)


# ---------------------------------------------------------------------------
# Full (combined, parallelized, persisted) evaluation tab
# ---------------------------------------------------------------------------
def run_full_evaluation(progress=gr.Progress()):
    results = []
    for result, completed, total, prog_value in evaluate_all_full():
        results.append(result)
        progress(prog_value, desc=f"Evaluating test {completed}/{total}...")

    if not results:
        empty = pd.DataFrame()
        return EMPTY_HTML, empty, empty, None, None, load_history_df()

    saved = save_full_run(results)
    summary = saved["summary"]

    def tile(label, key, metric_type, **kw):
        return format_metric_html(label, summary[key]["mean"], metric_type, stdev=summary[key]["stdev"], **kw)

    final_html = f"""
    <div style="padding: 0;">
        {tile("MRR (LLM-graded)", "mrr", "mrr")}
        {tile("nDCG (LLM-graded)", "ndcg", "ndcg")}
        {tile("Precision@k", "precision_at_k", "precision")}
        {tile("Recall@k (gold chunks)", "recall_at_k", "recall")}
        {tile("Keyword Coverage (diagnostic)", "keyword_coverage", "coverage", is_percentage=True)}
        {tile("Accuracy", "accuracy", "accuracy", score_format=True)}
        {tile("Completeness", "completeness", "completeness", score_format=True)}
        {tile("Relevance", "relevance", "relevance", score_format=True)}
        {tile("Faithfulness", "faithfulness", "faithfulness", score_format=True)}
        {completion_banner(len(results), saved["failed"])}
    </div>
    """

    category_rows = [{"Category": category, **metrics} for category, metrics in summary["by_category"].items()]
    category_df = pd.DataFrame(category_rows)

    def _fmt_rank(v) -> str:
        return "—" if v is None or v == float("inf") else f"{v:.1f}"

    detail_rows = [
        {
            "Category": r.category,
            "Question": r.question,
            "MRR": round(r.retrieval.mrr, 3),
            "Precision@k": round(r.retrieval.precision_at_k, 3),
            "Recall@k": round(r.retrieval.recall_at_k, 3),
            "First Rank": _fmt_rank(r.retrieval.avg_first_rank),
            "Grades (0-2)": str(r.retrieval.relevance_grades),
            "Retrieved": " | ".join(r.retrieval.retrieved_sections),
            "Accuracy": r.answer_eval.accuracy,
            "Completeness": r.answer_eval.completeness,
            "Relevance": r.answer_eval.relevance,
            "Faithfulness": r.faithfulness.faithfulness,
            "Judge feedback": r.answer_eval.feedback,
            "Time (s)": round(r.elapsed_seconds, 1),
        }
        for r in results
    ]
    detail_df = pd.DataFrame(detail_rows).sort_values("Accuracy")

    return final_html, category_df, detail_df, saved["json_path"], saved["csv_path"], load_history_df()


# ---------------------------------------------------------------------------
# Run history tab
# ---------------------------------------------------------------------------
def load_history_df() -> pd.DataFrame:
    history = load_run_history()
    if not history:
        return pd.DataFrame()

    rows = []
    for entry in history:
        row = {"run_id": entry["run_id"], "timestamp": entry["timestamp"]}
        for metric in (
            "mrr", "ndcg", "precision_at_k", "recall_at_k", "keyword_coverage",
            "accuracy", "completeness", "relevance", "faithfulness",
        ):
            if isinstance(entry.get(metric), dict):
                row[metric] = round(entry[metric].get("mean", 0.0), 4)
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serif"])

    with gr.Blocks(title="Digital Twin Evaluation Dashboard", theme=theme) as app:
        gr.Markdown("# 📊 Digital Twin Evaluation Dashboard")
        gr.Markdown("Evaluate retrieval and answer quality for the digital twin's RAG pipeline")

        with gr.Tabs():
            # ---------------- FULL EVALUATION (recommended) ----------------
            with gr.Tab("⚡ Full Evaluation (recommended)"):
                gr.Markdown(
                    "Runs the full twin (rewrite, retrieval, answer) with tool notifications disabled, then judges "
                    "retrieval relevance, answer quality and faithfulness. Results are saved to "
                    "`evaluation/results/` as JSON and CSV, and added to the run history."
                )
                full_button = gr.Button("Run Full Evaluation", variant="primary", size="lg")
                full_metrics = gr.HTML(
                    "<div style='padding: 20px; text-align: center; color: #999;'>"
                    "Click 'Run Full Evaluation' to start</div>"
                )
                with gr.Row():
                    full_category_table = gr.Dataframe(label="Breakdown by Category", wrap=True)
                full_detail_table = gr.Dataframe(
                    label="Per-Test Detail (sorted by lowest accuracy)", wrap=True
                )
                with gr.Row():
                    json_download = gr.File(label="Download JSON")
                    csv_download = gr.File(label="Download CSV")

            # ---------------- Retrieval-only ----------------
            with gr.Tab("🔍 Retrieval Only"):
                gr.Markdown(
                    "Retrieval metrics only, no answers generated. Tests without keywords "
                    "(unanswerable / off-topic) are skipped here. Relevance is graded by one cheap LLM call per "
                    "test (cached across runs); untick the box for a free keyword-only fallback."
                )
                use_llm_box = gr.Checkbox(value=True, label="Use LLM relevance grading (same metrics as Full Evaluation)")
                retrieval_button = gr.Button("Run Retrieval Evaluation", variant="secondary", size="lg")
                with gr.Row():
                    with gr.Column(scale=1):
                        retrieval_metrics = gr.HTML(
                            "<div style='padding: 20px; text-align: center; color: #999;'>"
                            "Click 'Run Retrieval Evaluation' to start</div>"
                        )
                    with gr.Column(scale=1):
                        retrieval_chart = gr.BarPlot(
                            x="Category", y="Average MRR", title="Average MRR by Category",
                            y_lim=[0, 1], height=400,
                        )

            # ---------------- Run history ----------------
            with gr.Tab("📈 Run History"):
                gr.Markdown("Every saved 'Full Evaluation' run, for spotting regressions over time.")
                refresh_history_button = gr.Button("Refresh")
                history_table = gr.Dataframe(label="History", wrap=True, value=load_history_df())

        # Wiring
        full_button.click(
            fn=run_full_evaluation,
            outputs=[
                full_metrics, full_category_table, full_detail_table,
                json_download, csv_download, history_table,
            ],
        )
        retrieval_button.click(
            fn=run_retrieval_evaluation, inputs=[use_llm_box], outputs=[retrieval_metrics, retrieval_chart]
        )
        refresh_history_button.click(fn=load_history_df, outputs=[history_table])

    app.launch(inbrowser=True)


if __name__ == "__main__":
    main()