"""Tests for deterministic dataset splitting by template_id."""

from parity.build.split import assign_template_split
from parity.schemas import Split


def test_split_determinism() -> None:
    # A template must always map to the same split given the same seed
    tid = "T-housing-014"
    split1 = assign_template_split(tid, seed=42)
    split2 = assign_template_split(tid, seed=42)
    assert split1 == split2
    assert split1 in (Split.DEV, Split.TEST)


def test_no_template_in_both_splits() -> None:
    templates = [f"T-test-{i:03d}" for i in range(100)]
    dev_set = set()
    test_set = set()

    for tid in templates:
        s = assign_template_split(tid, seed=42)
        if s == Split.DEV:
            dev_set.add(tid)
        else:
            test_set.add(tid)

    # Disjoint check
    assert dev_set.isdisjoint(test_set)
    assert len(dev_set) + len(test_set) == len(templates)
    # Roughly balanced
    assert 35 <= len(dev_set) <= 65
