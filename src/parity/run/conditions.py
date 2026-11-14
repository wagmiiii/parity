"""Execution conditions and environment definitions."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class ConditionType(StrEnum):
    BASELINE = "baseline"
    STEERED = "steered"
    SYSPROMPT = "sysprompt"


class ConditionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    condition_type: ConditionType
    system_prompt: str | None = None
    steering_artifact: str | None = None
    steering_strength: float = 1.0
    extra_params: dict[str, Any] | None = None
