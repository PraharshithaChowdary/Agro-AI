"""Deterministic image-service doubles for API contract tests.

These tests validate routing, schema handling, and persistence without downloading or
running multi-GB models. They do NOT measure real-model identification accuracy.
The real Ollama HTTP/model path has separate unit tests below.
"""
from __future__ import annotations

import io
import statistics
from datetime import datetime, timezone
from typing import Any

import pytest
from PIL import Image


def _kind(image_bytes: bytes) -> str:
    try:
        with Image.open(io.BytesIO(image_bytes)) as im:
            im = im.convert("RGB")
            w, h = im.size
            pix = im.load()
            r, g, b = pix[w // 2, h // 2]
            r0, g0, b0 = pix[0, 0]
            if w > 500 or h > 500:
                return "non_agricultural"
            if b0 > 150 and b0 > r0 * 1.35 and b0 > g0 * 1.35:
                return "non_agricultural"
            if r > 160 and g < 100 and b < 160:
                return "flower"
            if b > r * 1.15 and b > g * 1.15:
                return "vegetable"
            if r0 > 75 and r0 > g0 * 1.35 and g0 > b0 * 1.3:
                return "soil"
            return "leaf"
    except Exception:
        return "non_agricultural"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _recommendations() -> list[dict[str, str]]:
    return [
        {"title": f"Next step {i}", "description": text, "type": "prevention" if i > 1 else "action"}
        for i, text in enumerate([
            "Inspect the affected area in natural light.",
            "Take a close-up and a whole-plant photo for comparison.",
            "Avoid applying a treatment until the cause is confirmed.",
            "Ask a local agricultural extension adviser if symptoms spread.",
        ], 1)
    ]


def _plant_report(image_bytes: bytes, plant_name: str, crop_type: str | None, growing_location: str | None) -> dict[str, Any]:
    kind = _kind(image_bytes)
    if kind in {"soil", "non_agricultural"}:
        return {"_wrong_module": "This image does not appear to contain a plant or crop. Upload a clear agricultural photo."}
    name = "Monstera / Swiss Cheese Plant" if plant_name.lower() == "monstera" else (plant_name or "Uncertain plant")
    return {
        "isPlantImage": True, "validationStatus": "Ollama visual screening",
        "validationMessage": "Visual candidate only; identity and health are not confirmed.",
        "userPlantName": name, "hindiName": "", "scientificName": None,
        "cropType": crop_type or kind.title(), "growingLocation": growing_location or "Not specified",
        "healthAssessment": "Uncertain / Inconclusive", "healthScorePercentage": 0.0,
        "observedSymptoms": [
            {"name": "Visual observation", "severity": "None", "percentage": 0.0,
             "observation": "An image-level observation for route testing; not a diagnosis."}
            for _ in range(4)
        ],
        "hasSymptoms": False, "diseaseModelAvailable": False,
        "possibleDisease": None, "diseaseConfidence": None,
        "diseaseDiagnosisNotice": "No validated disease classifier was run in this test.",
        "careGuide": {"watering": "Check soil moisture.", "sunlight": "Check species needs.", "soil": "Use suitable well-drained soil.", "humidity": "Monitor airflow.", "nutrition": "Use soil-test guidance."},
        "recommendations": _recommendations(), "generalManagementTips": ["Inspect regularly."],
        "disclaimer": "Test result only. Image-based screening cannot confirm disease.", "analysisTimestamp": _now(),
        "imageType": kind, "detectedSubject": name, "visibleCondition": "uncertain",
        "ripenessStatus": "uncertain", "spoilageStatus": "uncertain",
        "visualSummary": "The test image was routed to the plant report contract.",
        "visualObservations": ["Image received."], "possibleIssues": [], "precautions": ["Confirm important issues with an adviser."],
        "analysisSource": "test_double",
    }


def _crop_report(image_bytes: bytes) -> dict[str, Any]:
    kind = _kind(image_bytes)
    if kind == "soil":
        return {"_wrong_module": "This image appears to show soil. Open the Soil Analysis module."}
    if kind == "non_agricultural":
        return {"_wrong_module": "This does not appear to be an agricultural image. Upload a clear plant or produce photo."}
    name = {"flower": "Rose", "vegetable": "Brinjal", "leaf": "Plant leaf"}.get(kind, "Plant")
    return {
        "isAgricultural": True, "predictedCrop": name, "predictedCondition": "Uncertain — test-only visual screening",
        "isHealthy": False, "healthPercentage": None, "damageSeverityPercentage": None, "confidence": 0.0,
        "severityLevel": "Uncertain", "explanation": "Test report; not a real model prediction.",
        "recommendations": _recommendations(), "preventionTips": ["Take a clear follow-up photo."],
        "scientificName": None, "modelStatus": "test_double", "analysisTimestamp": _now(),
        "imageType": kind, "visibleCondition": "uncertain", "ripenessStatus": "uncertain",
        "spoilageStatus": "uncertain", "visibleObservations": ["Visible subject test sample."],
        "possibleIssues": [], "summary": "This report came from the test double.",
        "precautions": ["Confirm important issues before taking action."], "analysisProvider": "test_double",
        "limitationsDisclaimer": "Test only; no calibrated prediction was made.",
    }


def _soil_report(image_bytes: bytes) -> dict[str, Any]:
    if _kind(image_bytes) != "soil":
        return {"_wrong_module": "This image looks more like a plant than soil. Open Crop Analysis."}
    return {
        "isAgricultural": True, "predictedSoilCategory": "Uncertain from photo — soil testing recommended",
        "hindiName": "", "geography": "", "coverageIndia": "", "pHRange": "Cannot be determined from a photograph",
        "confidence": 0.0, "visualObservations": ["Brown visible surface in test sample."], "suitableCrops": ["Crop A", "Crop B", "Crop C"],
        "soilImprovementGuidance": ["Collect representative samples."], "fertilizerGuidance": ["Do not infer fertilizer dose from image."],
        "limitationsDisclaimer": "Test only. Soil chemistry needs a lab test.", "modelStatus": "test_double", "analysisTimestamp": _now(),
        "summary": "Test soil summary.", "analysisProvider": "test_double",
    }


def _identify_report(image_bytes: bytes, plant_name: str | None = None, organ: str | None = None, db: Any = None) -> dict[str, Any]:
    kind = _kind(image_bytes)
    if kind in {"soil", "non_agricultural"}:
        return {"_wrong_module": "This image does not appear to show a recognizable plant or produce. Upload a clear photo."}
    name = plant_name or {"flower": "Rose", "vegetable": "Brinjal", "leaf": "Plant"}.get(kind, "Plant")
    candidate = {"rank": 1, "plantId": None, "id": None, "scientificName": None, "commonName": name, "hindiName": "", "teluguName": "", "tamilName": "", "family": "", "category": kind.title(), "confidence": 0.0, "confidencePercentage": 0.0}
    return {
        "success": True, "mode": "name_assisted" if plant_name else "automatic", "isAgricultural": True,
        "detectedOrgan": organ or kind, "organAnalysis": {"imageType": kind, "condition": "uncertain"},
        "organHonestyNotice": "Test double; no real vision inference ran.", "isAmbiguous": True, "ambiguityMessage": "Test candidate only.",
        "inDistribution": None, "directorySearchQuery": name, "topCandidate": candidate, "candidates": [candidate],
        "normalizedEntropy": None, "savedToAccount": False, "persistenceMessage": None,
        "visualEvidence": ["Image sent to the route."], "nameAssistedAnalysis": {"providedName": plant_name, "visualCandidate": name} if plant_name else None,
        "targetedPlant": {"id": "tomato", "commonName": "Tomato", "scientificName": "Solanum lycopersicum"} if plant_name else None,
        "analysisTimestamp": _now(), "healthAssessment": {"healthStatus": "Uncertain", "healthScorePercentage": 0.0},
        "recommendations": _recommendations(), "visualCondition": "uncertain", "ripenessStatus": "uncertain", "spoilageStatus": "uncertain",
        "visualSummary": "Test image summary.", "possibleIssues": [], "precautions": ["Use field confirmation."], "analysisSource": "test_double",
    }


def _health_report(image_bytes: bytes, plant_id: str | None, plant_name: str | None, db: Any = None) -> dict[str, Any]:
    kind = _kind(image_bytes)
    return {
        "success": kind not in {"soil", "non_agricultural"}, "plantName": plant_name or "Plant",
        "healthStatus": "Uncertain / Inconclusive", "healthScorePercentage": 0.0,
        "observedSymptoms": [{"symptom": "Visual observation", "severityPercentage": 0.0, "severityLevel": "Uncertain", "description": "Test-only qualitative observation."} for _ in range(3)],
        "diseaseModelAvailable": False, "diseaseDiagnosis": None,
        "diagnosisNotice": "Test-only: no disease classifier ran.", "recommendations": _recommendations(),
        "disclaimer": "Photo-based screening is not a confirmed diagnosis.", "analysisTimestamp": _now(),
        "imageType": kind, "detectedSubject": plant_name or "Plant", "visualCondition": "uncertain",
        "ripenessStatus": "uncertain", "spoilageStatus": "uncertain", "visualSummary": "Test health summary.",
        "possibleIssues": [], "precautions": ["Confirm with a local agricultural adviser."], "analysisSource": "test_double",
    }




@pytest.fixture(scope="session", autouse=True)
def ensure_test_catalogue():
    """Prepare a clean checkout for route tests without depending on a committed DB file."""
    import importlib.util
    from pathlib import Path
    script = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap_database.py"
    spec = importlib.util.spec_from_file_location("agro_test_bootstrap", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Database bootstrap script is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.bootstrap()


@pytest.fixture(autouse=True)
def mock_local_vision_for_api_contract_tests(monkeypatch):
    """Keep API tests deterministic and independent of the local Ollama daemon."""
    try:
        import app.api.production as production_api
        import app.api.plants as plants_api
        monkeypatch.setattr(production_api, "named_plant_report", _plant_report)
        monkeypatch.setattr(production_api, "crop_report", _crop_report)
        monkeypatch.setattr(production_api, "soil_report", _soil_report)
        monkeypatch.setattr(plants_api, "identification_report", _identify_report)
        monkeypatch.setattr(plants_api, "health_report", _health_report)
    except ImportError:
        # Some isolated tests may run without loading all API modules.
        pass
