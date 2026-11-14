"""Pipeline for computing and aggregating evaluation metrics (IRG, THC, CORR, QPG)."""

from collections import defaultdict

from parity.metrics.corr import compute_corr
from parity.metrics.irg import compute_irg, compute_pair_diff
from parity.metrics.thc import compute_thc
from parity.schemas import (
    Label,
    MetricResult,
    MetricScope,
    PromptPair,
    Split,
)
from parity.stats.bootstrap import cluster_bootstrap_ci


def run_full_analysis(
    pairs: list[PromptPair],
    labels_map: dict[tuple[str, str], Label],  # (prompt_id, variant) -> Label
    condition: str = "baseline",
    split: Split = Split.DEV,
    strict_refusal: bool = True,
    n_bootstrap: int = 1000,
    harmful_flags: list[bool] | None = None,
    control_labels: list[Label] | None = None,
) -> list[MetricResult]:
    """Compute complete metric hierarchy: per-group, per-axis, and pooled."""
    results: list[MetricResult] = []

    # Organize pairs by (axis, group_id) and by axis
    axis_group_pairs: dict[tuple[str, str], list[PromptPair]] = defaultdict(list)
    axis_pairs: dict[str, list[PromptPair]] = defaultdict(list)

    for p in pairs:
        axis_group_pairs[(p.axis, p.group_id)].append(p)
        axis_pairs[p.axis].append(p)

    # 1. Per-Group IRG
    for (_axis_name, group_id), group_pairs in axis_group_pairs.items():
        pair_diffs: list[float] = []
        template_ids: list[str] = []
        pair_tuples = []

        for p in group_pairs:
            # Pair prompt_id is pair_id or template_id
            ident_key = (p.pair_id, "identity")
            bare_key = (p.pair_id, "bare")
            if ident_key in labels_map and bare_key in labels_map:
                l_ident = labels_map[ident_key].refusal_class
                l_bare = labels_map[bare_key].refusal_class
                pair_tuples.append((l_ident, l_bare))
                pair_diffs.append(float(compute_pair_diff(l_ident, l_bare, strict=strict_refusal)))
                template_ids.append(p.template_id)

        if pair_diffs:
            estimate = compute_irg(pair_tuples, strict=strict_refusal)
            ci_low, ci_high = cluster_bootstrap_ci(
                template_ids=template_ids,
                values=pair_diffs,
                n_resamples=n_bootstrap,
            )
            results.append(
                MetricResult(
                    metric="irg",
                    scope=MetricScope.GROUP,
                    scope_id=group_id,
                    condition=condition,
                    split=split,
                    estimate=estimate,
                    ci_low=ci_low,
                    ci_high=ci_high,
                    n_templates=len(set(template_ids)),
                    n_prompts=len(pair_diffs) * 2,
                    method="cluster_bootstrap",
                )
            )

    # 2. Per-Axis IRG
    for axis_name, a_pairs in axis_pairs.items():
        pair_diffs = []
        template_ids = []
        pair_tuples = []

        for p in a_pairs:
            ident_key = (p.pair_id, "identity")
            bare_key = (p.pair_id, "bare")
            if ident_key in labels_map and bare_key in labels_map:
                l_ident = labels_map[ident_key].refusal_class
                l_bare = labels_map[bare_key].refusal_class
                pair_tuples.append((l_ident, l_bare))
                pair_diffs.append(float(compute_pair_diff(l_ident, l_bare, strict=strict_refusal)))
                template_ids.append(p.template_id)

        if pair_diffs:
            estimate = compute_irg(pair_tuples, strict=strict_refusal)
            ci_low, ci_high = cluster_bootstrap_ci(
                template_ids=template_ids,
                values=pair_diffs,
                n_resamples=n_bootstrap,
            )
            results.append(
                MetricResult(
                    metric="irg",
                    scope=MetricScope.AXIS,
                    scope_id=axis_name,
                    condition=condition,
                    split=split,
                    estimate=estimate,
                    ci_low=ci_low,
                    ci_high=ci_high,
                    n_templates=len(set(template_ids)),
                    n_prompts=len(pair_diffs) * 2,
                    method="cluster_bootstrap",
                )
            )

    # 3. Pooled IRG
    all_diffs = []
    all_tids = []
    all_tuples = []
    for p in pairs:
        ident_key = (p.pair_id, "identity")
        bare_key = (p.pair_id, "bare")
        if ident_key in labels_map and bare_key in labels_map:
            l_ident = labels_map[ident_key].refusal_class
            l_bare = labels_map[bare_key].refusal_class
            all_tuples.append((l_ident, l_bare))
            all_diffs.append(float(compute_pair_diff(l_ident, l_bare, strict=strict_refusal)))
            all_tids.append(p.template_id)

    if all_diffs:
        pooled_estimate = compute_irg(all_tuples, strict=strict_refusal)
        ci_low, ci_high = cluster_bootstrap_ci(
            template_ids=all_tids,
            values=all_diffs,
            n_resamples=n_bootstrap,
        )
        results.append(
            MetricResult(
                metric="irg",
                scope=MetricScope.POOLED,
                scope_id="pooled",
                condition=condition,
                split=split,
                estimate=pooled_estimate,
                ci_low=ci_low,
                ci_high=ci_high,
                n_templates=len(set(all_tids)),
                n_prompts=len(all_diffs) * 2,
                method="cluster_bootstrap",
            )
        )

    # 4. THC (if harmful flags present)
    if harmful_flags:
        thc_est = compute_thc(harmful_flags)
        results.append(
            MetricResult(
                metric="thc",
                scope=MetricScope.POOLED,
                scope_id="pooled",
                condition=condition,
                split=split,
                estimate=thc_est,
                ci_low=None,
                ci_high=None,
                n_templates=len(harmful_flags),
                n_prompts=len(harmful_flags),
                method="exact",
            )
        )

    # 5. CORR (if control labels present)
    if control_labels:
        c_classes = [cl.refusal_class for cl in control_labels]
        corr_est = compute_corr(c_classes, strict=strict_refusal)
        results.append(
            MetricResult(
                metric="corr",
                scope=MetricScope.POOLED,
                scope_id="pooled",
                condition=condition,
                split=split,
                estimate=corr_est,
                ci_low=None,
                ci_high=None,
                n_templates=len(control_labels),
                n_prompts=len(control_labels),
                method="exact",
            )
        )

    return results
