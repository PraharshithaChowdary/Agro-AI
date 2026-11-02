"""
AGRO AI — Indian Plant Species Identification Training Script
=============================================================
Fine-tunes a Deep Convolutional Neural Network (MobileNetV2) on real,
labelled botanical photographs arranged by species directory.

Dataset Directory Structure Expected:
-------------------------------------
datasets/plant_species/
  ├── train/
  │   ├── abelmoschus-esculentus/
  │   │   ├── img1.jpg
  │   │   └── img2.jpg
  │   ├── azadirachta-indica/
  │   └── ... (other species)
  └── validation/
      ├── abelmoschus-esculentus/
      └── ...

Usage:
------
Local or Google Colab:
  python training/train_plant_identification.py --data-dir /path/to/dataset --epochs 25 --batch-size 32
"""

import os
import sys
import json
import argparse
from pathlib import Path
import numpy as np

# Suppress TensorFlow verbose info logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = BASE_DIR / "datasets" / "plant_species"
DEFAULT_MODELS_DIR = BASE_DIR / "backend" / "models"
METADATA_PATH = DEFAULT_MODELS_DIR / "model_metadata.json"

IMG_SIZE = (224, 224)
DEFAULT_BATCH_SIZE = 32
DEFAULT_EPOCHS = 25
DEFAULT_LR = 3e-4


def parse_args():
    parser = argparse.ArgumentParser(description="Train AGRO AI Plant Species Vision Model")
    parser.add_argument(
        "--data-dir",
        type=str,
        default=str(DEFAULT_DATA_DIR),
        help="Path to dataset containing 'train' and 'validation' folders (or class subfolders)."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(DEFAULT_MODELS_DIR),
        help="Directory to save the trained model (.keras) and class metadata."
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=DEFAULT_EPOCHS,
        help="Number of training epochs."
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Training batch size."
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=DEFAULT_LR,
        help="Initial Adam learning rate."
    )
    parser.add_argument(
        "--download-public",
        action="store_true",
        help="Automatically download public open plant photograph dataset (Zero API keys / zero tokens required)."
    )
    return parser.parse_args()


def download_public_dataset(target_dir: Path) -> bool:
    """
    Downloads publicly accessible real botanical photographs from the open PlantVillage
    research repository with NO API keys, NO login, and NO tokens.
    """
    import subprocess
    import shutil
    print("\n[INFO] Starting automatic public dataset download (Zero tokens / Zero API keys)...")
    target_dir.mkdir(parents=True, exist_ok=True)
    temp_repo = target_dir.parent / "temp_plantvillage_repo"
    
    try:
        print("[1/2] Cloning public plant repository from GitHub...")
        res = subprocess.run(
            ["git", "clone", "--depth", "1", "https://github.com/spMohanty/PlantVillage-Dataset.git", str(temp_repo)],
            capture_output=True,
            text=True
        )
        if res.returncode != 0:
            print(f"[WARN] Git clone error: {res.stderr}")
            return False

        src_color = temp_repo / "raw" / "color"
        if src_color.exists():
            print("[2/2] Moving real plant photograph classes into dataset directory...")
            for d in src_color.iterdir():
                if d.is_dir():
                    dst = target_dir / d.name
                    shutil.copytree(d, dst, dirs_exist_ok=True)
            shutil.rmtree(temp_repo, ignore_errors=True)
            print(f"[SUCCESS] Downloaded public plant dataset to: {target_dir}")
            return True
        return False
    except Exception as e:
        print(f"[ERROR] Failed to download public dataset: {e}")
        shutil.rmtree(temp_repo, ignore_errors=True)
        return False


def check_dataset_validity(data_dir: Path):
    """
    Validates whether genuine labelled image subfolders exist in data_dir.
    Returns (train_path, val_path, is_valid, message).
    """
    if not data_dir.exists():
        return None, None, False, f"Dataset root directory not found at: {data_dir}"

    train_dir = data_dir / "train"
    val_dir = data_dir / "validation"
    if not val_dir.exists():
        val_dir = data_dir / "val"

    # Case 1: train/ and validation/ subdirectories exist
    if train_dir.exists() and train_dir.is_dir():
        train_classes = [d for d in train_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
        if len(train_classes) < 2:
            return None, None, False, f"Found only {len(train_classes)} class in {train_dir}. At least 2 species classes are required."
        
        sample_images = list(train_dir.glob("*/*.jpg")) + list(train_dir.glob("*/*.png")) + list(train_dir.glob("*/*.jpeg"))
        if len(sample_images) < 10:
            return None, None, False, f"Found only {len(sample_images)} total images in {train_dir}. Insufficient real data for training."
        
        return train_dir, (val_dir if val_dir.exists() else None), True, f"Found {len(train_classes)} species classes with {len(sample_images)} training images."

    # Case 2: Class subfolders exist directly in data_dir
    root_classes = [d for d in data_dir.iterdir() if d.is_dir() and not d.name.startswith(".") and d.name not in ["train", "val", "validation", "test"]]
    if len(root_classes) >= 2:
        sample_images = list(data_dir.glob("*/*.jpg")) + list(data_dir.glob("*/*.png")) + list(data_dir.glob("*/*.jpeg"))
        if len(sample_images) >= 10:
            return data_dir, None, True, f"Found {len(root_classes)} direct species class folders in {data_dir} with {len(sample_images)} images."

    return None, None, False, (
        f"No genuine plant image folders found in '{data_dir}'.\n"
        "Please provide real photographic plant image folders structured as:\n"
        "  datasets/plant_species/train/<species-name>/*.jpg\n"
        "  datasets/plant_species/validation/<species-name>/*.jpg"
    )


def build_plant_model(num_classes: int, learning_rate: float = DEFAULT_LR):
    """
    Constructs transfer learning model using MobileNetV2 pretrained on ImageNet.
    MobileNetV2's expected inputs are scaled to [-1, 1]; backend inference mirrors this for Keras.
    """
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
    from tensorflow.keras.models import Model

    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)
    )

    # Freeze earlier feature extractor layers, fine-tune top 30 layers
    for layer in base_model.layers[:-30]:
        layer.trainable = False
    for layer in base_model.layers[-30:]:
        layer.trainable = True

    x = base_model.output
    x = GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = BatchNormalization(name="batch_norm")(x)
    x = Dense(384, activation="relu", name="dense_features")(x)
    x = Dropout(0.4, name="dropout")(x)
    outputs = Dense(num_classes, activation="softmax", name="species_probabilities")(x)

    model = Model(inputs=base_model.input, outputs=outputs, name="agro_ai_plant_identifier")
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.TopKCategoricalAccuracy(k=min(5, num_classes), name=f"top_{min(5, num_classes)}_accuracy")
        ]
    )
    return model


