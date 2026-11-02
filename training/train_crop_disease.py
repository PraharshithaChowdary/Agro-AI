"""
AGRO AI — Crop & Foliar Disease Model Training Script
Fine-tunes MobileNetV2 on multi-class crop pathogen datasets (PlantVillage / PlantDoc).
"""

import os
import json
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "datasets" / "crop_disease"
MODELS_DIR = BASE_DIR / "backend" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20

def build_crop_model(num_classes: int):
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)
    )
    # Fine-tuning: Freeze early layers, keep upper layers trainable
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.4)(x)
    predictions = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=3e-4),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=3, name="top_3_accuracy")]
    )
    return model

def train():
    train_dir = DATASET_DIR / "train"
    val_dir = DATASET_DIR / "validation"

    if not train_dir.exists() or len(list(train_dir.glob("*/*"))) < 10:
        print(f"Training data not found at {train_dir}.")
        print("Please download PlantVillage / PlantDoc datasets as documented in DATASET_GUIDE.md")
        return

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=25,
        zoom_range=0.2,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest"
    )

    val_datagen = ImageDataGenerator(rescale=1./255)

    train_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical"
    )

    val_gen = val_datagen.flow_from_directory(
        val_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical"
    )

    num_classes = train_gen.num_classes
    class_labels = list(train_gen.class_indices.keys())
    print(f"Discovered {num_classes} crop disease classes.")

    model = build_crop_model(num_classes)
    export_path = MODELS_DIR / "crop_disease.keras"

    callbacks = [
        EarlyStopping(monitor="val_accuracy", patience=5, restore_best_weights=True),
        ModelCheckpoint(str(export_path), monitor="val_accuracy", save_best_only=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=2, min_lr=1e-6)
    ]

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    print(f"✓ Model trained and saved to {export_path}")

if __name__ == "__main__":
    train()
