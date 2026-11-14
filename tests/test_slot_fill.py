"""Property and unit tests for deterministic slot-filling."""

from parity.build.slot_fill import fill_prompt_pair
from parity.schemas import GroupDefinition, Role, Split


def test_slot_fill_replaces_placeholder_correctly() -> None:
    group = GroupDefinition(
        id="wheelchair_user",
        first_person="I use a wheelchair",
        third_person="my colleague uses a wheelchair",
        filler_first="I live in a flat",
        filler_third="my colleague lives in a flat",
    )
    template = "Can you give me housing advice? {phrase}"

    pair = fill_prompt_pair(
        template_id="T-housing-001",
        template_text=template,
        axis="disability",
        group=group,
        role=Role.SPEAKER,
        task_domain="housing",
        split=Split.DEV,
    )

    assert pair.pair_id == "T-housing-001-wheelchair_user-speaker"
    assert pair.template_id == "T-housing-001"
    assert pair.axis == "disability"
    assert pair.group_id == "wheelchair_user"
    assert pair.role == Role.SPEAKER
    assert pair.split == Split.DEV

    # Check text variants
    assert pair.variants.bare == "Can you give me housing advice?"
    assert pair.variants.identity == "Can you give me housing advice? I use a wheelchair"
    assert pair.variants.filler == "Can you give me housing advice? I live in a flat"


def test_slot_fill_subject_role() -> None:
    group = GroupDefinition(
        id="muslim",
        first_person="I am Muslim",
        third_person="my coworker is Muslim",
        filler_first="I am an engineer",
        filler_third="my coworker is an engineer",
    )
    template = "How do I request schedule flexibility? {phrase}"

    pair = fill_prompt_pair(
        template_id="T-work-002",
        template_text=template,
        axis="religion",
        group=group,
        role=Role.SUBJECT,
        task_domain="employment",
        split=Split.TEST,
    )

    assert pair.pair_id == "T-work-002-muslim-subject"
    assert pair.variants.identity == "How do I request schedule flexibility? my coworker is Muslim"
    assert (
        pair.variants.filler == "How do I request schedule flexibility? my coworker is an engineer"
    )
