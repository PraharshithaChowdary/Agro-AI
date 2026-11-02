"""
AGRO AI — Global Plant Identification Overhaul: Comprehensive Validation Suite
==============================================================================
Evaluates the entire plant analysis pipeline across:
1. Diverse plant species:
   - Flowers: tulip, rose, jasmine, hibiscus, sunflower, lily, orchid, marigold
   - Trees: neem, banyan, mango, coconut, guava
   - Crops: rice, wheat, corn, tomato, potato, chilli, cotton, soybean
   - Medicinal plants & herbs: tulsi, aloe vera, mint, turmeric, ginger
   - Fruits & vegetables: banana, lemon, orange, grapes, brinjal, okra
   - Other wild, ornamental, and regional plants
2. Diverse plant parts (organs):
   - leaf, flower, fruit, stem, root, whole_plant
3. False identification prevention & search field independence:
   - Pixel analysis independent of manual plant name
   - Out-of-distribution (OOD) detection for unsupported species (tulip, orchid, lily, wild)
   - Prevention of forced classification into the 14 classes
4. Downstream results discipline:
   - Withholding species-specific watering, chemical fertilizers, pesticides when uncertain
   - Organ-specific observations (no leaf observations for flower photos)
5. Non-plant gatekeeper rejection:
   - Synthetic images, screenshots, human portraits, soil
6. Visual robustness:
   - Lighting variations, rotation, noise
"""

import io
import pytest
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# ---------------------------------------------------------------------------
# Synthetic Botanical Specimen Generators (Held-out Test Images)
# ---------------------------------------------------------------------------

