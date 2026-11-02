"""
AGRO AI — Large-Scale Botanical Dataset Preparation & Validation Pipeline
========================================================================
Handles dataset downloading, class normalization, image integrity verification,
duplicate removal, stratified splitting (Train/Val/Test), and class mapping export
for AGRO AI's multi-species plant identification system.

Targets 50+ botanical species spanning Indian crops, medicinal plants, fruit trees,
and flowers (including Rose, Tulsi, Neem, Mango, Corn, Tomato, Guava, Hibiscus).
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from PIL import Image

# Canonical Mapping from diverse raw dataset folder names to standard binomial slugs
SPECIES_SLUG_MAP: Dict[str, str] = {
    # --- Indian Medicinal & Tree Plants ---
    "neem": "azadirachta-indica",
    "azadirachta indica": "azadirachta-indica",
    "azadirachta_indica": "azadirachta-indica",
    "tulsi": "ocimum-tenuiflorum",
    "holy basil": "ocimum-tenuiflorum",
    "ocimum sanctum": "ocimum-tenuiflorum",
    "ocimum_sanctum": "ocimum-tenuiflorum",
    "ocimum tenuiflorum": "ocimum-tenuiflorum",
    "ocimum_tenuiflorum": "ocimum-tenuiflorum",
    "mango": "mangifera-indica",
    "mangifera indica": "mangifera-indica",
    "mangifera_indica": "mangifera-indica",
    "guava": "psidium-guajava",
    "psidium guajava": "psidium-guajava",
    "psidium_guajava": "psidium-guajava",
    "mint": "mentha-arvensis",
    "pudina": "mentha-arvensis",
    "mentha": "mentha-arvensis",
    "peepal": "ficus-religiosa",
    "ficus religiosa": "ficus-religiosa",
    "ficus_religiosa": "ficus-religiosa",
    "banyan": "ficus-benghalensis",
    "ficus benghalensis": "ficus-benghalensis",
    "ficus_benghalensis": "ficus-benghalensis",
    "hibiscus": "hibiscus-rosa-sinensis",
    "china rose": "hibiscus-rosa-sinensis",
    "hibiscus rosa-sinensis": "hibiscus-rosa-sinensis",
    "hibiscus_rosa-sinensis": "hibiscus-rosa-sinensis",
    "papaya": "carica-papaya",
    "carica papaya": "carica-papaya",
    "carica_papaya": "carica-papaya",
    "lemon": "citrus-limon",
    "citrus limon": "citrus-limon",
    "citrus_limon": "citrus-limon",
    "pomegranate": "punica-granatum",
    "punica granatum": "punica-granatum",
    "punica_granatum": "punica-granatum",
    "aloe vera": "aloe-barbadensis",
    "aloe_vera": "aloe-barbadensis",
    "jamun": "syzygium-cumini",
    "syzygium cumini": "syzygium-cumini",
    "syzygium_cumini": "syzygium-cumini",
    "curry leaf": "murraya-koenigii",
    "murraya koenigii": "murraya-koenigii",
    "murraya_koenigii": "murraya-koenigii",
    "betel": "piper-betle",
    "paan": "piper-betle",
    "piper betle": "piper-betle",
    "piper_betle": "piper-betle",
    "drumstick": "moringa-oleifera",
    "moringa": "moringa-oleifera",
    "moringa oleifera": "moringa-oleifera",
    "amla": "phyllanthus-emblica",
    "emblica officinalis": "phyllanthus-emblica",
    "emblica_officinalis": "phyllanthus-emblica",
    "phyllanthus emblica": "phyllanthus-emblica",
    "phyllanthus_emblica": "phyllanthus-emblica",
    "periwinkle": "catharanthus-roseus",
    "sadabahar": "catharanthus-roseus",
    "catharanthus roseus": "catharanthus-roseus",

    # --- Flowers ---
    "rose": "rosa-indica",
    "rosa": "rosa-indica",
    "rosa indica": "rosa-indica",
    "rosa_indica": "rosa-indica",
    "roses": "rosa-indica",
    "sunflower": "helianthus-annuus",
    "helianthus annuus": "helianthus-annuus",
    "marigold": "tagetes-erecta",
    "tagetes erecta": "tagetes-erecta",
    "jasmine": "jasminum-sambac",
    "jasminum sambac": "jasminum-sambac",
    "lotus": "nelumbo-nucifera",
    "nelumbo nucifera": "nelumbo-nucifera",

    # --- Crops & Agricultural Produce (PlantVillage & Standard) ---
    "corn": "zea-mays",
    "maize": "zea-mays",
    "zea mays": "zea-mays",
    "zea_mays": "zea-mays",
    "corn_(maize)___healthy": "zea-mays",
    "corn_(maize)___common_rust": "zea-mays",
    "corn_(maize)___northern_leaf_blight": "zea-mays",
    "tomato": "solanum-lycopersicum",
    "solanum lycopersicum": "solanum-lycopersicum",
    "solanum_lycopersicum": "solanum-lycopersicum",
    "tomato___healthy": "solanum-lycopersicum",
    "tomato___early_blight": "solanum-lycopersicum",
    "tomato___late_blight": "solanum-lycopersicum",
    "potato": "solanum-tuberosum",
    "solanum tuberosum": "solanum-tuberosum",
    "solanum_tuberosum": "solanum-tuberosum",
    "potato___healthy": "solanum-tuberosum",
    "potato___early_blight": "solanum-tuberosum",
    "potato___late_blight": "solanum-tuberosum",
    "bell pepper": "capsicum-annuum",
    "pepper": "capsicum-annuum",
    "capsicum annuum": "capsicum-annuum",
    "capsicum_annuum": "capsicum-annuum",
    "pepper,_bell___healthy": "capsicum-annuum",
    "pepper,_bell___bacterial_spot": "capsicum-annuum",
    "orange": "citrus-sinensis",
    "sweet orange": "citrus-sinensis",
    "citrus sinensis": "citrus-sinensis",
    "citrus_sinensis": "citrus-sinensis",
    "orange___haunglongbing_(citrus_greening)": "citrus-sinensis",
    "apple": "malus-domestica",
    "malus domestica": "malus-domestica",
    "malus_domestica": "malus-domestica",
    "apple___healthy": "malus-domestica",
    "apple___apple_scab": "malus-domestica",
    "grape": "vitis-vinifera",
    "vitis vinifera": "vitis-vinifera",
    "vitis_vinifera": "vitis-vinifera",
    "grape___healthy": "vitis-vinifera",
    "grape___black_rot": "vitis-vinifera",
    "soybean": "glycine-max",
    "glycine max": "glycine-max",
    "glycine_max": "glycine-max",
    "soybean___healthy": "glycine-max",
    "squash": "cucurbita-pepo",
    "pumpkin": "cucurbita-pepo",
    "cucurbita pepo": "cucurbita-pepo",
    "cucurbita_pepo": "cucurbita-pepo",
    "squash___powdery_mildew": "cucurbita-pepo",
    "strawberry": "fragaria-ananassa",
    "fragaria ananassa": "fragaria-ananassa",
    "fragaria_ananassa": "fragaria-ananassa",
    "strawberry___healthy": "fragaria-ananassa",
    "peach": "prunus-persica",
    "prunus persica": "prunus-persica",
    "prunus_persica": "prunus-persica",
    "peach___healthy": "prunus-persica",
    "cherry": "prunus-avium",
    "prunus avium": "prunus-avium",
    "prunus_avium": "prunus-avium",
    "cherry_(including_sour)___healthy": "prunus-avium",
    "raspberry": "rubus-idaeus",
    "rubus idaeus": "rubus-idaeus",
    "rubus_idaeus": "rubus-idaeus",
    "raspberry___healthy": "rubus-idaeus",
    "blueberry": "vaccinium-corymbosum",
    "vaccinium corymbosum": "vaccinium-corymbosum",
    "vaccinium_corymbosum": "vaccinium-corymbosum",
    "blueberry___healthy": "vaccinium-corymbosum"
}

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


class PlantDatasetPipeline:
    """
    Complete dataset curation, cleaning, verification, and train/val/test splitting pipeline.
    """

    @staticmethod
    def normalize_class_name(raw_name: str) -> str:
        """
        Maps arbitrary folder names to canonical binomial slugs.
        e.g. 'Neem (Azadirachta indica)' -> 'azadirachta-indica'
        """
        clean = raw_name.strip().lower()
        # Direct lookup
        if clean in SPECIES_SLUG_MAP:
            return SPECIES_SLUG_MAP[clean]
        
        # Substring matching
        for k, slug in SPECIES_SLUG_MAP.items():
            if k in clean or clean in k:
                return slug
        
        # Fallback to sanitized slug
        sanitized = clean.replace(" ", "-").replace("_", "-").replace("(", "").replace(")", "")
        return sanitized

    @staticmethod
    def compute_file_hash(path: Path) -> Optional[str]:
        """Calculates MD5 hash for duplicate detection."""
        try:
            with open(path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return None

    @classmethod
    def audit_dataset_folder(cls, folder_path: Path) -> Dict[str, Any]:
        """
        Audits a dataset directory: counts species, detects corrupt files,
        finds duplicates, and checks minimum class sizes.
        """
        if not folder_path.exists():
            return {
                "exists": False,
                "error": f"Path '{folder_path}' does not exist.",
                "total_images": 0,
                "total_classes": 0
            }

        classes = sorted([d.name for d in folder_path.iterdir() if d.is_dir()])
        class_counts = {}
        corrupted_files = []
        duplicate_hashes = {}
        duplicates = []
        total_images = 0

        for c in classes:
            c_dir = folder_path / c
            img_files = [f for f in c_dir.iterdir() if f.is_file() and f.suffix.lower() in VALID_EXTENSIONS]
            class_counts[c] = len(img_files)
            total_images += len(img_files)

            for f in img_files:
                # Check readability
                try:
                    with Image.open(f) as img:
                        img.verify()
                except Exception:
                    corrupted_files.append(str(f))
                    continue

                # Check duplicates
                f_hash = cls.compute_file_hash(f)
                if f_hash:
                    if f_hash in duplicate_hashes:
                        duplicates.append((str(f), duplicate_hashes[f_hash]))
                    else:
                        duplicate_hashes[f_hash] = str(f)

        empty_classes = [c for c, count in class_counts.items() if count == 0]
        small_classes = [c for c, count in class_counts.items() if 0 < count < 15]

        return {
            "exists": True,
            "path": str(folder_path),
            "total_classes": len(classes),
            "total_images": total_images,
            "classes": classes,
            "class_counts": class_counts,
            "empty_classes": empty_classes,
            "small_classes": small_classes,
            "corrupted_count": len(corrupted_files),
            "corrupted_files": corrupted_files[:10],
            "duplicate_count": len(duplicates),
            "duplicates_sample": duplicates[:5]
        }

    @classmethod
    def import_and_organize_raw_dataset(
        cls,
        source_dir: Path,
        target_dir: Path,
        min_images_per_class: int = 10,
        remove_duplicates: bool = True
    ) -> Dict[str, Any]:
        """
        Imports images from an unorganized or raw dataset folder,
        normalizes class names into canonical slugs, removes duplicates/corrupt files,
        and saves organized classes into target_dir.
        """
        source_dir = Path(source_dir)
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)

        if not source_dir.exists():
            return {"success": False, "error": f"Source directory {source_dir} not found."}

        imported_stats = {}
        class_seen_hashes = {}
        skipped_corrupt = 0
        skipped_duplicates = 0
        total_copied = 0

        # Scan all directories in source
        raw_folders = [d for d in source_dir.iterdir() if d.is_dir()]
        print(f"[INFO] Scanning {len(raw_folders)} source folders in {source_dir.name}...")

        for folder in raw_folders:
            slug = cls.normalize_class_name(folder.name)
            class_target = target_dir / slug
            class_target.mkdir(parents=True, exist_ok=True)

            if slug not in imported_stats:
                imported_stats[slug] = 0
                class_seen_hashes[slug] = set()

            for img_file in folder.iterdir():
                if not img_file.is_file() or img_file.suffix.lower() not in VALID_EXTENSIONS:
                    continue

                # Verify image readability
                try:
                    with Image.open(img_file) as img:
                        img.verify()
                except Exception:
                    skipped_corrupt += 1
                    continue

                # Hash duplicate check within class
                if remove_duplicates:
                    h = cls.compute_file_hash(img_file)
                    if not h or h in class_seen_hashes[slug]:
                        skipped_duplicates += 1
                        continue
                    class_seen_hashes[slug].add(h)

                # Copy with clean sequential name
                imported_stats[slug] += 1
                new_name = f"{slug}_{imported_stats[slug]:05d}{img_file.suffix.lower()}"
                shutil.copy2(img_file, class_target / new_name)
                total_copied += 1

        # Prune classes with fewer than min_images_per_class
        pruned_classes = []
        for slug, count in list(imported_stats.items()):
            if count < min_images_per_class:
                pruned_classes.append(slug)
                shutil.rmtree(target_dir / slug, ignore_errors=True)
                del imported_stats[slug]

        return {
            "success": True,
            "organized_classes": len(imported_stats),
            "total_images": total_copied,
            "class_counts": imported_stats,
            "skipped_corrupt": skipped_corrupt,
            "skipped_duplicates": skipped_duplicates,
            "pruned_classes": pruned_classes
        }

    @classmethod
    def create_stratified_split(
        cls,
        source_classes_dir: Path,
        output_dir: Path,
        train_ratio: float = 0.70,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        seed: int = 42
    ) -> Dict[str, Any]:
        """
        Creates strictly reproducible Train / Validation / Test stratified splits.
        """
        import random
        random.seed(seed)

        source_classes_dir = Path(source_classes_dir)
        output_dir = Path(output_dir)

        train_dir = output_dir / "train"
        val_dir = output_dir / "validation"
        test_dir = output_dir / "test"

        for p in [train_dir, val_dir, test_dir]:
            p.mkdir(parents=True, exist_ok=True)

        classes = sorted([d.name for d in source_classes_dir.iterdir() if d.is_dir()])
        split_summary = {"train": 0, "val": 0, "test": 0, "classes": len(classes)}

        for c in classes:
            (train_dir / c).mkdir(exist_ok=True)
            (val_dir / c).mkdir(exist_ok=True)
            (test_dir / c).mkdir(exist_ok=True)

            img_files = sorted([f for f in (source_classes_dir / c).iterdir() if f.is_file() and f.suffix.lower() in VALID_EXTENSIONS])
            random.shuffle(img_files)

            n_total = len(img_files)
            n_train = int(n_total * train_ratio)
            n_val = int(n_total * val_ratio)

            train_imgs = img_files[:n_train]
            val_imgs = img_files[n_train:n_train + n_val]
            test_imgs = img_files[n_train + n_val:]

            for f in train_imgs:
                shutil.copy2(f, train_dir / c / f.name)
            for f in val_imgs:
                shutil.copy2(f, val_dir / c / f.name)
            for f in test_imgs:
                shutil.copy2(f, test_dir / c / f.name)

            split_summary["train"] += len(train_imgs)
            split_summary["val"] += len(val_imgs)
            split_summary["test"] += len(test_imgs)

        # Export exact plant_classes.json matching this split
        classes_file = output_dir / "plant_classes.json"
        with open(classes_file, "w", encoding="utf-8") as f:
            json.dump(classes, f, indent=2)

        split_summary["plant_classes_file"] = str(classes_file)
        split_summary["class_list"] = classes
        return split_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AGRO AI Plant Dataset Pipeline")
    parser.add_argument("--audit", type=str, help="Audit an existing dataset directory")
    parser.add_argument("--organize-from", type=str, help="Raw dataset folder to organize")
    parser.add_argument("--target-dir", type=str, default="datasets/plant_species_organized", help="Target organized directory")
    parser.add_argument("--split-from", type=str, help="Directory to split into train/val/test")
    parser.add_argument("--split-to", type=str, default="datasets/plant_species_split", help="Output split directory")

    args = parser.parse_args()

    if args.audit:
        res = PlantDatasetPipeline.audit_dataset_folder(Path(args.audit))
        print(json.dumps(res, indent=2))
    elif args.organize_from:
        res = PlantDatasetPipeline.import_and_organize_raw_dataset(Path(args.organize_from), Path(args.target_dir))
        print(json.dumps(res, indent=2))
    elif args.split_from:
        res = PlantDatasetPipeline.create_stratified_split(Path(args.split_from), Path(args.split_to))
        print(json.dumps(res, indent=2))
    else:
        print("[INFO] Plant Dataset Pipeline module loaded. Run with --audit, --organize-from, or --split-from.")
