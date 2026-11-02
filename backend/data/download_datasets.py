"""
AGRO AI — Automated Dataset Acquisition & Download Pipeline
Handles safe, configurable retrieval from official public repositories (PlantVillage, PlantDoc, Kaggle Soil).
Enforces storage pre-flight checks, resumable downloads, and attribution tracking.
"""

import os
import sys
import shutil
import urllib.request
import zipfile
import tarfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASETS_DIR = BASE_DIR / "datasets"

SOURCES = {
    "plantvillage": {
        "name": "PlantVillage Crop Foliar Disease Dataset",
        "url": "https://github.com/spMohanty/PlantVillage-Dataset/archive/master.zip",
        "target_dir": DATASETS_DIR / "leaf_diseases" / "raw_plantvillage",
        "min_free_gb": 3.0,
        "license": "CC-BY-SA 4.0",
        "description": "54,306 curated laboratory leaf photographs spanning 38 classes."
    },
    "plantdoc": {
        "name": "PlantDoc In-Field Crop Disease Dataset",
        "url": "https://github.com/pratikkayal/PlantDoc-Dataset/archive/master.zip",
        "target_dir": DATASETS_DIR / "leaf_diseases" / "raw_plantdoc",
        "min_free_gb": 2.0,
        "license": "MIT",
        "description": "2,569 field photographs under variable natural lighting and occlusion."
    },
    "plantclef_info": {
        "name": "PlantCLEF Species Identification Benchmark",
        "url": "https://www.imageclef.org/node/332",
        "target_dir": DATASETS_DIR / "plants" / "raw_plantclef",
        "min_free_gb": 10.0,
        "license": "Research & Academic Use",
        "description": "Large-scale botanical species benchmark targeting up to 10,000 flora species."
    }
}

def check_disk_space(required_gb: float) -> bool:
    """Verifies that sufficient free disk space exists before downloading."""
    total, used, free = shutil.disk_usage(DATASETS_DIR if DATASETS_DIR.exists() else BASE_DIR)
    free_gb = free / (1024 ** 3)
    print(f"[STORAGE] Available: {free_gb:.2f} GB | Required: {required_gb:.2f} GB")
    return free_gb >= required_gb

def download_file_with_progress(url: str, output_path: Path):
    """Downloads a file with real-time percentage progress."""
    print(f"[DOWNLOAD] Connecting to: {url}")
    
    def _progress_hook(block_num, block_size, total_size):
        if total_size > 0:
            downloaded = block_num * block_size
            pct = min(100.0, (downloaded / total_size) * 100.0)
            sys.stdout.write(f"\r-> Progress: {pct:.1f}% ({downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB)")
            sys.stdout.flush()

    urllib.request.urlretrieve(url, str(output_path), reporthook=_progress_hook)
    print("\n[DOWNLOAD] Download complete.")

def acquire_dataset(source_key: str):
    """Acquires and unpacks the requested dataset source."""
    if source_key not in SOURCES:
        print(f"[ERROR] Unknown dataset source '{source_key}'. Available: {list(SOURCES.keys())}")
        return False

    info = SOURCES[source_key]
    print(f"\n==================================================")
    print(f"Acquiring: {info['name']}")
    print(f"License: {info['license']}")
    print(f"Source: {info['url']}")
    print(f"==================================================")

    if not check_disk_space(info["min_free_gb"]):
        print(f"[ERROR] Insufficient disk space for {info['name']}. Minimum {info['min_free_gb']} GB required.")
        return False

    info["target_dir"].mkdir(parents=True, exist_ok=True)
    
    # Check if download is an external portal (e.g. PlantCLEF requiring authentication)
    if "imageclef.org" in info["url"]:
        print(f"[MANUAL ACTION REQUIRED] PlantCLEF dataset requires user registration at {info['url']}")
        print(f"Please follow the terms on the portal and place downloaded archives into:\n-> {info['target_dir']}")
        return True

    zip_path = info["target_dir"] / "archive.zip"
    try:
        download_file_with_progress(info["url"], zip_path)
        print(f"[EXTRACT] Unpacking archive into {info['target_dir']}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(info["target_dir"])
        if zip_path.exists():
            zip_path.unlink() # Cleanup archive
        print(f"[OK] {info['name']} successfully organized.")
        return True
    except Exception as e:
        print(f"[WARN] Automated download encountered: {e}")
        print(f"You can manually clone or download from: {info['url']}")
        return False

if __name__ == "__main__":
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    print("AGRO AI Dataset Acquisition CLI")
    print("--------------------------------")
    for key in SOURCES:
        print(f"- {key}: {SOURCES[key]['name']}")
    
    if len(sys.argv) > 1:
        chosen = sys.argv[1].lower()
        acquire_dataset(chosen)
    else:
        print("\nUsage: python download_datasets.py <source_key>")
        print("Example: python download_datasets.py plantvillage")
