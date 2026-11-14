"""End-to-end test for response labeling and metrics analysis pipeline."""

import tempfile
from pathlib import Path

from parity.metrics.pipeline import run_full_analysis
from parity.report.tables import format_metrics_table, save_metrics_reports
from parity.schemas import Label, PromptPair, RefusalClass, RefusalSource, Split


def test_pipeline_end_to_end_mock() -> None:
    # 1. Load small subset from pilot pairs if present, or construct mock pairs
    pilot_path = Path("data/pilot/pilot_pairs.jsonl")
    assert pilot_path.exists(), "Pilot pairs file should exist"

    pairs: list[PromptPair] = []
    with open(pilot_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                pairs.append(PromptPair.model_validate_json(line))
            if len(pairs) >= 8:
                break

    assert len(pairs) == 8

    # 2. Construct mock labels map for the 8 pairs
    # For odd indices: identity refused, bare complied -> IRG > 0
    # For even indices: both complied -> IRG = 0
    labels_map: dict[tuple[str, str], Label] = {}
    for i, p in enumerate(pairs):
        ident_class = RefusalClass.REFUSE if (i % 2 == 1) else RefusalClass.COMPLY
        bare_class = RefusalClass.COMPLY

        labels_map[(p.pair_id, "identity")] = Label(
            run_id="mock-run",
            prompt_id=p.pair_id,
            variant="identity",
            refusal_class=ident_class,
            refusal_source=RefusalSource.RULE,
            human_override=False,
        )
        labels_map[(p.pair_id, "bare")] = Label(
            run_id="mock-run",
            prompt_id=p.pair_id,
            variant="bare",
            refusal_class=bare_class,
            refusal_source=RefusalSource.RULE,
            human_override=False,
        )

    # 3. Execute analysis pipeline
    results = run_full_analysis(
        pairs=pairs,
        labels_map=labels_map,
        condition="baseline",
        split=Split.PILOT,
        n_bootstrap=50,
        harmful_flags=[False, False, True],  # 1 out of 3 compliant -> THC = 1/3
        control_labels=[
            Label(
                run_id="mock-run",
                prompt_id="ctrl-01",
                variant="control",
                refusal_class=RefusalClass.COMPLY,
                refusal_source=RefusalSource.RULE,
            ),
            Label(
                run_id="mock-run",
                prompt_id="ctrl-02",
                variant="control",
                refusal_class=RefusalClass.REFUSE,
                refusal_source=RefusalSource.RULE,
            ),
        ],
    )

    assert len(results) > 0

    # Check metrics present
    metric_names = {r.metric for r in results}
    assert "irg" in metric_names
    assert "thc" in metric_names
    assert "corr" in metric_names

    # Check pooled IRG estimate
    pooled_res = [r for r in results if r.metric == "irg" and r.scope.value == "pooled"]
    assert len(pooled_res) == 1
    # 4 out of 8 pairs had refusal diff of +1, 4 had 0 -> mean = 0.50
    assert pooled_res[0].estimate == 0.50

    # 4. Check report table formatting and saving
    table_df = format_metrics_table(results)
    assert not table_df.empty
    assert "Metric" in table_df.columns
    assert "Estimate" in table_df.columns

    with tempfile.TemporaryDirectory() as tmp_dir:
        save_metrics_reports(results, output_dir=tmp_dir)
        tmp_p = Path(tmp_dir)
        assert (tmp_p / "metrics_summary.csv").exists()
        assert (tmp_p / "metrics_raw.parquet").exists()
