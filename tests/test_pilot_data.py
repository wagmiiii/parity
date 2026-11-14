"""Pair-diff property tests for pilot dataset (R-102, Gate G1).

Invariant:
Every minimal pair must differ from the bare variant by ONLY the inserted phrase.
"""

from pathlib import Path

from parity.config import load_groups_config
from parity.schemas import PromptPair, Role, Split


def test_pilot_pairs_exist_and_count() -> None:
    pilot_path = Path("data/pilot/pilot_pairs.jsonl")
    assert pilot_path.exists(), "pilot_pairs.jsonl does not exist"

    pairs: list[PromptPair] = []
    with open(pilot_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                pairs.append(PromptPair.model_validate_json(line))

    # Expecting 20 templates x 2 axes x 2 groups x 2 roles = 160 pairs (or at least 50 pairs)
    assert len(pairs) >= 50, f"Expected at least 50 pairs, found {len(pairs)}"


def test_pilot_pair_diff_property() -> None:
    pilot_path = Path("data/pilot/pilot_pairs.jsonl")
    groups_config = load_groups_config("configs/groups.yaml")

    # Map groups for lookup
    group_map = {}
    for axis_name, axis_def in groups_config.axes.items():
        for g in axis_def.groups:
            group_map[(axis_name, g.id)] = g

    with open(pilot_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            pair = PromptPair.model_validate_json(line)
            assert pair.split == Split.PILOT

            group = group_map.get((pair.axis, pair.group_id))
            assert group is not None, f"Unknown group: {pair.axis}/{pair.group_id}"

            if pair.role == Role.SPEAKER:
                ident_phrase = group.first_person
                filler_phrase = group.filler_first
            else:
                ident_phrase = group.third_person
                filler_phrase = group.filler_third

            # Invariant: identity variant contains identity phrase
            assert ident_phrase in pair.variants.identity

            # Invariant: filler variant contains filler phrase
            assert filler_phrase in pair.variants.filler

            # Invariant: bare variant does not contain identity or filler phrase
            assert ident_phrase not in pair.variants.bare
            assert filler_phrase not in pair.variants.bare

            # Property test: removing identity phrase yields bare variant (normalized)
            ident_stripped = pair.variants.identity.replace(ident_phrase, "")
            ident_normalized = " ".join(ident_stripped.split())
            bare_normalized = " ".join(pair.variants.bare.split())
            assert ident_normalized == bare_normalized, (
                f"Pair {pair.pair_id}: identity stripped '{ident_normalized}' != bare '{bare_normalized}'"
            )

            # Property test: removing filler phrase yields bare variant (normalized)
            filler_stripped = pair.variants.filler.replace(filler_phrase, "")
            filler_normalized = " ".join(filler_stripped.split())
            assert filler_normalized == bare_normalized, (
                f"Pair {pair.pair_id}: filler stripped '{filler_normalized}' != bare '{bare_normalized}'"
            )
