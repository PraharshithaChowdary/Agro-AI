import io
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageDraw
import numpy as np
from app.ml.preprocessing import extract_botanical_feature_vector, extract_visual_color_features
from app.ml.model_loader import model_registry
from app.services.crop_inference import CropInferenceService, EXPANDED_CROP_KNOWLEDGE_BASE
from app.services.soil_inference import SoilInferenceService
from app.services.image_validation import AgriculturalRelevanceService

def create_mock_leaf_image(leaf_type: str) -> bytes:
    img = Image.new("RGB", (256, 256), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    if leaf_type == "rose_green_leaf":
        # Dark emerald green rose leaf with fine serrations
        # Dicot compound shape
        draw.ellipse([60, 40, 190, 210], fill=(30, 120, 45), outline=(15, 80, 25))
        # Draw some sharp serration teeth along the border
        for y in range(50, 200, 8):
            draw.polygon([(55, y), (65, y+4), (60, y+8)], fill=(25, 110, 40))
            draw.polygon([(195, y), (185, y+4), (190, y+8)], fill=(25, 110, 40))
        # Fine reticulate veins
        draw.line([125, 45, 125, 205], fill=(45, 145, 60), width=2)
        for y in range(70, 190, 20):
            draw.line([125, y, 80, y-15], fill=(40, 135, 55), width=1)
            draw.line([125, y, 170, y-15], fill=(40, 135, 55), width=1)
            
    elif leaf_type == "rose_black_spot":
        draw.ellipse([60, 40, 190, 210], fill=(35, 115, 45), outline=(15, 80, 25))
        # Black spots with yellow halo
        draw.ellipse([90, 90, 130, 130], fill=(180, 160, 30))
        draw.ellipse([98, 98, 122, 122], fill=(25, 20, 15))
        draw.ellipse([140, 130, 175, 165], fill=(180, 160, 30))
        draw.ellipse([148, 138, 168, 158], fill=(20, 15, 10))

    elif leaf_type == "brinjal_leaf":
        # Broad fuzzy ovate leaf with slight violet vein tinge
        draw.ellipse([40, 30, 216, 226], fill=(55, 125, 65))
        draw.line([128, 35, 128, 220], fill=(110, 85, 120), width=3) # Purple midrib
        draw.line([128, 80, 60, 60], fill=(95, 75, 110), width=2)
        draw.line([128, 80, 195, 60], fill=(95, 75, 110), width=2)

    elif leaf_type == "wheat_blade":
        # Slender linear green blade
        draw.polygon([(110, 10), (145, 10), (140, 245), (115, 245)], fill=(35, 140, 50))
        # Parallel veins
        for x in range(115, 140, 4):
            draw.line([x, 15, x, 240], fill=(50, 165, 65), width=1)

    elif leaf_type == "tomato_leaf":
        # Lobed tomato leaf
        draw.polygon([(128, 30), (160, 70), (190, 60), (170, 100), (210, 130), (160, 150), (180, 200), (128, 220), (76, 200), (96, 150), (46, 130), (86, 100), (66, 60), (96, 70)], fill=(45, 145, 50))
        draw.line([128, 35, 128, 215], fill=(65, 175, 70), width=2)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()

def run_tests():
    print("=== Testing Crop Inference with Trained ML Ensemble ===")
    
    test_cases = [
        ("rose_green_leaf", "Rose (Rosa rubiginosa / hybrid)"),
        ("rose_black_spot", "Rose (Rosa rubiginosa / hybrid)"),
        ("brinjal_leaf", "Brinjal / Eggplant (Solanum melongena)"),
        ("wheat_blade", "Wheat (Triticum aestivum)"),
        ("tomato_leaf", "Tomato (Solanum lycopersicum)")
    ]
    
    for ltype, expected_crop in test_cases:
        img_bytes = create_mock_leaf_image(ltype)
        res = CropInferenceService.analyze_crop_image(img_bytes)
        print(f"\nSpecimen: {ltype}")
        print(f"  -> Predicted Crop: {res['predictedCrop']}")
        print(f"  -> Condition: {res['predictedCondition']}")
        print(f"  -> Health: {res['healthPercentage']}% | Damage: {res['damageSeverityPercentage']}%")
        print(f"  -> Confidence: {res['confidence'] * 100.0:.1f}%")
        print(f"  -> Model Status: {res['modelStatus']}")
        print(f"  -> Recommendation Count: {len(res['recommendations'])}")

if __name__ == "__main__":
    run_tests()
