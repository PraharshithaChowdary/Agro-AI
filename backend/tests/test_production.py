import io
from PIL import Image
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_mock_leaf_image_bytes() -> bytes:
    """Creates an RGB image with green plant/leaf coloration."""
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_mock_rose_image_bytes() -> bytes:
    """Creates an RGB image with floral rose/pink + dark green serrated coloration."""
    img = Image.new("RGB", (224, 224), color=(34, 110, 34))
    # Add pink/crimson blossom center
    for x in range(60, 160):
        for y in range(60, 160):
            img.putpixel((x, y), (210, 60, 100))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_mock_brinjal_image_bytes() -> bytes:
    """Creates an RGB image with brinjal solanaceous violet/purple + broad leaf coloration."""
    img = Image.new("RGB", (224, 224), color=(40, 120, 50))
    # Add purple/violet stem/calyx tones
    for x in range(70, 150):
        for y in range(70, 150):
            img.putpixel((x, y), (90, 45, 115))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_mock_soil_image_bytes() -> bytes:
    """Creates an RGB image with earth/brown soil coloration."""
    img = Image.new("RGB", (224, 224), color=(110, 65, 30))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_mock_synthetic_image_bytes() -> bytes:
    """Creates an RGB image with non-agricultural neon blue/synthetic colors."""
    img = Image.new("RGB", (224, 224), color=(0, 0, 255))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_crop_analysis_valid_image():
    image_bytes = create_mock_leaf_image_bytes()
    response = client.post(
        "/api/production/crop-analysis",
        files={"image": ("leaf.jpg", image_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["isAgricultural"] is True
    assert "predictedCrop" in data
    assert "predictedCondition" in data
    assert "healthPercentage" in data
    assert "damageSeverityPercentage" in data
    assert data["confidence"] == 0.0  # uncalibrated local vision screening must not fake confidence
    assert len(data["recommendations"]) >= 4
    assert len(data["preventionTips"]) >= 1

def test_rose_identification():
    image_bytes = create_mock_rose_image_bytes()
    response = client.post(
        "/api/production/crop-analysis",
        files={"image": ("rose_sample.jpg", image_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Rose" in data["predictedCrop"]
    assert data["healthPercentage"] is None  # visual screening does not produce a calibrated percentage

def test_brinjal_identification():
    image_bytes = create_mock_brinjal_image_bytes()
    response = client.post(
        "/api/production/crop-analysis",
        files={"image": ("brinjal_sample.jpg", image_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Brinjal" in data["predictedCrop"]

def test_cross_module_soil_uploaded_to_crop_analysis():
    """
    Test that uploading a soil sample to crop-analysis rejects it and suggests soil analysis.
    """
    soil_bytes = create_mock_soil_image_bytes()
    response = client.post(
        "/api/production/crop-analysis",
        files={"image": ("soil_photo.jpg", soil_bytes, "image/jpeg")}
    )
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert "Soil sample" in detail or "Soil Analysis" in detail

def test_cross_module_leaf_uploaded_to_soil_analysis():
    """
    Test that uploading a crop/leaf image to soil-analysis rejects it and suggests crop analysis.
    """
    leaf_bytes = create_mock_leaf_image_bytes()
    response = client.post(
        "/api/production/soil-analysis",
        files={"image": ("plant_leaf.jpg", leaf_bytes, "image/jpeg")}
    )
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert "Crop" in detail or "Plant Leaf" in detail or "Crop Analysis" in detail

def test_soil_analysis_valid_image():
    image_bytes = create_mock_soil_image_bytes()
    response = client.post(
        "/api/production/soil-analysis",
        files={"image": ("soil.jpg", image_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["isAgricultural"] is True
    assert "predictedSoilCategory" in data
    assert len(data["suitableCrops"]) >= 3
    assert "limitationsDisclaimer" in data

def test_non_agricultural_image_rejection():
    image_bytes = create_mock_synthetic_image_bytes()
    response = client.post(
        "/api/production/crop-analysis",
        files={"image": ("unrelated.jpg", image_bytes, "image/jpeg")}
    )
    assert response.status_code == 400
    assert "Invalid Image" in response.json()["detail"] or "Uncertain" in response.json()["detail"]

def test_malformed_image_handling():
    corrupt_bytes = b"NOT_A_REAL_IMAGE_DATA_CORRUPT_BYTES"
    response = client.post(
        "/api/production/crop-analysis",
        files={"image": ("corrupt.jpg", corrupt_bytes, "image/jpeg")}
    )
    assert response.status_code == 400
    assert "Malformed" in response.json()["detail"] or "Invalid" in response.json()["detail"]

def test_production_history_requires_authentication():
    response = client.get("/api/production/history")
    assert response.status_code == 401

def test_get_supported_plants_endpoint():
    response = client.get("/api/production/supported-plants")
    assert response.status_code == 200
    plants = response.json()
    assert len(plants) >= 15
    sample = plants[0]
    assert "name" in sample
    assert "scientificName" in sample
    assert "diseaseModelAvailable" in sample

def test_analyze_named_plant_trained_species():
    image_bytes = create_mock_leaf_image_bytes()
    response = client.post(
        "/api/production/analyze-named-plant",
        data={
            "plant_name": "Tomato",
            "crop_type": "Vegetable",
            "growing_location": "Greenhouse"
        },
        files={"image": ("tomato_leaf.jpg", image_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["isPlantImage"] is True
    assert "Tomato" in data["userPlantName"]
    assert data["diseaseModelAvailable"] is False  # no validated disease classifier used by local vision route
    assert len(data["observedSymptoms"]) >= 4
    assert "careGuide" in data
    assert len(data["recommendations"]) >= 4

def test_analyze_named_plant_untrained_species():
    image_bytes = create_mock_leaf_image_bytes()
    response = client.post(
        "/api/production/analyze-named-plant",
        data={
            "plant_name": "Monstera",
            "crop_type": "Houseplant",
            "growing_location": "Indoor Potted"
        },
        files={"image": ("monstera_leaf.jpg", image_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["isPlantImage"] is True
    assert data["userPlantName"] == "Monstera / Swiss Cheese Plant"
    assert data["diseaseModelAvailable"] is False
    assert "careGuide" in data
    assert "watering" in data["careGuide"]
    assert len(data["recommendations"]) >= 4

def test_analyze_named_plant_non_agri_rejection():
    synth_bytes = create_mock_synthetic_image_bytes()
    response = client.post(
        "/api/production/analyze-named-plant",
        data={"plant_name": "Tomato"},
        files={"image": ("screen.jpg", synth_bytes, "image/jpeg")}
    )
    assert response.status_code == 400
    assert "does not appear to contain" in response.json()["detail"] or "Invalid" in response.json()["detail"]

