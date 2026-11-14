"""SafeTune adapter for inference-time steering and LoRA hardening."""

from pathlib import Path
from typing import Any


def fit_steering_vectors(
    contrast_pairs: list[dict[str, str]],
    model_id: str,
    output_path: Path | str,
    layer_range: tuple[int, int] = (10, 24),
) -> dict[str, Any]:
    """Fit steering vectors using SafeTune steer API.

    # VERIFY: Inspect SafeTune runner.steer entrypoints and parameter names in installed source.
    """
    # Adapter stub
    return {
        "status": "not_implemented",
        "output_path": str(output_path),
        "layer_range": layer_range,
    }


def apply_steering(
    model: Any,
    steering_vector_path: Path | str,
    strength: float = 1.0,
) -> Any:
    """Apply steering vector hook to model during inference.

    # VERIFY: Check SafeTune hook / wrapper API in installed source.
    """
    # Adapter stub
    return model
