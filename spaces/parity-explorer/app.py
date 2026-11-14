"""Parity Explorer: Read-only Gradio viewer for benchmark pairs and audit results."""

from pathlib import Path

import gradio as gr
import pandas as pd


def load_metrics(results_dir: str = "reports/results") -> pd.DataFrame:
    """Load precomputed metrics from parquet or csv if available."""
    p = Path(results_dir)
    parquet_files = list(p.glob("*.parquet"))
    if parquet_files:
        return pd.read_parquet(parquet_files[0])
    csv_files = list(p.glob("*.csv"))
    if csv_files:
        return pd.read_csv(csv_files[0])
    return pd.DataFrame(
        columns=[
            "metric",
            "scope",
            "scope_id",
            "condition",
            "split",
            "estimate",
            "ci_low",
            "ci_high",
        ]
    )


def create_demo() -> gr.Blocks:
    with gr.Blocks(title="Parity Explorer") as demo:
        gr.Markdown("# Parity Explorer\nAudit and repair of identity treatment gaps.")
        with gr.Tab("Summary Metrics"):
            metrics_table = gr.Dataframe(value=load_metrics)
            refresh_btn = gr.Button("Refresh")
            refresh_btn.click(fn=load_metrics, outputs=metrics_table)
        with gr.Tab("Pair Viewer"):
            gr.Markdown("Browse benchmark prompt pairs and model responses.")
    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch()
