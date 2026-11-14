"""AuditKIT adapter for model evaluation, inference, and refusal detection."""

from typing import Any

from parity.schemas import Response


def run_model_inference(
    prompts: list[dict[str, str]],
    model_id: str,
    condition: str,
    decoding_config: dict[str, Any],
) -> list[Response]:
    """Run model inference via AuditKIT hf: backend.

    # VERIFY: Check AuditKIT evaluate / runner call signatures against installed source.
    """
    # Adapter stub
    return []


def detect_refusal(text: str) -> str:
    """Run AuditKIT refusal detector on output text.

    # VERIFY: Inspect AuditKIT detector signatures in installed source.
    """
    # Adapter stub
    return "comply"
