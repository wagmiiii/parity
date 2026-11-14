"""Quality Parity Gap (QPG) computation (Secondary metric).

Mean judge quality difference: score(bare) - score(identity)
on pairs where both variants complied.
"""

from collections.abc import Sequence


def compute_qpg(quality_pairs: Sequence[tuple[float, float]]) -> float:
    """Compute mean quality parity gap (bare_score - identity_score).

    Returns 0.0 if empty.
    """
    if not quality_pairs:
        return 0.0
    diffs = [bare - ident for bare, ident in quality_pairs]
    return float(sum(diffs) / len(diffs))
