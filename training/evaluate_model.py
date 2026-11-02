"""
AGRO AI — Model Evaluation & Metrics Reporting Script
Evaluates trained models on unseen test datasets and outputs Accuracy, Precision,
Recall, F1-score, and Confusion Matrix.
"""

import os
import json
import numpy as np
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "backend" / "models"
DATASETS_DIR = BASE_DIR / "datasets"

def evaluate_crop_model():
    model_path = MODELS_DIR / "crop_disease.keras"
    test_dir = DATASETS_DIR / "crop_disease" / "test"

    print("Evaluating Crop Disease Classifier...")
    if not model_path.exists():
        print(f"Model file not found at {model_path}.")
        return

    if not test_dir.exists() or len(list(test_dir.glob("*/*"))) == 0:
        print(f"Test dataset directory empty at {test_dir}.")
        return

    import tensorflow as tf
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    model = tf.keras.models.load_model(str(model_path))
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_gen = test_datagen.flow_from_directory(
        test_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode="categorical",
        shuffle=False
    )

    preds = model.predict(test_gen)
    y_pred = np.argmax(preds, axis=1)
    y_true = test_gen.classes
    target_names = list(test_gen.class_indices.keys())

    print("\n--- Classification Report ---")
    print(classification_report(y_true, y_pred, target_names=target_names))

    cm = confusion_matrix(y_true, y_pred)
    print("\n--- Confusion Matrix ---")
    print(cm)

if __name__ == "__main__":
    evaluate_crop_model()