def train():
    args = parse_args()
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("AGRO AI — Botanical Vision Identification Model Trainer")
    print("=" * 70)
    if args.download_public:
        download_public_dataset(data_dir)

    train_path, val_path, is_valid, msg = check_dataset_validity(data_dir)
    if not is_valid:
        print(f"\n[DATASET NOTICE] {msg}\n")
        print("To train this model on Google Colab or locally:")
        print("1. Download real plant photographs (e.g. PlantVillage, iNaturalist, or Kaggle Indian Plants).")
        print("2. Place them in species-named subfolders under datasets/plant_species/train/<species_id>/")
        print("3. Re-run: python training/train_plant_identification.py --data-dir datasets/plant_species")
        return False

    print(f"[SUCCESS] {msg}")

    import tensorflow as tf
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

    # Match MobileNetV2's ImageNet preprocessing ([-1, 1]), rather than
    # training a pretrained backbone on a different [0, 1] input distribution.
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=25,
        zoom_range=0.2,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        horizontal_flip=True,
        validation_split=0.2 if val_path is None else 0.0,
        fill_mode="nearest"
    )

    if val_path is not None:
        val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
        train_generator = train_datagen.flow_from_directory(
            str(train_path),
            target_size=IMG_SIZE,
            batch_size=args.batch_size,
            class_mode="categorical",
            shuffle=True
        )
        val_generator = val_datagen.flow_from_directory(
            str(val_path),
            target_size=IMG_SIZE,
            batch_size=args.batch_size,
            class_mode="categorical",
            shuffle=False
        )
    else:
        # Split single directory into train (80%) and validation (20%)
        train_generator = train_datagen.flow_from_directory(
            str(train_path),
            target_size=IMG_SIZE,
            batch_size=args.batch_size,
            class_mode="categorical",
            subset="training",
            shuffle=True
        )
        val_generator = train_datagen.flow_from_directory(
            str(train_path),
            target_size=IMG_SIZE,
            batch_size=args.batch_size,
            class_mode="categorical",
            subset="validation",
            shuffle=False
        )

    num_classes = train_generator.num_classes
    # Save exact class labels matching sorted indices
    class_indices = train_generator.class_indices
    sorted_classes = sorted(class_indices.keys(), key=lambda k: class_indices[k])

    print(f"[INFO] Discovered {num_classes} species classes.")
    print(f"[INFO] Classes: {sorted_classes[:10]} ... ({num_classes} total)")

    model = build_plant_model(num_classes, learning_rate=args.learning_rate)

    model_export_path = output_dir / "plant_identifier.keras"
    classes_export_path = output_dir / "plant_classes.json"

    # Save class mapping immediately
    with open(classes_export_path, "w", encoding="utf-8") as f:
        json.dump(sorted_classes, f, indent=2)
    print(f"[INFO] Saved class indices mapping to {classes_export_path}")

    callbacks = [
        EarlyStopping(monitor="val_accuracy", patience=6, restore_best_weights=True, verbose=1),
        ModelCheckpoint(str(model_export_path), monitor="val_accuracy", save_best_only=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=2, min_lr=1e-6, verbose=1)
    ]

    print("\n[INFO] Starting training...")
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=args.epochs,
        callbacks=callbacks
    )

    # Evaluate final validation metrics
    val_loss, val_acc, val_top5 = model.evaluate(val_generator)
    print("\n" + "=" * 70)
    print("TRAINING COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print(f"  Validation Accuracy (Top-1; not an independent field benchmark): {val_acc * 100:.2f}%")
    print(f"  Validation Accuracy (Top-5; not an independent field benchmark): {val_top5 * 100:.2f}%")
    print(f"  Model Saved: {model_export_path}")

    # Update model metadata
    metadata = {}
    if METADATA_PATH.exists():
        try:
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except Exception:
            metadata = {}

    # Keep the deployed ONNX model's class map intact. This is a separately trained
    # Keras model; model_loader prefers it only when its own metadata is present.
    metadata["plant_identifier_keras"] = {
        "model_name": f"MobileNetV2 Botanical Vision Classifier ({num_classes} Species)",
        "format": "keras",
        "classes": sorted_classes,
        "num_classes": num_classes,
        "image_size": [IMG_SIZE[0], IMG_SIZE[1], 3],
        "preprocessing": "mobilenet_v2_minus1_to_1",
        "validation_top1_accuracy": round(float(val_acc), 4),
        "validation_top5_accuracy": round(float(val_top5), 4),
        "accuracy_verified_on_independent_real_photos": False,
        "status": "trained_validation_metrics_recorded_independent_real_photo_test_required",
        "has_real_weights": True
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[SUCCESS] Updated {METADATA_PATH}")

    return True


if __name__ == "__main__":
    train()
