"""
AGRO AI — Dataset Preparation Script
Downloads, organizes, inspects, and splits public datasets for:
1. Agricultural Relevance (agriculture vs non_agriculture)
2. Crop & Foliar Disease Classification (PlantVillage / PlantDoc)
3. Soil Category Classification
"""

import os
import shutil
import hashlib
from pathlib import Path
from PIL import Image
import numpy as np

BASE_DATASET_DIR = Path(__file__).resolve().parent.parent / "datasets"

DIRS = {
    "relevance_agri": BASE_DATASET_DIR / "agricultural_relevance" / "agriculture",
    "relevance_non_agri": BASE_DATASET_DIR / "agricultural_relevance" / "non_agriculture",
    "crop_train": BASE_DATASET_DIR / "crop_disease" / "train",
    "crop_val": BASE_DATASET_DIR / "crop_disease" / "validation",
    "crop_test": BASE_DATASET_DIR / "crop_disease" / "test",
    "soil_train": BASE_DATASET_DIR / "soil" / "train",
    "soil_val": BASE_DATASET_DIR / "soil" / "validation",
    "soil_test": BASE_DATASET_DIR / "soil" / "test",
}

def setup_directory_structure():
    print("Creating dataset directory structure...")
    for path in DIRS.values():
        path.mkdir(parents=True, exist_ok=True)
    print("[OK] Dataset directories initialized.")

def verify_image_integrity(folder_path: Path):
    """
    Checks for corrupted or unreadable images in a directory.
    """
    corrupted = []
    total = 0
    for root, _, files in os.walk(folder_path):
        for f in files:
            file_path = Path(root) / f
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                total += 1
                try:
                    with Image.open(file_path) as img:
                        img.verify()
                except Exception:
                    corrupted.append(file_path)
    
    print(f"Inspection for {folder_path.name}: {total} images found, {len(corrupted)} corrupted.")
    return corrupted

def remove_duplicates_via_hash(folder_path: Path):
    """
    Finds and quarantines identical duplicate images using MD5 hashing.
    """
    hashes = {}
    duplicates = []
    for root, _, files in os.walk(folder_path):
        for f in files:
            file_path = Path(root) / f
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                try:
                    with open(file_path, "rb") as fp:
                        file_hash = hashlib.md5(fp.read()).hexdigest()
                    if file_hash in hashes:
                        duplicates.append(file_path)
                    else:
                        hashes[file_hash] = file_path
                except Exception:
                    pass
    print(f"Duplicate check for {folder_path.name}: Found {len(duplicates)} duplicates.")
    return duplicates

if __name__ == "__main__":
    setup_directory_structure()
    print("\nDataset preparation script ready. Place raw downloaded datasets into:")
    print(f"-> {BASE_DATASET_DIR}")
