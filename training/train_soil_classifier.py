"""
AGRO AI — Soil Classification Model Training Script
Trains a MobileNetV2 CNN for visual soil category classification.
"""

import os
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "datasets" / "soil"
MODELS_DIR = BASE_DIR / "backend" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15

def train():
    train_dir = DATASET_DIR / "train"
    val_dir = DATASET_DIR / "validation"

    if not train_dir.exists() or len(list(train_dir.glob("*/*"))) < 10:
        print(f"Soil training data not found at {train_dir}.")
        print("Please review datasets/README.md for soil data setup.")
        return

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        horizontal_flip=True,
        vertical_flip=True,
        zoom_range=0.2
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
    base = MobileNetV2(weights="imagenet", include_top=False, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    base.trainable = False

    x = GlobalAveragePooling2D()(base.output)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.3)(x)
    out = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base.input, outputs=out)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    export_path = MODELS_DIR / "soil_classifier.keras"
    callbacks = [
        EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True),
        ModelCheckpoint(str(export_path), monitor="val_accuracy", save_best_only=True)
    ]

    model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS, callbacks=callbacks)
    print(f"✓ Soil classification model saved to {export_path}")

if __name__ == "__main__":
    train()
