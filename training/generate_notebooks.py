import json
from pathlib import Path

TRAINING_DIR = Path(r"c:\Users\praha\Desktop\PDD AGRO AI\training")
TRAINING_DIR.mkdir(parents=True, exist_ok=True)

def create_notebook(title, description, task_type, default_classes, export_name, output_path):
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# AGRO AI — {title}\n",
                f"> **Smart Agriculture. Healthy Lives. Better Future.**\n\n",
                f"### Task: {description}\n\n",
                "This notebook trains a deep learning transfer learning vision model using GPU acceleration on Google Colab.\n",
                "Follow the numbered sections sequentially."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 1. Environment Initialization & GPU Acceleration Verification"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import sys\n",
                "import json\n",
                "import shutil\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from pathlib import Path\n",
                "from PIL import Image\n",
                "import tensorflow as tf\n",
                "from tensorflow.keras import layers, models, optimizers, callbacks\n",
                "from tensorflow.keras.applications import MobileNetV2\n",
                "from sklearn.metrics import classification_report, confusion_matrix\n\n",
                "print(f'TensorFlow Version: {tf.__version__}')\n",
                "gpus = tf.config.list_physical_devices('GPU')\n",
                "if gpus:\n",
                "    print(f'[OK] GPU Accelerator Detected: {gpus[0].name}')\n",
                "else:\n",
                "    print('[WARN] No GPU detected. In Colab, select: Runtime -> Change runtime type -> T4 GPU.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 2. Dataset Acquisition & Directory Setup"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                f"# Define data directories\n",
                f"DATASET_DIR = Path('/content/datasets/{task_type}')\n",
                f"EXPORT_DIR = Path('/content/exported_models')\n",
                f"EXPORT_DIR.mkdir(parents=True, exist_ok=True)\n",
                f"DATASET_DIR.mkdir(parents=True, exist_ok=True)\n\n",
                f"print(f'Dataset path configured: {{DATASET_DIR}}')\n",
                f"print('If using Google Drive, you can mount via: from google.colab import drive; drive.mount(\"/content/drive\")')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 3. Dataset Inspection & Stratified Splitting"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "IMG_SIZE = (224, 224)\n",
                "BATCH_SIZE = 32\n",
                "EPOCHS = 20\n\n",
                "# Data Augmentation & Normalization Generators\n",
                "train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(\n",
                "    rescale=1.0 / 255.0,\n",
                "    rotation_range=25,\n",
                "    width_shift_range=0.15,\n",
                "    height_shift_range=0.15,\n",
                "    zoom_range=0.20,\n",
                "    shear_range=0.15,\n",
                "    horizontal_flip=True,\n",
                "    fill_mode='nearest'\n",
                ")\n\n",
                "val_test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255.0)\n",
                "print('[OK] Preprocessing and augmentation pipelines configured.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 4. Model Architecture & Transfer Learning Definition"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "def build_transfer_learning_model(num_classes: int):\n",
                "    base_model = MobileNetV2(\n",
                "        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),\n",
                "        include_top=False,\n",
                "        weights='imagenet'\n",
                "    )\n",
                "    # Freeze early feature extractors\n",
                "    for layer in base_model.layers[:-25]:\n",
                "        layer.trainable = False\n\n",
                "    x = base_model.output\n",
                "    x = layers.GlobalAveragePooling2D()(x)\n",
                "    x = layers.BatchNormalization()(x)\n",
                "    x = layers.Dense(256, activation='relu')(x)\n",
                "    x = layers.Dropout(0.4)(x)\n",
                "    predictions = layers.Dense(num_classes, activation='softmax')(x)\n\n",
                "    model = models.Model(inputs=base_model.input, outputs=predictions)\n",
                "    model.compile(\n",
                "        optimizer=optimizers.Adam(learning_rate=3e-4),\n",
                "        loss='categorical_crossentropy',\n",
                "        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=min(3, num_classes), name='top_3_acc')]\n",
                "    )\n",
                "    return model\n\n",
                "print('[OK] Architecture function defined with MobileNetV2 backbone.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 5. Model Training with Early Stopping & Checkpoints"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                f"# Training execution placeholder\n",
                f"export_model_path = EXPORT_DIR / '{export_name}.keras'\n",
                f"training_callbacks = [\n",
                f"    callbacks.EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True),\n",
                f"    callbacks.ModelCheckpoint(str(export_model_path), monitor='val_accuracy', save_best_only=True),\n",
                f"    callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=2, min_lr=1e-6)\n",
                f"]\n",
                f"print(f'Model checkpoint target: {{export_model_path}}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 6. Evaluation, Confusion Matrix & Metrics"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "def plot_training_curves(history):\n",
                "    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n",
                "    ax1.plot(history.history['accuracy'], label='Train Accuracy')\n",
                "    ax1.plot(history.history['val_accuracy'], label='Val Accuracy')\n",
                "    ax1.set_title('Accuracy Trajectory')\n",
                "    ax1.set_xlabel('Epoch')\n",
                "    ax1.legend()\n",
                "    ax1.grid(True)\n\n",
                "    ax2.plot(history.history['loss'], label='Train Loss')\n",
                "    ax2.plot(history.history['val_loss'], label='Val Loss')\n",
                "    ax2.set_title('Loss Trajectory')\n",
                "    ax2.set_xlabel('Epoch')\n",
                "    ax2.legend()\n",
                "    ax2.grid(True)\n",
                "    plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 7. Model & Metadata Export for AGRO AI Backend"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                f"# Export class map metadata\n",
                f"class_metadata = {{\n",
                f"    'task': '{task_type}',\n",
                f"    'model_filename': '{export_name}.keras',\n",
                f"    'classes': {json.dumps(default_classes, indent=4)},\n",
                f"    'input_size': [224, 224, 3]\n",
                f"}}\n",
                f"metadata_path = EXPORT_DIR / '{export_name}_metadata.json'\n",
                f"with open(metadata_path, 'w') as mf:\n",
                f"    json.dump(class_metadata, mf, indent=2)\n\n",
                f"print(f'[OK] Metadata written to: {{metadata_path}}')\n",
                f"print('\\nTo deploy to AGRO AI:')\n",
                f"print('1. Download {export_name}.keras and place into: backend/models/{export_name}.keras')\n",
                f"print('2. Verify via: python backend/scripts/check_models.py')"
            ]
        }
    ]

    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python",
                "version": "3.10"
            },
            "accelerator": "GPU"
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"[OK] Generated notebook: {output_path}")

