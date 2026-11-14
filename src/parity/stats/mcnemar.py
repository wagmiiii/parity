"""Exact McNemar test for paired binary outcomes (e.g. baseline vs repaired)."""

from collections.abc import Sequence

from scipy import stats


def exact_mcnemar_test(
    baseline_outcomes: Sequence[int],
    repaired_outcomes: Sequence[int],
) -> dict[str, float]:
    """Compute exact McNemar test for paired binary observations.

    Contingency table:
      b: baseline=1, repaired=0 (improved or changed 1->0)
      c: baseline=0, repaired=1 (regressed or changed 0->1)

    Returns:
      {"statistic": float, "p_value": float, "b": int, "c": int}
    """
    if len(baseline_outcomes) != len(repaired_outcomes):
        raise ValueError("baseline_outcomes and repaired_outcomes must match in length")

    b = sum(
        1
        for base, rep in zip(baseline_outcomes, repaired_outcomes, strict=True)
        if base == 1 and rep == 0
    )
    c = sum(
        1
        for base, rep in zip(baseline_outcomes, repaired_outcomes, strict=True)
        if base == 0 and rep == 1
    )

    n_discordant = b + c
    if n_discordant == 0:
        return {"statistic": 0.0, "p_value": 1.0, "b": 0, "c": 0}

    # Two-sided binomial test under H0: p = 0.5
    binom_result = stats.binomtest(b, n=n_discordant, p=0.5, alternative="two-sided")

    return {
        "statistic": float(b),
        "p_value": float(binom_result.pvalue),
        "b": b,
        "c": c,
    }
