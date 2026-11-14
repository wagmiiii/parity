"""Tests for statistical methods: cluster bootstrap and exact McNemar."""

import pytest

from parity.stats.bootstrap import cluster_bootstrap_ci
from parity.stats.mcnemar import exact_mcnemar_test


def test_cluster_bootstrap_ci_coverage() -> None:
    # 20 templates with constant values
    template_ids = [f"T-{i}" for i in range(20) for _ in range(3)]
    values = [0.2] * len(template_ids)

    ci_low, ci_high = cluster_bootstrap_ci(
        template_ids=template_ids,
        values=values,
        n_resamples=200,
        seed=42,
    )
    assert ci_low == pytest.approx(0.2, abs=1e-5)
    assert ci_high == pytest.approx(0.2, abs=1e-5)


def test_exact_mcnemar_concordant() -> None:
    # Exactly concordant outcomes -> p-value = 1.0
    base = [1, 0, 1, 0, 1]
    rep = [1, 0, 1, 0, 1]
    res = exact_mcnemar_test(base, rep)
    assert res["b"] == 0
    assert res["c"] == 0
    assert res["p_value"] == 1.0


def test_exact_mcnemar_discordant() -> None:
    # 10 discordant pairs: 9 improved (1->0), 1 regressed (0->1)
    base = [1] * 9 + [0]
    rep = [0] * 9 + [1]
    res = exact_mcnemar_test(base, rep)
    assert res["b"] == 9
    assert res["c"] == 1
    # Binomial test p-value for 9 successes out of 10 trials with p=0.5
    # Two-sided p = 2 * (10 + 1) / 1024 ≈ 0.02148
    assert res["p_value"] < 0.05
