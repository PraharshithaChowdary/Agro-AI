import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.ml.model_loader import model_registry, MODEL_PATHS, METADATA_PATH

def check_models():
    print("==================================================")
    print("AGRO AI Machine Learning Model Diagnostic Status")
    print("==================================================")

    for key, path in MODEL_PATHS.items():
        present = path.exists()
        metadata = model_registry.get_metadata(key)
        name = metadata.get("model_name", key)
        version = metadata.get("version", "1.0.0")

        status_symbol = "[FOUND]" if present else "[CONFIGURED - WEIGHTS PENDING TRAINING]"
        print(f"\nModel: {name} (Key: {key})")
        print(f"  Status: {status_symbol}")
        print(f"  Target File: {path}")
        print(f"  Architecture: {metadata.get('architecture', 'Lightweight CNN')}")
        print(f"  Input Shape: {metadata.get('input_shape', [224, 224, 3])}")
        print(f"  Supported Classes: {len(metadata.get('classes', []))} classes")

    print("\n--------------------------------------------------")
    print("Summary:")
    print("* Automated fallback vision & agronomic reasoning engine is ACTIVE.")
    print("* To train production deep CNN weights (.keras files), run:")
    print("  Google Colab: training/agro_ai_production_training.ipynb")
    print("  Local Script: python training/train_crop_disease.py")
    print("==================================================")

if __name__ == "__main__":
    check_models()
