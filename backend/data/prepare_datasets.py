"""
AGRO AI — Dataset Preparation, Leakage Prevention & Manifest Generator
Cleans, partitions, and indexes datasets into stratified Train / Validation / Test splits.
Enforces MD5 hash deduplication to eliminate train-test contamination.
"""

import os
import json
import hashlib
import random
import shutil
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
MANIFESTS_DIR = DATASETS_DIR / "manifests"

PIPELINES = {
    "plants": DATASETS_DIR / "plants",
    "leaf_diseases": DATASETS_DIR / "leaf_diseases",
    "soil": DATASETS_DIR / "soil"
}

def setup_directories():
    """Initializes the required directory structure for all three machine learning tasks."""
    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    for name, path in PIPELINES.items():
        for split in ["train", "validation", "test"]:
            (path / split).mkdir(parents=True, exist_ok=True)
    print("[OK] Dataset directory architecture initialized.")

def compute_md5(file_path: Path) -> str:
    """Computes MD5 hash of image bytes for duplicate detection."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def prepare_pipeline_splits(pipeline_key: str, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15):
    """
    Scans raw class folders, quarantines duplicates, splits into stratified sets,
    and generates an immutable manifest JSON file.
    """
    if pipeline_key not in PIPELINES:
        print(f"[ERROR] Unknown pipeline '{pipeline_key}'")
        return

    root_dir = PIPELINES[pipeline_key]
    print(f"\n--- Preparing Splits for: {pipeline_key.upper()} ---")

    seen_hashes = {}
    manifest_records = []
    class_counts = {}

    # Find all image subdirectories
    subdirs = [d for d in root_dir.glob("*") if d.is_dir() and d.name not in ["train", "validation", "test", "raw", "raw_plantvillage", "raw_plantdoc", "raw_plantclef"]]
    
    if not subdirs:
        print(f"[INFO] No unpartitioned subdirectories found in {root_dir}. Searching in raw directories...")
        subdirs = [d for d in root_dir.glob("raw*/*") if d.is_dir()]

    if not subdirs:
        print(f"[INFO] Directory {root_dir} is ready for raw datasets. Place raw class folders inside.")
        return

    total_images = 0
    duplicate_count = 0
    corrupt_count = 0

    for cdir in subdirs:
        cname = cdir.name
        class_counts[cname] = {"train": 0, "val": 0, "test": 0, "total": 0}
        valid_files = []

        for f in cdir.glob("**/*"):
            if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
                # 1. Verify Image Integrity
                try:
                    with Image.open(f) as img:
                        img.verify()
                except Exception:
                    corrupt_count += 1
                    continue

                # 2. Check MD5 hash for exact duplicate avoidance (Leakage Prevention)
                file_hash = compute_md5(f)
                if file_hash in seen_hashes:
                    duplicate_count += 1
                    continue
                seen_hashes[file_hash] = str(f)
                valid_files.append((f, file_hash))

        # Stratified Shuffle
        random.seed(42)
        random.shuffle(valid_files)

        n_total = len(valid_files)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)

        for idx, (fpath, fhash) in enumerate(valid_files):
            if idx < n_train:
                split = "train"
            elif idx < (n_train + n_val):
                split = "validation"
            else:
                split = "test"

            target_dest = root_dir / split / cname / fpath.name
            target_dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file to split destination
            shutil.copy2(fpath, target_dest)

            class_counts[cname][split] += 1
            class_counts[cname]["total"] += 1
            total_images += 1

            manifest_records.append({
                "pipeline": pipeline_key,
                "class_label": cname,
                "split": split,
                "file_path": str(target_dest.relative_to(BASE_DIR)),
                "md5_hash": fhash
            })

    # Save manifest
    manifest_file = MANIFESTS_DIR / f"{pipeline_key}_manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as mf:
        json.dump({
            "pipeline": pipeline_key,
            "total_images": total_images,
            "duplicate_quarantined": duplicate_count,
            "corrupted_quarantined": corrupt_count,
            "class_summary": class_counts,
            "records": manifest_records
        }, mf, indent=2)

    print(f"[OK] Processed {total_images} images across {len(class_counts)} classes.")
    print(f"     Quarantined: {duplicate_count} duplicates, {corrupt_count} corrupt.")
    print(f"     Manifest written to: {manifest_file}")

if __name__ == "__main__":
    setup_directories()
    for key in PIPELINES:
        prepare_pipeline_splits(key)
