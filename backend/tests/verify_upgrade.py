import os
import sys
import io
import time
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient

# Ensure backend is on PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.main import app

client = TestClient(app)

def create_synthetic_leaf(color=(34, 139, 34)):
    img = Image.new("RGB", (256, 256), color=(240, 248, 240))
    draw = ImageDraw.Draw(img)
    draw.ellipse([50, 20, 206, 236], fill=color)
    draw.line([128, 20, 128, 236], fill=(20, 100, 20), width=3)
    for y in range(40, 220, 25):
        draw.line([128, y, 80, y - 15], fill=(20, 100, 20), width=2)
        draw.line([128, y, 176, y - 15], fill=(20, 100, 20), width=2)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_rose_flower_image():
    img = Image.new("RGB", (256, 256), color=(250, 245, 245))
    draw = ImageDraw.Draw(img)
    # Rose pink petals
    draw.ellipse([60, 60, 196, 196], fill=(220, 20, 60))
    draw.ellipse([80, 80, 176, 176], fill=(255, 105, 180))
    draw.ellipse([100, 100, 156, 156], fill=(199, 21, 133))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_tulip_flower_image():
    img = Image.new("RGB", (256, 256), color=(40, 90, 40))
    draw = ImageDraw.Draw(img)
    # Cup shaped yellow/red tulip with floral petal ratio
    draw.polygon([(128, 30), (70, 130), (128, 190), (186, 130)], fill=(230, 40, 20))
    draw.ellipse([90, 50, 166, 150], fill=(255, 120, 0))
    draw.line([128, 190, 128, 256], fill=(30, 110, 30), width=10)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_orange_fruit_image():
    img = Image.new("RGB", (256, 256), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)
    # Orange fruit
    draw.ellipse([50, 50, 206, 206], fill=(255, 140, 0))
    # Small stem / green leaf on top
    draw.ellipse([120, 30, 150, 55], fill=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_root_image():
    # Specimen with natural garden foliage background
    img = Image.new("RGB", (256, 256), color=(45, 75, 45))
    draw = ImageDraw.Draw(img)
    # Foliage and taproot
    draw.ellipse([60, 20, 196, 120], fill=(34, 139, 34))
    draw.line([128, 90, 128, 220], fill=(160, 110, 70), width=12)
    draw.line([128, 140, 70, 200], fill=(140, 90, 50), width=5)
    draw.line([128, 140, 186, 200], fill=(140, 90, 50), width=5)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def create_screenshot_image():
    img = Image.new("RGB", (400, 300), color=(240, 240, 245))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 400, 40], fill=(50, 50, 150))
    draw.rectangle([0, 40, 80, 300], fill=(30, 30, 40))
    for y in range(60, 280, 30):
        draw.line([90, y, 380, y], fill=(200, 200, 200), width=1)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def run_suite():
    print("=" * 80)
    print("AGRO AI BOTANICAL UPGRADE VERIFICATION SUITE")
    print("=" * 80)

    # 1. Catalog Scale Test
    print("\n--- 1. Botanical Directory Scale ---")
    res = client.get("/api/plants/stats")
    stats = res.json()
    print(f"Total Verified Species in DB: {stats['totalVerifiedSpecies']}")
    print(f"Target Species Goal: {stats['targetSpeciesGoal']}")
    print(f"Toxic Species Indexed: {stats['toxicOrPoisonousSpecies']}")
    assert stats["totalVerifiedSpecies"] >= 10000, "Directory does not meet 10,000+ species!"

    # 2. Autocomplete Tests
    print("\n--- 2. Google-Style Autocomplete Benchmarks ---")
    test_queries = ["tul", "ros", "corn", "oran", "vepa", "neem", "makk", "thulas"]
    for q in test_queries:
        t0 = time.time()
        res = client.get(f"/api/plants/autocomplete?q={q}&limit=5")
        dt_ms = (time.time() - t0) * 1000
        items = res.json()
        print(f"Query '{q}': {len(items)} suggestions in {dt_ms:.1f}ms")
        for item in items[:2]:
            print(f"   * {item['commonName']} ({item['scientificName']}) [Match: {item['matchSource']}] | TE: {item.get('teluguName', '')}")

    # 3. Vision Model Testing
    print("\n--- 3. Vision Model Identification & Honest Predictions ---")

    # A. Corn Leaf (In-distribution trained class)
    print("\n[TEST A] Corn / Maize Leaf (In-distribution Class):")
    corn_leaf = create_synthetic_leaf(color=(46, 139, 87))
    res = client.post("/api/plants/identify", files={"image": ("corn_leaf.jpg", corn_leaf, "image/jpeg")}, data={"organ": "leaf"})
    data = res.json()
    print(f"  Success: {data['success']}, Mode: {data['mode']}")
    print(f"  Top Candidate: {data['topCandidate']['commonName']} ({data['topCandidate']['scientificName']})")
    print(f"  Confidence: {data['topCandidate']['confidencePercentage']}%")
    print(f"  In-Distribution: {data.get('inDistribution')}, Ambiguous: {data['isAmbiguous']}")
    print(f"  Top 5 Candidates Count: {len(data['candidates'])}")

    # B. Rose Flower (Out-of-distribution class)
    print("\n[TEST B] Rose Flower (Out-of-distribution species):")
    rose_img = create_rose_flower_image()
    res = client.post("/api/plants/identify", files={"image": ("rose.jpg", rose_img, "image/jpeg")}, data={"organ": "flower"})
    data = res.json()
    print(f"  Organ Notice: {data.get('organHonestyNotice')}")
    print(f"  In-Distribution: {data.get('inDistribution')}, Ambiguous: {data['isAmbiguous']}")
    print(f"  Ambiguity Message: {data.get('ambiguityMessage')}")
    print(f"  Directory Search Fallback Query: '{data.get('directorySearchQuery')}'")

    # C. Tulip Flower (Out-of-distribution class)
    print("\n[TEST C] Tulip Flower (Out-of-distribution species):")
    tulip_img = create_tulip_flower_image()
    res = client.post("/api/plants/identify", files={"image": ("tulip.jpg", tulip_img, "image/jpeg")}, data={"organ": "flower"})
    data = res.json()
    print(f"  In-Distribution: {data.get('inDistribution')}, Ambiguous: {data['isAmbiguous']}")
    print(f"  Ambiguity Message: {data.get('ambiguityMessage')}")

    # D. Sweet Orange Fruit (Out-of-distribution class)
    print("\n[TEST D] Orange Fruit (Out-of-distribution class):")
    orange_img = create_orange_fruit_image()
    res = client.post("/api/plants/identify", files={"image": ("orange.jpg", orange_img, "image/jpeg")}, data={"organ": "fruit"})
    data = res.json()
    print(f"  Organ Notice: {data.get('organHonestyNotice')}")
    print(f"  In-Distribution: {data.get('inDistribution')}, Ambiguous: {data['isAmbiguous']}")

    # E. Underground Root
    print("\n[TEST E] Bare Root Specimen (Unsupported subterranean organ):")
    root_img = create_root_image()
    res = client.post("/api/plants/identify", files={"image": ("root.jpg", root_img, "image/jpeg")}, data={"organ": "root"})
    data = res.json()
    print(f"  Detected Organ: {data['detectedOrgan']}")
    print(f"  Organ Honesty Notice: {data.get('organHonestyNotice')}")
    print(f"  Ambiguous / Unverifiable: {data['isAmbiguous']}")

    # F. Non-Plant Screenshot
    print("\n[TEST F] Non-Plant Screenshot / UI Image (Rejection test):")
    screen_img = create_screenshot_image()
    res = client.post("/api/plants/identify", files={"image": ("screen.jpg", screen_img, "image/jpeg")})
    print(f"  Status Code: {res.status_code}")
    print(f"  Rejection Detail: {res.json()['detail']}")

    print("\n" + "=" * 80)
    print("VERIFICATION SUITE COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    run_suite()