# 1. Plant Species Notebook
create_notebook(
    "Plant Species Identification Training Pipeline",
    "Botanical species classification (13 active species, scaling towards 10,000)",
    "plants",
    [
        "Apple (Malus domestica)", "Brinjal (Solanum melongena)", "Chilli / Pepper (Capsicum annuum)",
        "Corn / Maize (Zea mays)", "Cotton (Gossypium hirsutum)", "Cucumber (Cucumis sativus)",
        "Grape (Vitis vinifera)", "Mango (Mangifera indica)", "Potato (Solanum tuberosum)",
        "Rice / Paddy (Oryza sativa)", "Rose (Rosa rubiginosa)", "Tomato (Solanum lycopersicum)",
        "Wheat (Triticum aestivum)"
    ],
    "plant_species",
    TRAINING_DIR / "plant_species_training.ipynb"
)

# 2. Leaf Disease Notebook
create_notebook(
    "Crop Foliar Disease & Pathogen Diagnostic Training Pipeline",
    "Foliar disease classification across 39 distinct crop species and pathogen classes",
    "leaf_diseases",
    [
        "Apple___healthy", "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust",
        "Brinjal___healthy", "Brinjal___Phomopsis_blight", "Brinjal___Little_leaf",
        "Corn___healthy", "Corn___Common_rust", "Corn___Northern_Leaf_Blight",
        "Cotton___healthy", "Cotton___Bacterial_blight", "Cucumber___healthy", "Cucumber___Downy_mildew",
        "Grape___healthy", "Grape___Black_rot", "Grape___Leaf_blight", "Mango___healthy", "Mango___Anthracnose",
        "Pepper___healthy", "Pepper___Bacterial_spot", "Potato___healthy", "Potato___Early_blight", "Potato___Late_blight",
        "Rice___healthy", "Rice___Brown_Spot", "Rice___Leaf_Blast", "Rose___healthy", "Rose___Black_spot",
        "Rose___Powdery_mildew", "Tomato___healthy", "Tomato___Early_blight", "Tomato___Late_blight",
        "Tomato___Leaf_Mold", "Tomato___Bacterial_spot", "Tomato___Septoria_leaf_spot",
        "Wheat___healthy", "Wheat___Leaf_rust", "Wheat___Yellow_rust"
    ],
    "crop_disease",
    TRAINING_DIR / "leaf_disease_training.ipynb"
)

# 3. Soil Classification Notebook
create_notebook(
    "Pedological Soil Category Visual Classification Pipeline",
    "Visual surface categorization across 6 major soil classes (scaling towards 50)",
    "soil",
    [
        "Alluvial Soil", "Black Soil (Regur)", "Clay Soil", "Laterite Soil", "Red Soil", "Sandy Loam Soil"
    ],
    "soil_classifier",
    TRAINING_DIR / "soil_classification_training.ipynb"
)
