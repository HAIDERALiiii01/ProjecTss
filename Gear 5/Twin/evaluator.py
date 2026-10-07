"""
RAG Evaluation Dashboard (Gradio)
=================================
Two working modes plus a history view:

- "Full Evaluation" — the recommended path. Runs retrieval + answer quality +
  faithfulness together off a single retrieval call per test (see eval.py),
  saves results to disk, and adds a row to the run history.
- "Retrieval Only" — fast, zero LLM-judge cost. Use this to iterate on
  chunking/embedding/search changes without burning judge tokens.
- "Run History" — every saved Full Evaluation run, to spot regressions.

(An "Answer Only" mode was deliberately dropped: it costs the same as Full
Evaluation but reports fewer metrics and still double-fetches context, so
there's no scenario where it beats Full Evaluation.)
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
# Color-coding thresholds (single source of truth)
# ---------------------------------------------------------------------------
THRESHOLDS = {
    "mrr": (0.90, 0.75),
    "ndcg": (0.90, 0.75),
    "precision": (0.90, 0.75),
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


def completion_banner(count: int) -> str:
    return f"""
    <div style="margin-top: 20px; padding: 10px; background-color: #d4edda; border-radius: 5px;
                text-align: center; border: 1px solid #c3e6cb;">
        <span style="font-size: 14px; color: #155724; font-weight: bold;">
            ✓ Evaluation complete · {count} tests
        </span>
    </div>
    """


# ---------------------------------------------------------------------------
# Retrieval-only tab
# ---------------------------------------------------------------------------
def run_retrieval_evaluation(progress=gr.Progress()):
    total_mrr = total_ndcg = total_precision = total_recall = total_coverage = 0.0
    category_mrr = defaultdict(list)
    count = 0

    for test, result, prog_value in evaluate_all_retrieval():
        count += 1
        total_mrr += result.mrr
        total_ndcg += result.ndcg
        total_precision += result.precision_at_k
        total_recall += result.recall_at_k
        total_coverage += result.keyword_coverage
        category_mrr[test.category].append(result.mrr)
        progress(prog_value, desc=f"Evaluating retrieval · test {count}...")

    if count == 0:
        return (
            "<div style='color:red;padding:20px;'>No tests completed — check logs for errors.</div>",
            pd.DataFrame(),
        )

    final_html = f"""
    <div style="padding: 0;">
        {format_metric_html("Mean Reciprocal Rank (MRR)", total_mrr / count, "mrr")}
        {format_metric_html("Normalized DCG (nDCG)", total_ndcg / count, "ndcg")}
        {format_metric_html("Precision@k", total_precision / count, "precision")}
        {format_metric_html("Recall@k", total_recall / count, "recall")}
        {format_metric_html("Keyword Coverage", total_coverage / count, "coverage", is_percentage=True)}
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
    """
    Runs retrieval + answer + faithfulness together off a single retrieval call
    per test, in parallel across tests. Saves results to disk at the end and
    returns a per-test detail table plus download links.
    """
    results = []
    for result, completed, total, prog_value in evaluate_all_full():
        results.append(result)
        progress(prog_value, desc=f"Evaluating test {completed}/{total}...")

    if not results:
        empty = pd.DataFrame()
        return (
            "<div style='color:red;padding:20px;'>No tests completed — check logs for errors.</div>",
            empty, empty, None, None, empty,
        )

    saved = save_full_run(results)
    summary = saved["summary"]

    final_html = f"""
    <div style="padding: 0;">
        {format_metric_html("MRR", summary["mrr"]["mean"], "mrr", stdev=summary["mrr"]["stdev"])}
        {format_metric_html("nDCG", summary["ndcg"]["mean"], "ndcg", stdev=summary["ndcg"]["stdev"])}
        {format_metric_html("Precision@k", summary["precision_at_k"]["mean"], "precision", stdev=summary["precision_at_k"]["stdev"])}
        {format_metric_html("Recall@k", summary["recall_at_k"]["mean"], "recall", stdev=summary["recall_at_k"]["stdev"])}
        {format_metric_html("Keyword Coverage", summary["keyword_coverage"]["mean"], "coverage", is_percentage=True, stdev=summary["keyword_coverage"]["stdev"])}
        {format_metric_html("Accuracy", summary["accuracy"]["mean"], "accuracy", score_format=True, stdev=summary["accuracy"]["stdev"])}
        {format_metric_html("Completeness", summary["completeness"]["mean"], "completeness", score_format=True, stdev=summary["completeness"]["stdev"])}
        {format_metric_html("Relevance", summary["relevance"]["mean"], "relevance", score_format=True, stdev=summary["relevance"]["stdev"])}
        {format_metric_html("Faithfulness", summary["faithfulness"]["mean"], "faithfulness", score_format=True, stdev=summary["faithfulness"]["stdev"])}
        {completion_banner(len(results))}
    </div>
    """

    # Per-category breakdown across every metric
    category_rows = []
    for category, metrics in summary["by_category"].items():
        row = {"Category": category}
        row.update(metrics)
        category_rows.append(row)
    category_df = pd.DataFrame(category_rows)

    # Per-test detail table for drilling into individual failures
    def _fmt_rank(v: float) -> str:
        return "—" if v == float("inf") else f"{v:.1f}"

    detail_rows = [
        {
            "Category": r.category,
            "Question": r.question,
            "MRR": round(r.retrieval.mrr, 3),
            "Precision@k": round(r.retrieval.precision_at_k, 3),
            "Recall@k": round(r.retrieval.recall_at_k, 3),
            "Avg First Rank": _fmt_rank(r.retrieval.avg_first_rank),
            "Accuracy": r.answer_eval.accuracy,
            "Completeness": r.answer_eval.completeness,
            "Relevance": r.answer_eval.relevance,
            "Faithfulness": r.faithfulness.faithfulness,
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
            if metric in entry and isinstance(entry[metric], dict):
                row[metric] = entry[metric].get("mean")
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serif"])

    with gr.Blocks(title="RAG Evaluation Dashboard", theme=theme) as app:
        gr.Markdown("# 📊 RAG Evaluation Dashboard")
        gr.Markdown("Evaluate retrieval and answer quality for the Insurellm RAG system")

        with gr.Tabs():
            # ---------------- FULL EVALUATION (recommended) ----------------
            with gr.Tab("⚡ Full Evaluation (recommended)"):
                gr.Markdown(
                    "Runs retrieval + answer quality + faithfulness together, in parallel, "
                    "off a single retrieval call per test. Results are saved to `results/` "
                    "as JSON and CSV, and added to the run history below."
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
            with gr.Tab("🔍 Retrieval Only (fast, no LLM cost)"):
                gr.Markdown(
                    "Skips the LLM judges entirely — use this to quickly check the effect of "
                    "chunking, embedding, or search changes without burning judge-model tokens."
                )
                retrieval_button = gr.Button("Run Retrieval Evaluation", variant="secondary", size="lg")
                with gr.Row():
                    with gr.Column(scale=1):
                        retrieval_metrics = gr.HTML(
                            "<div style='padding: 20px; text-align: center; color: #999;'>"
                            "Click 'Run Evaluation' to start</div>"
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
        retrieval_button.click(fn=run_retrieval_evaluation, outputs=[retrieval_metrics, retrieval_chart])
        refresh_history_button.click(fn=load_history_df, outputs=[history_table])

    app.launch(inbrowser=True)


if __name__ == "__main__":
    main()