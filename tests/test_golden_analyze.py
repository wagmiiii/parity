"""Golden analysis test for metrics computation pipeline."""

from parity.metrics.irg import compute_irg
from parity.report.tables import format_metrics_table
from parity.schemas import MetricResult, MetricScope, RefusalClass, Split


def test_golden_analyze_flow() -> None:
    pairs = [
        (RefusalClass.REFUSE, RefusalClass.COMPLY),
        (RefusalClass.COMPLY, RefusalClass.COMPLY),
    ]
    irg = compute_irg(pairs)
    assert irg == 0.5

    result = MetricResult(
        metric="irg",
        scope=MetricScope.GROUP,
        scope_id="wheelchair_user",
        condition="baseline",
        split=Split.DEV,
        estimate=irg,
        ci_low=0.1,
        ci_high=0.9,
        n_templates=2,
        n_prompts=4,
        method="cluster_bootstrap",
    )

    df = format_metrics_table([result])
    assert len(df) == 1
    assert df.iloc[0]["Metric"] == "IRG"
    assert df.iloc[0]["Estimate"] == "0.5000"
