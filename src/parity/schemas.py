"""Pydantic schemas for Parity data records and file boundaries.

All records are validated through these models when serialized to or deserialized from JSONL.
"""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Split(StrEnum):
    DEV = "dev"
    TEST = "test"
    PILOT = "pilot"


class Role(StrEnum):
    SPEAKER = "speaker"
    SUBJECT = "subject"


class RefusalClass(StrEnum):
    REFUSE = "refuse"
    HEDGE = "hedge"
    COMPLY = "comply"
    EMPTY = "empty"


class RefusalSource(StrEnum):
    RULE = "rule"
    JUDGE = "judge"
    HUMAN = "human"


class HarmCategory(StrEnum):
    DEMEANING_CONTENT = "demeaning_content"
    DISCRIMINATION_ADVICE = "discrimination_advice"
    HARASSMENT_PLANNING = "harassment_planning_category_level"
    STEREOTYPE_ENDORSEMENT = "stereotype_endorsement"


class MetricScope(StrEnum):
    POOLED = "pooled"
    AXIS = "axis"
    GROUP = "group"


class PairVariants(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bare: str
    filler: str
    identity: str


class PromptPair(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pair_id: str
    template_id: str
    axis: str
    group_id: str
    role: Role
    task_domain: str
    variants: PairVariants
    split: Split
    identity_irrelevant_ok: bool | None = None
    provenance: dict[str, Any] | None = None


class HarmPrompt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_id: str
    template_id: str
    axis: str
    group_id: str
    harm_category: HarmCategory
    text: str
    matched_nongroup_text: str | None = None
    split: Split


class ControlPrompt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_id: str
    task_domain: str
    text: str
    split: Split


class RunConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    model_id: str
    condition: str
    decoding: dict[str, Any] = Field(default_factory=dict)
    seed: int = 42
    git_sha: str | None = None
    config_hash: str | None = None
    lib_versions: dict[str, str] | None = None
    benchmark_version: str | None = None
    benchmark_checksum: str | None = None


class Response(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    prompt_id: str
    variant: str  # bare | filler | identity | harmful | control
    text: str
    n_tokens: int
    truncated: bool = False
    empty: bool = False


class Run(BaseModel):
    model_config = ConfigDict(extra="forbid")

    config: RunConfig
    timestamp: str | None = None
    responses: list[Response] = Field(default_factory=list)


class Label(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    prompt_id: str
    variant: str
    refusal_class: RefusalClass
    refusal_source: RefusalSource
    harm_compliant: bool | None = None
    judge_quality: int | None = None
    judge_id: str | None = None
    human_override: bool = False

    @property
    def response_key(self) -> str:
        return f"{self.run_id}:{self.prompt_id}:{self.variant}"


class MetricResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric: str  # irg | thc | corr | qpg
    scope: MetricScope  # pooled | axis | group
    scope_id: str
    condition: str
    split: Split
    estimate: float
    ci_low: float | None = None
    ci_high: float | None = None
    n_templates: int
    n_prompts: int
    method: str


class GroupDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    first_person: str
    third_person: str
    filler_first: str
    filler_third: str


class AxisDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    groups: list[GroupDefinition]


class GroupsConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    axes: dict[str, AxisDefinition]
