"""Judge-based classifier for ambiguous refusal, harm compliance, and QPG scoring."""

from typing import Any

from parity.schemas import RefusalClass


def evaluate_refusal_judge(prompt: str, response: str, judge_model: str) -> RefusalClass:
    """Use an LLM judge to classify ambiguous responses."""
    # Stub: to be connected to LiteLLM / AuditKIT judge
    return RefusalClass.COMPLY


def evaluate_harm_compliance(prompt: str, response: str, judge_model: str) -> bool:
    """Judge whether response complied with a group-targeted harmful request."""
    # Stub: returns True if harm compliant, False if refused
    return False


def score_quality_qpg(
    prompt: str, response_a: str, response_b: str, judge_model: str
) -> dict[str, Any]:
    """Score relative quality difference (QPG) on pairs where both complied."""
    # Stub
    return {"score_a": 3, "score_b": 3, "delta": 0.0}
