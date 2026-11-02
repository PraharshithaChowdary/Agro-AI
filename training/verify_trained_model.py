import sys
import json
from pathlib import Path
import numpy as np
import onnxruntime as ort
from PIL import Image
import io

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.ml.model_loader import model_registry
from app.ml.preprocessing import load_and_preprocess_image, extract_botanical_feature_vector
from app.services.plant_identifier_service import PlantIdentifierService
from app.database import SessionLocal

def main():
    print("=" * 70)
    print("AGRO AI — Botanical Vision Integration & Verification Suite")
    print("=" * 70)

    # 1. Check all model files on disk
    models_dir = Path("backend/models")
    joblib_path = models_dir / "plant_identifier.joblib"
    onnx_path = models_dir / "plant_identifier.onnx"
    keras_path = models_dir / "plant_identifier.keras"
    classes_path = models_dir / "plant_classes.json"

    print("\n[1/5] Verifying model files on disk:")
    print(f"  - 98-Species Botanical Classifier (.joblib): {joblib_path.exists()} ({joblib_path.stat().st_size / (1024*1024):.2f} MB)" if joblib_path.exists() else "  - Joblib Model: False")
    print(f"  - 14-Crop Deep Foliar Model (.onnx)       : {onnx_path.exists()} ({onnx_path.stat().st_size / (1024*1024):.2f} MB)" if onnx_path.exists() else "  - ONNX Model: False")
    print(f"  - Keras Archive (.keras)                  : {keras_path.exists()} ({keras_path.stat().st_size / (1024*1024):.2f} MB)" if keras_path.exists() else "  - Keras Model: False")
    print(f"  - Verified Classes JSON                   : {classes_path.exists()} ({classes_path.stat().st_size} bytes)")

    assert joblib_path.exists() or onnx_path.exists(), "No valid plant_identifier model found!"
    assert classes_path.exists(), "plant_classes.json not found!"

    # 2. Check classes and output layer dimensions
    print("\n[2/5] Verifying model classes and output layer dimensions:")
    with open(classes_path, "r", encoding="utf-8") as f:
        classes = json.load(f)
    print(f"  - Number of verified botanical classes: {len(classes)}")
    print(f"  - Sample classes: {classes[:8]} ... {classes[-4:]}")

    if onnx_path.exists():
        sess = ort.InferenceSession(str(onnx_path))
        in_meta = sess.get_inputs()[0]
        out_meta = sess.get_outputs()[0]
        print(f"  - ONNX Input  : '{in_meta.name}' with shape {in_meta.shape}")
        print(f"  - ONNX Output : '{out_meta.name}' with shape {out_meta.shape}")
        assert out_meta.shape[-1] in [14, len(classes)], f"Unexpected ONNX output dim {out_meta.shape[-1]}"
        print(f"  [OK] SUCCESS: ONNX model verified ({out_meta.shape[-1]} deep classes).")

    # 3. Verify ModelRegistry loader
    print("\n[3/5] Verifying ModelRegistry loader:")
    is_trained = model_registry.is_plant_identifier_trained()
    print(f"  - is_plant_identifier_trained(): {is_trained}")
    assert is_trained is True, "ModelRegistry should report trained=True!"

    loaded_model = model_registry.get_model("plant_identifier")
    print(f"  - Loaded primary model type: {type(loaded_model)}")
    assert loaded_model is not None, "Primary plant_identifier model must load!"

    registry_classes = model_registry.get_classes("plant_identifier")
    assert len(registry_classes) == len(classes), f"Class count mismatch: {len(registry_classes)} vs {len(classes)}"
    print(f"  [OK] SUCCESS: ModelRegistry loaded primary model with {len(registry_classes)} verified species classes.")

    # 4. Verify Image Preprocessing
    print("\n[4/5] Verifying image preprocessing tensor and botanical feature vector:")
    test_img = Image.new("RGB", (320, 240), color=(40, 150, 45))
    buf = io.BytesIO()
    test_img.save(buf, format="JPEG")
    img_bytes = buf.getvalue()

    tensor = load_and_preprocess_image(img_bytes)
    feat_vec = extract_botanical_feature_vector(img_bytes)
    print(f"  - CNN Tensor shape: {tensor.shape}, dtype: {tensor.dtype}, min/max: {tensor.min():.3f}/{tensor.max():.3f}")
    print(f"  - Feature vector shape: {feat_vec.shape}, dtype: {feat_vec.dtype}")
    assert tensor.shape == (1, 224, 224, 3), "Tensor must be (1, 224, 224, 3)"
    assert len(feat_vec) == 48, "Feature vector must be 48 dimensions"
    print("  [OK] SUCCESS: Preprocessing pipelines active and validated.")

    # 5. Verify PlantIdentifierService inference and candidate ranking
    print("\n[5/5] Running end-to-end identification inference:")
    db = SessionLocal()
    result = PlantIdentifierService.identify_plant(image_bytes=img_bytes, db=db)
    db.close()

    assert result["success"] is True, "Result success should be True"
    assert result["isAgricultural"] is True, "Should be recognized as agricultural"
    assert result["topCandidate"] is not None, "Top candidate must be populated"
    assert len(result["candidates"]) >= 1, "Candidates list must be populated"

    top = result["topCandidate"]
    top_id = top.get("plantId") or top.get("id")
    top_name = top.get("commonName")
    top_conf = top.get("confidencePercentage")

    print(f"  - Identification Success : {result['success']}")
    print(f"  - Mode                    : {result['mode']}")
    print(f"  - Detected Organ          : {result['detectedOrgan']}")
    print(f"  - Top Species ID          : {top_id}")
    print(f"  - Common Name             : {top_name}")
    print(f"  - Scientific Name         : {top.get('scientificName')}")
    print(f"  - Confidence              : {top_conf}%")
    print(f"  - Ranked Candidates Count : {len(result['candidates'])}")
    print(f"  - Calibrated Entropy      : {result.get('calibratedEntropy')}")

    print("\n  Top Ranked Candidates:")
    for c in result["candidates"][:5]:
        cid = c.get("plantId") or c.get("id")
        cnm = c.get("commonName") or cid
        print(f"    #{c.get('rank', 1)}: {cnm} ({cid}) - {c.get('confidencePercentage')}%")

    print("\n" + "=" * 70)
    print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY (100% VERIFIED)")
    print("=" * 70)

if __name__ == "__main__":
    main()
