import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_mock_leaf_image_bytes():
    """Creates a synthetic green foliage image in memory."""
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    # Add subtle variations
    for x in range(50, 170):
        for y in range(50, 170):
            img.putpixel((x, y), (46, 160, 60))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_mock_synthetic_image_bytes():
    """Creates a non-agricultural uniform neon blue synthetic image."""
    img = Image.new("RGB", (224, 224), color=(0, 0, 255))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_mock_tulip_flower_image_bytes():
    """Creates a vibrant crimson/rose floral image with petal structures."""
    img = Image.new("RGB", (224, 224), color=(220, 45, 85))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.ellipse([30, 20, 194, 204], fill=(240, 50, 95))
    draw.ellipse([80, 75, 144, 149], fill=(255, 210, 40)) # Yellow pistil
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_mock_corn_leaf_image_bytes():
    """Creates an elongated linear strap-like monocot leaf with parallel veins."""
    img = Image.new("RGB", (100, 350), color=(40, 150, 45))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    for x in range(10, 90, 10):
        draw.line([(x, 0), (x, 350)], fill=(55, 175, 60), width=2)
    draw.line([(50, 0), (50, 350)], fill=(80, 195, 80), width=4) # midrib
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_get_plant_categories():
    response = client.get("/api/plants/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    categories = [c["category"] for c in data]
    assert "crop" in categories
    assert "vegetable" in categories
    assert "fruit plant" in categories

def test_get_plant_stats():
    response = client.get("/api/plants/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["totalVerifiedSpecies"] >= 90
    assert data["targetSpeciesGoal"] == 10000

def test_search_plants_pagination():
    response = client.get("/api/plants/search?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 90
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["items"]) == 10

def test_search_plants_by_common_name():
    response = client.get("/api/plants/search?q=Mango")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    found = any("Mango" in p["commonName"] for p in data["items"])
    assert found

def test_search_plants_by_scientific_name():
    response = client.get("/api/plants/search?q=Oryza sativa")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert data["items"][0]["scientificName"] == "Oryza sativa"

def test_search_plants_by_telugu_name():
    response = client.get("/api/plants/search?q=వరి")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert "Vari" in data["items"][0]["teluguName"] or "వరి" in data["items"][0]["teluguName"]

def test_search_plants_by_tamil_name():
    response = client.get("/api/plants/search?q=நெல்")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert "Nel" in data["items"][0]["tamilName"] or "நெல்" in data["items"][0]["tamilName"]

def test_search_plants_by_hindi_name():
    response = client.get("/api/plants/search?q=गेहूं")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert "Gehun" in data["items"][0]["hindiName"] or "गेहूं" in data["items"][0]["hindiName"]

def test_search_plants_filter_category():
    response = client.get("/api/plants/search?category=vegetable")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 15
    for item in data["items"]:
        assert item["category"] == "vegetable"

def test_get_plant_details_valid():
    response = client.get("/api/plants/mangifera-indica")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "mangifera-indica"
    assert data["scientificName"] == "Mangifera indica"
    assert data["family"] == "Anacardiaceae"
    assert "leafCharacteristics" in data
    assert "growingSeason" in data
    assert len(data["uses"]) >= 1

def test_get_plant_details_not_found():
    response = client.get("/api/plants/unknown-fictional-species")
    assert response.status_code == 404

def test_identify_plant_mode_a_automatic():
    img_bytes = create_mock_leaf_image_bytes()
    response = client.post(
        "/api/plants/identify",
        files={"image": ("foliage.jpg", img_bytes, "image/jpeg")},
        data={"organ": "leaf"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["mode"] == "automatic"
    assert data["isAgricultural"] is True
    assert "visualEvidence" in data
    assert len(data["visualEvidence"]) >= 1
    assert "healthAssessment" in data
    assert "recommendations" in data
    assert data["topCandidate"] is not None
    assert len(data["candidates"]) >= 1
    assert "confidencePercentage" in data["topCandidate"]
    assert data["topCandidate"]["confidencePercentage"] == 0.0  # no calibrated probability from generic vision

def test_identify_plant_mode_b_name_assisted():
    img_bytes = create_mock_leaf_image_bytes()
    response = client.post(
        "/api/plants/identify",
        files={"image": ("foliage.jpg", img_bytes, "image/jpeg")},
        data={"plant_name": "Tomato", "organ": "leaf"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["mode"] == "name_assisted"
    assert "nameAssistedAnalysis" in data
    assert "targetedPlant" in data
    assert data["targetedPlant"] is not None

def test_identify_plant_non_agricultural_rejection():
    synth_bytes = create_mock_synthetic_image_bytes()
    response = client.post(
        "/api/plants/identify",
        files={"image": ("synthetic.jpg", synth_bytes, "image/jpeg")}
    )
    assert response.status_code == 400
    assert "agricultural" in response.json()["detail"].lower() or "plant" in response.json()["detail"].lower()

def test_identify_plant_screenshot_rejection():
    # Simulate digital UI / calendar / web screenshot
    img = Image.new("RGB", (600, 450), color=(248, 250, 252))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 600, 50], fill=(79, 70, 229)) # Purple header
    draw.rectangle([0, 50, 120, 450], fill=(30, 41, 59)) # Dark sidebar
    for y in range(80, 450, 40):
        draw.line([(120, y), (600, y)], fill=(226, 232, 240), width=1)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    screenshot_bytes = buf.getvalue()

    response = client.post(
        "/api/plants/identify",
        files={"image": ("screenshot.jpg", screenshot_bytes, "image/jpeg")}
    )
    assert response.status_code == 400
    detail = response.json()["detail"].lower()
    # Must reject as screenshot / non-agricultural, NOT as soil!
    assert "plant" in detail or "agricultural" in detail or "photo" in detail
    assert "contain soil" not in detail

def test_identify_plant_all_organs():
    leaf_bytes = create_mock_leaf_image_bytes()
    for org in ["leaf", "flower", "fruit", "stem", "root", "whole_plant"]:
        res = client.post(
            "/api/plants/identify",
            files={"image": ("specimen.jpg", leaf_bytes, "image/jpeg")},
            data={"organ": org}
        )
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["detectedOrgan"] == org  # route contract in the deterministic API test double
        assert "organAnalysis" in data

def test_analyze_plant_health():
    img_bytes = create_mock_leaf_image_bytes()
    response = client.post(
        "/api/plants/analyze-health",
        files={"image": ("tomato_leaf.jpg", img_bytes, "image/jpeg")},
        data={"plant_name": "Tomato"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "healthStatus" in data
    assert "healthScorePercentage" in data
    assert len(data["observedSymptoms"]) == 3
    assert len(data["recommendations"]) >= 4

def test_autocomplete_plants():
    # Test partial English prefix
    res1 = client.get("/api/plants/autocomplete?q=tul&limit=5")
    assert res1.status_code == 200
    items1 = res1.json()
    assert len(items1) > 0
    names1 = [i["commonName"].lower() + i["scientificName"].lower() for i in items1]
    assert any("tul" in n for n in names1)

    # Test Telugu regional name match
    res2 = client.get("/api/plants/autocomplete?q=vepa&limit=5")
    assert res2.status_code == 200
    items2 = res2.json()
    assert len(items2) > 0

    # Test scientific name match
    res3 = client.get("/api/plants/autocomplete?q=rosa&limit=5")
    assert res3.status_code == 200
    items3 = res3.json()
    assert len(items3) > 0

def test_plant_directory_scale():
    res = client.get("/api/plants/stats")
    assert res.status_code == 200
    stats = res.json()
    assert stats["totalVerifiedSpecies"] >= 10000

def test_identify_plant_organ_honesty_and_ood():
    leaf_bytes = create_mock_leaf_image_bytes()
    res = client.post(
        "/api/plants/identify",
        files={"image": ("specimen.jpg", leaf_bytes, "image/jpeg")},
        data={"organ": "root"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "organHonestyNotice" in data
    assert "root" in data["organHonestyNotice"].lower()
    # Underground root should be flagged as ambiguous / out-of-distribution
    assert data["isAmbiguous"] is True
    assert data["inDistribution"] is False
    assert "directorySearchQuery" in data

def test_regression_tulip_photo_with_entered_corn_name():
    """
    CRITICAL REGRESSION TEST:
    Uploading a tulip flower photo while entering 'Corn / Maize' must NEVER:
    1. Output Corn at 95% confidence.
    2. Overwrite the image prediction with user-entered name.
    3. Falsely report 'Morphological Check: Consistent'.
    It MUST flag ambiguity and report species inconsistency.
    """
    tulip_bytes = create_mock_tulip_flower_image_bytes()
    response = client.post(
        "/api/plants/identify",
        files={"image": ("tulip.jpg", tulip_bytes, "image/jpeg")},
        data={"plant_name": "Corn / Maize", "organ": "flower"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["mode"] == "name_assisted"

    # Vision model must independently flag floral / out-of-distribution
    assert data["isAmbiguous"] is True

    # User entered name must NOT overwrite topCandidate as Corn with 95%
    if data.get("topCandidate"):
        assert data["topCandidate"]["plantId"] != "zea-mays"
        assert data["topCandidate"]["confidencePercentage"] < 60.0

    # Cross-check must detect inconsistency and warn
    na = data.get("nameAssistedAnalysis")
    assert na is not None
    assert na["isConsistent"] is False
    assert "Inconsistent" in na["status"] or "Mismatch" in na["status"] or "Uncertain" in na["status"]

def test_regression_corn_photo_with_entered_corn_name():
    """
    REGRESSION TEST:
    Uploading a real corn leaf photo while entering 'Corn / Maize':
    Must independently identify zea-mays with high confidence and report consistency.
    """
    corn_bytes = create_mock_corn_leaf_image_bytes()
    response = client.post(
        "/api/plants/identify",
        files={"image": ("corn_leaf.jpg", corn_bytes, "image/jpeg")},
        data={"plant_name": "Corn / Maize", "organ": "leaf"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["mode"] == "name_assisted"
    assert data["topCandidate"] is not None
    assert data["topCandidate"]["plantId"] == "zea-mays"

    na = data.get("nameAssistedAnalysis")
    assert na is not None
    assert na["isConsistent"] is True
    assert "Consistent" in na["status"]

def test_regression_unrelated_photo_with_entered_corn_name():
    """
    REGRESSION TEST:
    Uploading an unrelated / synthetic non-agricultural photo with entered 'Corn / Maize' name:
    Must be rejected with HTTP 400. The manual name must NOT bypass gatekeeping.
    """
    synth_bytes = create_mock_synthetic_image_bytes()
    response = client.post(
        "/api/plants/identify",
        files={"image": ("unrelated_neon.jpg", synth_bytes, "image/jpeg")},
        data={"plant_name": "Corn / Maize", "organ": "leaf"}
    )
    assert response.status_code == 400
    assert "agricultural" in response.json()["detail"].lower() or "plant" in response.json()["detail"].lower()

def test_regression_supported_plant_photo_without_manual_name():
    """
    REGRESSION TEST:
    Mode A (Automatic): Uploading a supported plant photo without any manual name:
    Must run automatic identification without nameAssistedAnalysis.
    """
    corn_bytes = create_mock_corn_leaf_image_bytes()
    response = client.post(
        "/api/plants/identify",
        files={"image": ("corn.jpg", corn_bytes, "image/jpeg")},
        data={"organ": "leaf"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["mode"] == "automatic"
    assert data["nameAssistedAnalysis"] is None
    assert data["topCandidate"] is not None
    assert data["topCandidate"]["plantId"] == "zea-mays"


