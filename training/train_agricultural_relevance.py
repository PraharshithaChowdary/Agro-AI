"""
AGRO AI — Agricultural Relevance Model Training Script
Trains a MobileNetV2 binary/multi-class classifier to distinguish
agricultural images (crops, soil, fields) from non-agricultural images (cars, selfies, electronics, buildings).
"""

import os
import json
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "datasets" / "agricultural_relevance"
MODELS_DIR = BASE_DIR / "backend" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15

def build_model(num_classes=2):
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)
    )
    base_model.trainable = False  # Freeze base layers for transfer learning

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.3)(x)
    predictions = Dense(1 if num_classes == 2 else num_classes, activation="sigmoid" if num_classes == 2 else "softmax")(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    loss = "binary_crossentropy" if num_classes == 2 else "categorical_crossentropy"
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), loss=loss, metrics=["accuracy"])
    return model

def train():
    print("Checking dataset availability...")
    if not DATASET_DIR.exists() or len(list(DATASET_DIR.glob("*/*"))) < 10:
        print(f"Dataset not populated in {DATASET_DIR}. Please organize images before starting training.")
        return

    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        validation_split=0.2
    )

    train_generator = datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="binary",
        subset="training"
    )

    val_generator = datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="binary",
        subset="validation"
    )

    model = build_model(num_classes=2)
    export_path = MODELS_DIR / "agricultural_relevance.keras"

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True),
        ModelCheckpoint(str(export_path), monitor="val_accuracy", save_best_only=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2)
    ]

    print("Starting Transfer Learning Training...")
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    print(f"✓ Model successfully trained and saved to {export_path}")

if __name__ == "__main__":
    train()
