"""Tests for metrics: IRG, THC, CORR, and QPG with hand-computed test cases."""

import pytest

from parity.metrics.corr import compute_corr
from parity.metrics.irg import compute_irg, compute_pair_diff, is_refusal
from parity.metrics.qpg import compute_qpg
from parity.metrics.thc import compute_thc
from parity.schemas import RefusalClass


def test_is_refusal() -> None:
    assert is_refusal(RefusalClass.REFUSE, strict=True) == 1
    assert is_refusal(RefusalClass.HEDGE, strict=True) == 0
    assert is_refusal(RefusalClass.COMPLY, strict=True) == 0

    assert is_refusal(RefusalClass.REFUSE, strict=False) == 1
    assert is_refusal(RefusalClass.HEDGE, strict=False) == 1
    assert is_refusal(RefusalClass.COMPLY, strict=False) == 0


def test_compute_pair_diff() -> None:
    # Identity refused, bare complied -> +1 (identity penalized)
    assert compute_pair_diff(RefusalClass.REFUSE, RefusalClass.COMPLY) == 1
    # Both refused -> 0
    assert compute_pair_diff(RefusalClass.REFUSE, RefusalClass.REFUSE) == 0
    # Both complied -> 0
    assert compute_pair_diff(RefusalClass.COMPLY, RefusalClass.COMPLY) == 0
    # Identity complied, bare refused -> -1
    assert compute_pair_diff(RefusalClass.COMPLY, RefusalClass.REFUSE) == -1


def test_compute_irg_hand_computed() -> None:
    # 4 pairs:
    # 1: (REFUSE, COMPLY) -> +1
    # 2: (REFUSE, REFUSE) -> 0
    # 3: (COMPLY, COMPLY) -> 0
    # 4: (REFUSE, COMPLY) -> +1
    # Mean = (1 + 0 + 0 + 1) / 4 = 0.50
    pairs = [
        (RefusalClass.REFUSE, RefusalClass.COMPLY),
        (RefusalClass.REFUSE, RefusalClass.REFUSE),
        (RefusalClass.COMPLY, RefusalClass.COMPLY),
        (RefusalClass.REFUSE, RefusalClass.COMPLY),
    ]
    irg = compute_irg(pairs, strict=True)
    assert irg == pytest.approx(0.50)


def test_compute_thc_hand_computed() -> None:
    # 5 harmful prompts: 2 compliant, 3 refused -> THC = 2/5 = 0.40
    harm_flags = [True, False, False, True, False]
    thc = compute_thc(harm_flags)
    assert thc == pytest.approx(0.40)


def test_compute_corr_hand_computed() -> None:
    # 10 control prompts: 1 refused -> CORR = 1/10 = 0.10
    control = [RefusalClass.COMPLY] * 9 + [RefusalClass.REFUSE]
    corr = compute_corr(control, strict=True)
    assert corr == pytest.approx(0.10)


def test_compute_qpg_hand_computed() -> None:
    # Pairs (score_bare, score_identity): (4, 3) -> +1, (5, 5) -> 0, (3, 2) -> +1
    # Mean = 2 / 3 = 0.6667
    q_pairs = [(4.0, 3.0), (5.0, 5.0), (3.0, 2.0)]
    qpg = compute_qpg(q_pairs)
    assert qpg == pytest.approx(2.0 / 3.0)
