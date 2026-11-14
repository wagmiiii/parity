"""Contract tests for third-party adapters (CuratorKIT, AuditKIT, SafeTune).

Tests run on mock fixtures without hitting network or GPU.
"""

from parity.adapters.audit import detect_refusal, run_model_inference
from parity.adapters.curator import diversify_templates
from parity.adapters.safetune import apply_steering, fit_steering_vectors


def test_curator_adapter_contract() -> None:
    res = diversify_templates(
        seed_templates_path="data/seeds",
        config_path="configs/curator_templates.yaml",
        output_path="data/build/v0.1",
    )
    assert isinstance(res, dict)
    assert "status" in res


def test_audit_adapter_contract() -> None:
    prompts = [{"prompt_id": "P-001", "text": "Hello world"}]
    responses = run_model_inference(
        prompts=prompts,
        model_id="test-model",
        condition="baseline",
        decoding_config={"temperature": 0.0},
    )
    assert isinstance(responses, list)

    label = detect_refusal("I cannot fulfill this request.")
    assert isinstance(label, str)


def test_safetune_adapter_contract() -> None:
    contrast_pairs = [{"positive": "comply prompt", "negative": "refuse prompt"}]
    fit_res = fit_steering_vectors(
        contrast_pairs=contrast_pairs,
        model_id="test-model",
        output_path="artifacts/test_vectors.pt",
    )
    assert isinstance(fit_res, dict)
    assert "status" in fit_res

    steered = apply_steering(model=None, steering_vector_path="artifacts/test_vectors.pt")
    assert steered is None
