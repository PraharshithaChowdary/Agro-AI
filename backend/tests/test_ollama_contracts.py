"""Unit tests for structured local-vision normalization (no Ollama daemon needed)."""
from app.services.ollama_service import OllamaService


def test_normalizer_keeps_summary_about_image_and_uses_no_confidence_score():
    raw = {
        "is_agricultural": True,
        "image_type": "fruit",
        "subject_name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "visible_condition": "possible_spoilage",
        "ripeness_status": "overripe",
        "spoilage_status": "possible_visible_spoilage",
        "visible_observations": ["A darkened patch is visible near the stem."],
        "possible_issues": [{"name": "Possible external rot", "evidence": "Dark softened-looking area visible on the surface", "likelihood": "moderate"}],
        "summary": "The photo shows a tomato with a darkened patch near the stem. Internal condition cannot be inferred.",
        "recommendations": ["Keep suspect produce separate while inspecting it."],
        "precautions": ["Do not use this photo alone to determine food safety."],
        "uncertainty_notes": ["Internal rot cannot be confirmed."],
    }
    normalized = OllamaService._normalize_report(raw, "")
    assert normalized["image_type"] == "fruit"
    assert normalized["visible_condition"] == "possible_spoilage"
    assert "tomato" in normalized["summary"].lower()
    assert normalized["possible_issues"][0]["likelihood"] == "moderate"
    assert all("confidence" not in key.lower() for key in normalized)


def test_normalizer_sanitizes_chemical_dose_recommendations():
    raw = {
        "is_agricultural": True,
        "image_type": "leaf",
        "subject_name": "Leaf",
        "visible_condition": "possible_stress",
        "ripeness_status": "not_applicable",
        "spoilage_status": "not_applicable",
        "summary": "Yellow spots are visible on the leaf.",
        "recommendations": ["Spray pesticide at a specific dose immediately."],
        "precautions": ["Apply fungicide dosage now."],
    }
    normalized = OllamaService._normalize_report(raw, "")
    assert "Do not choose a chemical treatment" in normalized["recommendations"][0]
    assert "Confirm any treatment" in normalized["precautions"][0]


def test_unparseable_model_response_becomes_uncertain_instead_of_forced_diagnosis():
    report = OllamaService._parse_json("not valid json; probably blight")
    normalized = OllamaService._normalize_report(report, "not valid json; probably blight")
    assert normalized["image_type"] == "uncertain"
    assert normalized["visible_condition"] == "uncertain"
    assert normalized["possible_issues"] == []
    assert "probably blight" in normalized["summary"]


def test_default_vision_model_is_qwen_vl(monkeypatch):
    monkeypatch.delenv("OLLAMA_VISION_MODEL", raising=False)
    assert OllamaService.vision_model() == "qwen2.5vl:3b"


def test_image_preparation_converts_image_to_jpeg_base64():
    import base64
    import io
    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGBA", (20, 10), (40, 120, 40, 255)).save(buffer, format="PNG")
    encoded = OllamaService._prepare_image(buffer.getvalue())
    decoded = base64.b64decode(encoded)
    with Image.open(io.BytesIO(decoded)) as result:
        assert result.format == "JPEG"
        assert result.mode == "RGB"
        assert result.size == (20, 10)


def test_model_readiness_requires_the_configured_qwen_tag():
    assert OllamaService._model_installed("qwen2.5vl:3b", ["qwen2.5vl:3b"])
    assert not OllamaService._model_installed("qwen2.5vl:3b", ["qwen2.5vl:7b"])
    assert OllamaService._model_installed("moondream", ["moondream:latest"])


def test_image_analysis_sends_image_to_qwen_vl_and_returns_structured_report(monkeypatch):
    import json
    import app.services.ollama_service as ollama_module

    monkeypatch.setenv("OLLAMA_VISION_MODEL", "qwen2.5vl:3b")
    monkeypatch.setattr(OllamaService, "_assert_model_ready", classmethod(lambda cls, model: None))
    monkeypatch.setattr(OllamaService, "_prepare_image", classmethod(lambda cls, image_bytes: "ZmFrZQ=="))
    expected = {
        "is_agricultural": True,
        "image_type": "leaf",
        "subject_name": "Leaf",
        "visible_condition": "possible_stress",
        "ripeness_status": "not_applicable",
        "spoilage_status": "not_applicable",
        "visible_observations": ["Small yellow spots are visible."],
        "possible_issues": [],
        "summary": "A leaf is visible with a few yellow spots. The cause cannot be confirmed from this photo.",
        "recommendations": ["Photograph the same leaf again in good light."],
        "precautions": ["Confirm spreading symptoms with a local agricultural adviser."],
        "uncertainty_notes": ["A photograph cannot confirm a plant pathogen."],
    }
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None
        def json(self):
            return {"message": {"content": json.dumps(expected)}}

    def fake_post(url, **kwargs):
        captured.update({"url": url, "payload": kwargs["json"], "timeout": kwargs["timeout"]})
        return FakeResponse()

    monkeypatch.setattr(ollama_module.httpx, "post", fake_post)
    report = OllamaService.analyze_image(b"test-image", task="plant")
    assert captured["url"].endswith("/api/chat")
    assert captured["payload"]["model"] == "qwen2.5vl:3b"
    assert captured["payload"]["format"] == "json"
    assert captured["payload"]["messages"][0]["images"] == ["ZmFrZQ=="]
    assert report["image_type"] == "leaf"
    assert "yellow spots" in report["summary"]


def test_image_preparation_resizes_large_upload_for_local_memory(monkeypatch):
    import base64
    import io
    from PIL import Image

    monkeypatch.setenv("OLLAMA_IMAGE_MAX_SIDE", "896")
    buffer = io.BytesIO()
    Image.new("RGB", (2400, 1600), (30, 110, 40)).save(buffer, format="PNG")
    encoded = OllamaService._prepare_image(buffer.getvalue())
    with Image.open(io.BytesIO(base64.b64decode(encoded))) as result:
        assert max(result.size) == 896
        assert result.format == "JPEG"


def test_runner_crash_error_gives_actionable_local_diagnostic(monkeypatch):
    import httpx
    import app.services.ollama_service as ollama_module
    from app.services.ollama_service import OllamaServiceError

    monkeypatch.setattr(OllamaService, "_assert_model_ready", classmethod(lambda cls, model: None))
    monkeypatch.setattr(OllamaService, "_prepare_image", classmethod(lambda cls, image_bytes: "ZmFrZQ=="))
    request = httpx.Request("POST", "http://127.0.0.1:11434/api/chat")
    response = httpx.Response(500, request=request, json={"error": "an error was encountered while running the model: unexpected EOF"})

    class FakeFailureResponse:
        def raise_for_status(self):
            response.raise_for_status()

    monkeypatch.setattr(ollama_module.httpx, "post", lambda *args, **kwargs: FakeFailureResponse())
    try:
        OllamaService.analyze_image(b"image-bytes", task="plant")
    except OllamaServiceError as exc:
        assert "runner stopped unexpectedly" in str(exc)
        assert "update Ollama" in str(exc)
    else:
        raise AssertionError("Expected an actionable Ollama runner error")
