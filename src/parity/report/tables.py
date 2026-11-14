"""Tabular formatting and export of evaluation metrics."""

from pathlib import Path

import pandas as pd

from parity.schemas import MetricResult


def format_metrics_table(results: list[MetricResult]) -> pd.DataFrame:
    """Format MetricResult models into a clean presentation DataFrame."""
    rows = []
    for r in results:
        ci_str = (
            f"[{r.ci_low:.3f}, {r.ci_high:.3f}]"
            if (r.ci_low is not None and r.ci_high is not None)
            else "N/A"
        )
        rows.append(
            {
                "Metric": r.metric.upper(),
                "Scope": r.scope.value,
                "Scope ID": r.scope_id,
                "Condition": r.condition,
                "Split": r.split.value,
                "Estimate": f"{r.estimate:.4f}",
                "95% CI": ci_str,
                "N Templates": r.n_templates,
                "N Prompts": r.n_prompts,
            }
        )
    return pd.DataFrame(rows)


def save_metrics_reports(
    results: list[MetricResult],
    output_dir: Path | str = "reports/results",
) -> None:
    """Save metrics as both CSV and Parquet."""
    p = Path(output_dir)
    p.mkdir(parents=True, exist_ok=True)
    df = format_metrics_table(results)
    df.to_csv(p / "metrics_summary.csv", index=False)
    # Also save raw pydantic records as parquet
    raw_df = pd.DataFrame([r.model_dump() for r in results])
    raw_df.to_parquet(p / "metrics_raw.parquet", index=False)