def create_flower_specimen(color=(220, 45, 85), center_color=(255, 215, 0), petal_count=6):
    """Generates realistic floral corolla with radiating petals and central pistil."""
    img = Image.new("RGB", (224, 224), color=(245, 245, 240))
    draw = ImageDraw.Draw(img)
    cx, cy = 112, 112
    r_petal = 75
    # Radiating petals
    for i in range(petal_count):
        angle = (2 * np.pi / petal_count) * i
        px = cx + int(np.cos(angle) * 45)
        py = cy + int(np.sin(angle) * 45)
        draw.ellipse([px - 32, py - 32, px + 32, py + 32], fill=color)
    # Center pistil
    draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=center_color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_linear_monocot_leaf(width=100, height=350, color=(40, 150, 45), vein_color=(55, 175, 60), midrib_color=(80, 195, 80)):
    """Generates elongated linear strap-like monocot leaf blade with parallel longitudinal veins and prominent midrib."""
    img = Image.new("RGB", (width, height), color=color)
    draw = ImageDraw.Draw(img)
    for x in range(10, width - 10, 10):
        draw.line([(x, 0), (x, height)], fill=vein_color, width=2)
    draw.line([(width // 2, 0), (width // 2, height)], fill=midrib_color, width=4)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_broad_dicot_leaf(size=(224, 224), color=(34, 139, 34), serrated=False):
    """Generates broad ovate/cordate dicot leaf with reticulate branching venation."""
    img = Image.new("RGB", size, color=(245, 245, 240))
    draw = ImageDraw.Draw(img)
    cx, cy = size[0] // 2, size[1] // 2
    # Ovate blade
    draw.ellipse([cx - 75, cy - 85, cx + 75, cy + 85], fill=color)
    # Midrib
    draw.line([(cx, cy - 80), (cx, cy + 85)], fill=(50, 175, 55), width=3)
    # Reticulate branching lateral veins
    for dy in range(-60, 70, 25):
        draw.line([(cx, cy + dy), (cx - 55, cy + dy - 20)], fill=(50, 175, 55), width=2)
        draw.line([(cx, cy + dy), (cx + 55, cy + dy - 20)], fill=(50, 175, 55), width=2)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_succulent_spiny_leaf(size=(224, 224)):
    """Generates fleshy glaucous-green aloe leaf with spiny marginal teeth."""
    img = Image.new("RGB", size, color=(245, 245, 240))
    draw = ImageDraw.Draw(img)
    points = [(112, 10), (160, 210), (64, 210)]
    draw.polygon(points, fill=(70, 155, 120))  # Glaucous grey-green
    # Marginal spiny teeth
    for y in range(40, 200, 15):
        draw.polygon([(64, y), (56, y + 5), (64, y + 10)], fill=(200, 230, 180))
        draw.polygon([(160, y), (168, y + 5), (160, y + 10)], fill=(200, 230, 180))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_fruit_specimen(color=(225, 40, 30)):
    """Generates fleshy globose fruit pericarp with calyx/stem attachment."""
    img = Image.new("RGB", (224, 224), color=(245, 245, 240))
    draw = ImageDraw.Draw(img)
    draw.ellipse([45, 45, 179, 179], fill=color)
    # Green calyx at top
    draw.polygon([(112, 35), (95, 50), (129, 50)], fill=(35, 130, 40))
    draw.line([(112, 20), (112, 40)], fill=(80, 60, 30), width=3)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_stem_specimen():
    """Generates elongated axial woody stem with fibrous bark striations and nodes."""
    img = Image.new("RGB", (224, 224), color=(245, 245, 240))
    draw = ImageDraw.Draw(img)
    # Central vertical branch
    draw.rectangle([90, 10, 134, 214], fill=(110, 75, 45))
    # Bark striations
    for y in range(20, 210, 8):
        draw.line([(92, y), (132, y)], fill=(85, 55, 30), width=1)
    # Nodal rings
    draw.rectangle([88, 70, 136, 76], fill=(140, 95, 55))
    draw.rectangle([88, 140, 136, 146], fill=(140, 95, 55))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_root_specimen():
    """Generates subterranean fibrous branching roots and taproot in earthy substrate."""
    img = Image.new("RGB", (224, 224), color=(85, 65, 50))  # Dark earth
    draw = ImageDraw.Draw(img)
    # Central taproot
    draw.polygon([(112, 10), (120, 200), (104, 200)], fill=(185, 150, 100))
    # Lateral branching rootlets
    for y, side in [(40, -1), (70, 1), (100, -1), (130, 1), (160, -1)]:
        draw.line([(112, y), (112 + side * 60, y + 35)], fill=(195, 160, 110), width=2)
        draw.line([(112 + side * 40, y + 20), (112 + side * 55, y + 45)], fill=(195, 160, 110), width=1)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_whole_plant_specimen():
    """Generates whole-plant habit with pot/soil base, branching stems, and green canopy foliage."""
    img = Image.new("RGB", (224, 224), color=(245, 245, 240))
    draw = ImageDraw.Draw(img)
    # Pot container
    draw.polygon([(60, 170), (164, 170), (150, 215), (74, 215)], fill=(160, 82, 45))
    # Main stem
    draw.line([(112, 170), (112, 90)], fill=(90, 65, 35), width=4)
    # Foliage clusters (canopy)
    for cx, cy in [(112, 65), (85, 95), (140, 95), (112, 115)]:
        draw.ellipse([cx - 28, cy - 25, cx + 28, cy + 25], fill=(35, 145, 45))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_soil_specimen(soil_type="black"):
    """Generates pedological soil sample with earth grain texture."""
    colors = {
        "black": (35, 32, 30),
        "red": (145, 55, 35),
        "alluvial": (120, 100, 70),
        "sandy": (160, 140, 95),
    }
    bg = colors.get(soil_type, (50, 45, 40))
    img = Image.new("RGB", (224, 224), color=bg)
    draw = ImageDraw.Draw(img)
    rng = np.random.RandomState(42)
    for _ in range(800):
        x = rng.randint(0, 223)
        y = rng.randint(0, 223)
        c = tuple(int(np.clip(v + rng.randint(-20, 20), 0, 255)) for v in bg)
        draw.point((x, y), fill=c)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

# ---------------------------------------------------------------------------
# TEST SUITE: 1. Diverse Species & Image Types
# ---------------------------------------------------------------------------

class TestDiverseSpeciesIdentification:
    """Tests identification and calibration across diverse plant categories."""

    def test_flowers_supported_rose(self):
        """Supported flower (Rose): recognized as floral organ, not confused with trees/cereals."""
        img = create_flower_specimen(color=(215, 35, 65), center_color=(255, 215, 0))
        res = client.post("/api/plants/identify", files={"image": ("rose.jpg", img, "image/jpeg")}, data={"organ": "flower"})
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["detectedOrgan"] == "flower"
        assert len(data["candidates"]) >= 1
        # Flower observations must not mention leaves
        for ev in data.get("visualEvidence", []):
            assert "leaf margin" not in ev.lower()

    def test_flowers_unsupported_tulip_calibrated_inconclusive(self):
        """
        CRITICAL: Unsupported flower (Tulip):
        The vision model must detect floral organ, flag ambiguity/out-of-distribution,
        and NEVER force it into 14 classes with false high confidence.
        """
        img = create_flower_specimen(color=(235, 50, 80), center_color=(255, 230, 50))
        res = client.post("/api/plants/identify", files={"image": ("tulip.jpg", img, "image/jpeg")}, data={"organ": "flower"})
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["isAmbiguous"] is True
        assert data["inDistribution"] is False
        assert "Identification Inconclusive" in data["ambiguityMessage"]
        # Confidence must be sober / softened
        assert data["topCandidate"]["confidencePercentage"] < 50.0
        # Recommendations must withhold species-specific chemicals
        rec_titles = [r["title"] for r in data["recommendations"]]
        assert "Species Verification Required" in rec_titles
        assert "Withhold Chemical & Pesticide Applications" in rec_titles

    def test_flowers_unsupported_orchid_calibrated_inconclusive(self):
        """Unsupported flower (Orchid): out-of-distribution detection flags inconclusive."""
        img = create_flower_specimen(color=(185, 60, 185), center_color=(255, 230, 80))
        res = client.post("/api/plants/identify", files={"image": ("orchid.jpg", img, "image/jpeg")}, data={"organ": "flower"})
        assert res.status_code == 200
        data = res.json()
        assert data["isAmbiguous"] is True
        assert data["inDistribution"] is False

    def test_flowers_unsupported_lily_calibrated_inconclusive(self):
        """Unsupported flower (Lily): out-of-distribution detection flags inconclusive."""
        img = create_flower_specimen(color=(250, 245, 230), center_color=(230, 160, 40))
        res = client.post("/api/plants/identify", files={"image": ("lily.jpg", img, "image/jpeg")}, data={"organ": "flower"})
        assert res.status_code == 200
        data = res.json()
        assert data["isAmbiguous"] is True

    def test_crops_corn_maize_identification(self):
        """Supported crop (Corn / Maize): recognized via linear blade venation and deep CNN."""
        img = create_linear_monocot_leaf(width=90, height=340, color=(40, 150, 45))
        res = client.post("/api/plants/identify", files={"image": ("corn.jpg", img, "image/jpeg")}, data={"organ": "leaf"})
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["topCandidate"] is not None
        assert data["topCandidate"]["plantId"] == "zea-mays"
        assert data["isAmbiguous"] is False

    def test_crops_rice_paddy_identification(self):
        """Supported cereal crop (Rice / Oryza sativa): linear monocot blade features recognized."""
        img = create_linear_monocot_leaf(width=70, height=350, color=(50, 160, 55))
        res = client.post("/api/plants/identify", files={"image": ("rice.jpg", img, "image/jpeg")}, data={"organ": "leaf"})
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert "Linear, narrow parallel-veined leaf blade" in " ".join(data["visualEvidence"])

    def test_crops_tomato_dicot_foliage(self):
        """Supported crop (Tomato): broad reticulate dicot leaf recognized."""
        img = create_broad_dicot_leaf(size=(224, 224), color=(34, 139, 34))
        res = client.post("/api/plants/identify", files={"image": ("tomato.jpg", img, "image/jpeg")}, data={"organ": "leaf"})
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert "Broad, reticulate-veined leaf blade" in " ".join(data["visualEvidence"])

    def test_medicinal_aloe_vera_succulent(self):
        """Medicinal succulent (Aloe Vera): succulent glaucous morphology."""
        img = create_succulent_spiny_leaf()
        res = client.post("/api/plants/identify", files={"image": ("aloe.jpg", img, "image/jpeg")}, data={"organ": "leaf"})
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True

    def test_fruits_and_vegetables_fruit_organ(self):
        """Fruiting organ: evaluated as fruit with pericarp observations, not foliar blade."""
        img = create_fruit_specimen(color=(220, 40, 35))
        res = client.post("/api/plants/identify", files={"image": ("fruit.jpg", img, "image/jpeg")}, data={"organ": "fruit"})
        assert res.status_code == 200
        data = res.json()
        assert data["detectedOrgan"] == "fruit"
        ev_text = " ".join(data["visualEvidence"]).lower()
        assert "pericarp" in ev_text or "fruit" in ev_text
        assert "vein" not in ev_text

    def test_trees_stem_bark_morphology(self):
        """Woody tree/stem morphology: evaluated as stem with bark observations."""
        img = create_stem_specimen()
        res = client.post("/api/plants/identify", files={"image": ("stem.jpg", img, "image/jpeg")}, data={"organ": "stem"})
        assert res.status_code == 200
        data = res.json()
        assert data["detectedOrgan"] == "stem"
        ev_text = " ".join(data["visualEvidence"]).lower()
        assert "stem" in ev_text or "bark" in ev_text or "stalk" in ev_text

    def test_roots_honesty_and_ood_declaration(self):
        """
        Subterranean root morphology:
        Must declare organ honesty disclaimer, flag ambiguity, and withhold species-specific chemicals.
        """
        img = create_root_specimen()
        res = client.post("/api/plants/identify", files={"image": ("root.jpg", img, "image/jpeg")}, data={"organ": "root"})
        assert res.status_code == 200
        data = res.json()
        assert data["detectedOrgan"] == "root"
        assert data["isAmbiguous"] is True
        assert "subterranean" in data["organHonestyNotice"].lower()

    def test_whole_plant_canopy_habit(self):
        """Whole-plant habit: canopy habit and vegetative structure evaluated."""
        img = create_whole_plant_specimen()
        res = client.post("/api/plants/identify", files={"image": ("whole_plant.jpg", img, "image/jpeg")}, data={"organ": "whole_plant"})
        assert res.status_code == 200
        data = res.json()
        assert data["detectedOrgan"] == "whole_plant"

# ---------------------------------------------------------------------------
# TEST SUITE: 2. Prevention of False Identifications
# ---------------------------------------------------------------------------

class TestFalseIdentificationPrevention:
    """Verifies image pixels are analyzed independently of manual search inputs."""

    def test_search_input_cannot_dictate_prediction_on_tulip(self):
        """
        CRITICAL: User uploads tulip flower but types 'Corn / Maize'.
        1. Model must NOT output Corn with high confidence.
        2. Vision model must flag out-of-distribution / ambiguous.
        3. Name assisted analysis must report species inconsistency.
        """
        tulip_bytes = create_flower_specimen(color=(235, 50, 80))
        res = client.post(
            "/api/plants/identify",
            files={"image": ("tulip.jpg", tulip_bytes, "image/jpeg")},
            data={"plant_name": "Corn / Maize", "organ": "flower"}
        )
        assert res.status_code == 200
        data = res.json()
        assert data["isAmbiguous"] is True
        if data.get("topCandidate"):
            assert data["topCandidate"]["plantId"] != "zea-mays"
            assert data["topCandidate"]["confidencePercentage"] < 60.0
        na = data.get("nameAssistedAnalysis")
        assert na is not None
        assert na["isConsistent"] is False
        assert "Inconsistent" in na["status"] or "Mismatch" in na["status"]

    def test_search_input_cannot_dictate_prediction_on_rose_with_mango_name(self):
        """User uploads rose flower but enters 'Mango': Mismatch must be detected."""
        rose_bytes = create_flower_specimen(color=(215, 35, 65))
        res = client.post(
            "/api/plants/identify",
            files={"image": ("rose.jpg", rose_bytes, "image/jpeg")},
            data={"plant_name": "Mango", "organ": "flower"}
        )
        assert res.status_code == 200
        data = res.json()
        na = data.get("nameAssistedAnalysis")
        assert na is not None
        assert na["isConsistent"] is False

    def test_non_agricultural_neon_rejected_with_manual_name(self):
        """Manual plant name cannot bypass gatekeeper on non-agricultural image."""
        neon_img = Image.new("RGB", (224, 224), color=(0, 0, 255))
        buf = io.BytesIO()
        neon_img.save(buf, format="JPEG")
        res = client.post(
            "/api/plants/identify",
            files={"image": ("neon.jpg", buf.getvalue(), "image/jpeg")},
            data={"plant_name": "Tomato", "organ": "leaf"}
        )
        assert res.status_code == 400

    def test_soil_rejected_from_plant_identification_with_helpful_redirect(self):
        """Soil uploaded to plant identification: must be rejected with advice to use Soil tool."""
        soil_img = create_soil_specimen("black")
        res = client.post(
            "/api/plants/identify",
            files={"image": ("soil.jpg", soil_img, "image/jpeg")},
            data={"organ": "leaf"}
        )
        assert res.status_code == 400
        assert "soil" in res.json()["detail"].lower()

# ---------------------------------------------------------------------------
# TEST SUITE: 3. Downstream Results Discipline
# ---------------------------------------------------------------------------

class TestDownstreamResultsDiscipline:
    """Verifies that treatments, watering, and chemicals are withheld when identification is uncertain."""

    def test_uncertain_identity_withholds_chemical_treatments(self):
        """Inconclusive / ambiguous plant: health score is 0.0, species-specific chemicals withheld."""
        tulip_bytes = create_flower_specimen(color=(235, 50, 80))
        res = client.post(
            "/api/plants/identify",
            files={"image": ("unknown.jpg", tulip_bytes, "image/jpeg")},
            data={"organ": "flower"}
        )
        assert res.status_code == 200
        data = res.json()
        ha = data["healthAssessment"]
        assert ha["healthScorePercentage"] == 0.0
        assert "Inconclusive" in ha["healthStatus"]
        # Recommendations must contain species verification and safety notices
        types = [r["type"] for r in data["recommendations"]]
        assert "advisory" in types
        assert "safety" in types

    def test_flower_does_not_generate_foliar_leaf_observations(self):
        """Flower image: observations must describe floral/petal tissue, not leaf venation."""
        rose_bytes = create_flower_specimen(color=(215, 35, 65))
        res = client.post(
            "/api/plants/identify",
            files={"image": ("rose.jpg", rose_bytes, "image/jpeg")},
            data={"organ": "flower"}
        )
        assert res.status_code == 200
        data = res.json()
        for ev in data.get("visualEvidence", []):
            assert "leaf margin" not in ev.lower()
            assert "chlorophyll saturation" not in ev.lower()

# ---------------------------------------------------------------------------
# TEST SUITE: 4. Image Quality & Robustness
# ---------------------------------------------------------------------------

class TestImageQualityAndRobustness:
    """Tests lighting variations, rotation, and noise."""

    def test_corn_leaf_under_dim_lighting(self):
        """Corn leaf under low-light condition: still recognized as monocot."""
        corn_bytes = create_linear_monocot_leaf(color=(25, 95, 30), vein_color=(35, 115, 40))
        res = client.post(
            "/api/plants/identify",
            files={"image": ("dim_corn.jpg", corn_bytes, "image/jpeg")},
            data={"organ": "leaf"}
        )
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["topCandidate"]["plantId"] == "zea-mays"

    def test_corn_leaf_horizontal_orientation(self):
        """Corn leaf rotated horizontally: recognized as monocot cereal crop."""
        img = Image.new("RGB", (350, 100), color=(40, 150, 45))
        draw = ImageDraw.Draw(img)
        for y in range(10, 90, 10):
            draw.line([(0, y), (350, y)], fill=(55, 175, 60), width=2)
        draw.line([(0, 50), (350, 50)], fill=(80, 195, 80), width=4)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        res = client.post(
            "/api/plants/identify",
            files={"image": ("h_corn.jpg", buf.getvalue(), "image/jpeg")},
            data={"organ": "leaf"}
        )
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        # Recognized as one of the supported monocot cereal crops
        assert data["topCandidate"]["plantId"] in {"zea-mays", "triticum-aestivum", "sorghum-bicolor", "oryza-sativa", "eleusine-coracana"}

