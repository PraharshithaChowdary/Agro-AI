import os
import json
import joblib
from pathlib import Path
from typing import Optional, Dict, Any, List
import numpy as np
from app.config import settings

MODELS_DIR = Path(settings.MODELS_DIR)
METADATA_PATH = MODELS_DIR / "model_metadata.json"
PLANT_CLASSES_PATH = MODELS_DIR / "plant_classes.json"


class ModelRegistry:
    _instance = None
    _loaded_models: Dict[str, Any] = {}
    _metadata: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
            cls._instance._load_metadata()
            cls._instance._preload_models()
        return cls._instance

    def _load_metadata(self):
        if METADATA_PATH.exists():
            try:
                with open(METADATA_PATH, "r", encoding="utf-8") as f:
                    self._metadata = json.load(f)
            except Exception as e:
                print(f"[WARN] Failed to load model metadata: {e}")
                self._metadata = {}
        else:
            self._metadata = {}

    def _preload_models(self):
        """Preloads available verified models on server start."""
        for key in ["crop_disease", "soil_classifier", "agricultural_relevance"]:
            self.get_model(key)
        # Check plant identifier status
        # Load the actual image model used for visual species identification.
        # The 98-class joblib classifier consumes engineered feature vectors and must not
        # be represented as a trained image-recognition model.
        if (MODELS_DIR / "plant_identifier.onnx").exists() or (MODELS_DIR / "plant_identifier.keras").exists():
            self.get_model("plant_identifier_onnx")
        else:
            print("[WARN] No image-trained plant vision model found; plant identification will return inconclusive results.")

    def is_plant_identifier_trained(self) -> bool:
        """Return whether a supported image-model artefact is available on disk.

        This indicates file availability only, not that runtime dependencies load it
        successfully or that it has any particular real-photo accuracy.
        The legacy feature-vector joblib is not treated as a photo classifier.
        """
        meta = self.get_metadata("plant_identifier")
        keras_meta = self._metadata.get("plant_identifier_keras", {})
        onnx_path = MODELS_DIR / "plant_identifier.onnx"
        keras_path = MODELS_DIR / "plant_identifier.keras"
        onnx_available = bool(meta.get("has_real_weights", False) and onnx_path.exists())
        keras_available = bool(keras_meta.get("has_real_weights", False) and keras_path.exists())
        return onnx_available or keras_available

    def get_model(self, model_key: str):
        """
        Loads and returns the model from disk.
        Does not load synthetic placeholder models as real vision classifiers.
        """
        if model_key in self._loaded_models:
            return self._loaded_models[model_key]

        # Keep the public plant_identifier key aligned with the same ONNX image model
        # used by plant identification. Never silently substitute a feature-vector model.
        if model_key == "plant_identifier":
            return self.get_model("plant_identifier_onnx")

        # Plant image model. Once the supported training script has created and
        # registered a Keras model, prefer that newer model to the legacy ONNX file.
        # Otherwise use ONNX; fall back to Keras if ONNX Runtime is unavailable.
        if model_key == "plant_identifier_onnx":
            keras_path = MODELS_DIR / "plant_identifier.keras"
            keras_meta = self._metadata.get("plant_identifier_keras", {})
            prefer_keras = bool(keras_meta.get("has_real_weights", False) and keras_path.exists())

            if prefer_keras:
                try:
                    import tensorflow as tf
                    keras_model = tf.keras.models.load_model(str(keras_path), compile=False)
                    self._loaded_models[model_key] = keras_model
                    print(f"[INFO] Loaded newly trained Keras plant vision model from {keras_path.name}")
                    return keras_model
                except Exception as e:
                    print(f"[WARN] Failed to load Keras plant vision model {keras_path}: {e}")

            onnx_path = MODELS_DIR / "plant_identifier.onnx"
            if onnx_path.exists():
                try:
                    import onnxruntime as ort
                    session = ort.InferenceSession(str(onnx_path))
                    self._loaded_models[model_key] = session
                    print(f"[INFO] Loaded ONNX plant vision model from {onnx_path.name}")
                    return session
                except Exception as e:
                    print(f"[WARN] Failed to load ONNX model {onnx_path}: {e}")

            if keras_path.exists():
                try:
                    import tensorflow as tf
                    keras_model = tf.keras.models.load_model(str(keras_path), compile=False)
                    self._loaded_models[model_key] = keras_model
                    print(f"[INFO] Loaded fallback Keras plant vision model from {keras_path.name}")
                    return keras_model
                except Exception as e:
                    print(f"[WARN] Failed to load fallback Keras plant model {keras_path}: {e}")
            return None

        # Standard loading for other modules
        joblib_path = MODELS_DIR / f"{model_key}.joblib"
        keras_path = MODELS_DIR / f"{model_key}.keras"

        if joblib_path.exists():
            try:
                model = joblib.load(joblib_path)
                self._loaded_models[model_key] = model
                print(f"[INFO] Loaded ML model '{model_key}' from {joblib_path.name}")
                return model
            except Exception as e:
                print(f"[WARN] Failed to load joblib model {joblib_path}: {e}")

        if keras_path.exists():
            try:
                import tensorflow as tf
                model = tf.keras.models.load_model(str(keras_path))
                self._loaded_models[model_key] = model
                print(f"[INFO] Loaded Keras model '{model_key}' from {keras_path.name}")
                return model
            except Exception as e:
                print(f"[WARN] Failed to load keras model {keras_path}: {e}")

        return None

    def is_model_file_present(self, model_key: str) -> bool:
        if model_key == "plant_identifier":
            return self.is_plant_identifier_trained()
        joblib_path = MODELS_DIR / f"{model_key}.joblib"
        keras_path = MODELS_DIR / f"{model_key}.keras"
        return joblib_path.exists() or keras_path.exists()

    def get_metadata(self, model_key: str) -> Dict[str, Any]:
        return self._metadata.get(model_key, {})

    def get_classes(self, model_key: str) -> List[str]:
        if model_key in {"plant_identifier_onnx", "plant_identifier"}:
            active_model = self._loaded_models.get("plant_identifier_onnx")
            is_keras_model = active_model is not None and hasattr(active_model, "predict") and not hasattr(active_model, "run")
            meta = self.get_metadata("plant_identifier")
            keras_meta = self._metadata.get("plant_identifier_keras", {})
            keras_path = MODELS_DIR / "plant_identifier.keras"

            # If a model has already loaded, its class map must match that exact runtime.
            # Do not select Keras labels for an ONNX session just because a Keras file exists.
            if active_model is not None and not is_keras_model:
                return meta.get("deep_crop_subset_classes", [])

            if is_keras_model or (active_model is None and keras_meta.get("has_real_weights", False) and keras_path.exists()):
                labels = []
                if PLANT_CLASSES_PATH.exists():
                    try:
                        with open(PLANT_CLASSES_PATH, "r", encoding="utf-8") as f:
                            labels = json.load(f)
                    except Exception as e:
                        print(f"[WARN] Failed to read trained plant class labels: {e}")
                if not labels:
                    labels = keras_meta.get("classes", [])
                if is_keras_model:
                    try:
                        output_count = int(active_model.output_shape[-1])
                        if len(labels) != output_count:
                            print(f"[WARN] Keras label count ({len(labels)}) does not match model output count ({output_count}); returning no classes.")
                            return []
                    except Exception:
                        return []
                return labels
            return meta.get("deep_crop_subset_classes", [])
        meta = self.get_metadata(model_key)
        return meta.get("classes", [])


model_registry = ModelRegistry()

