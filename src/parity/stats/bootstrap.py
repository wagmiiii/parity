"""Cluster bootstrap confidence intervals by template_id.

Since prompts originating from the same template are correlated,
we resample clusters (template_id) with replacement.
"""

from collections import defaultdict
from collections.abc import Callable, Sequence

import numpy as np


def cluster_bootstrap_ci(
    template_ids: Sequence[str],
    values: Sequence[float],
    statistic_fn: Callable[[Sequence[float]], float] = np.mean,
    n_resamples: int = 1000,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> tuple[float, float]:
    """Compute empirical percentile cluster bootstrap confidence interval.

    Returns:
        (ci_lower, ci_upper)
    """
    if len(template_ids) != len(values):
        raise ValueError("template_ids and values must have the same length")
    if not template_ids:
        return 0.0, 0.0

    # Group values by template cluster
    clusters: dict[str, list[float]] = defaultdict(list)
    for tid, val in zip(template_ids, values, strict=True):
        clusters[tid].append(val)

    unique_clusters = list(clusters.keys())
    n_clusters = len(unique_clusters)

    rng = np.random.default_rng(seed)
    boot_stats: list[float] = []

    for _ in range(n_resamples):
        sampled_indices = rng.choice(n_clusters, size=n_clusters, replace=True)
        sampled_values: list[float] = []
        for idx in sampled_indices:
            c_id = unique_clusters[idx]
            sampled_values.extend(clusters[c_id])
        boot_stats.append(statistic_fn(sampled_values))

    alpha = 1.0 - confidence_level
    ci_low = float(np.percentile(boot_stats, 100.0 * (alpha / 2.0)))
    ci_high = float(np.percentile(boot_stats, 100.0 * (1.0 - alpha / 2.0)))
    return ci_low, ci_high
