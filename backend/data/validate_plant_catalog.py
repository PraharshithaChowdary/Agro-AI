"""
AGRO AI — Indian Plant Catalog Validator
Validates JSON plant catalog files against backend/data/plant_catalog_schema.json.
Checks required fields, valid enums, non-empty attributes, and data integrity.
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_FILE = BASE_DIR / "plant_catalog_schema.json"
CATALOG_DIR = BASE_DIR / "plant_catalog"

REQUIRED_FIELDS = [
    "id",
    "scientific_name",
    "common_name",
    "family",
    "genus",
    "species",
    "category",
    "status_in_india",
    "verification_status"
]

VALID_CATEGORIES = {
    "crop",
    "fruit plant",
    "vegetable",
    "herb",
    "medicinal plant",
    "tree",
    "shrub",
    "flower",
    "ornamental",
    "grass",
    "weed",
    "spice",
    "pulse",
    "oilseed",
    "plantation",
    "other"
}

VALID_STATUSES = {"native", "naturalized", "cultivated", "invasive", "unknown"}
VALID_VERIFICATION = {"verified", "provisional", "pending_review"}

def validate_record(record: dict, filename: str, idx: int) -> list:
    errors = []
    pid = record.get("id", f"<index-{idx}>")
    
    # 1. Required fields
    for field in REQUIRED_FIELDS:
        if field not in record or record[field] is None or record[field] == "":
            errors.append(f"[{filename} - {pid}] Missing required field: '{field}'")

    # 2. Category enum
    cat = record.get("category")
    if cat and cat not in VALID_CATEGORIES:
        errors.append(f"[{filename} - {pid}] Invalid category '{cat}'. Expected one of {sorted(VALID_CATEGORIES)}")

    # 3. Status enum
    st = record.get("status_in_india")
    if st and st not in VALID_STATUSES:
        errors.append(f"[{filename} - {pid}] Invalid status_in_india '{st}'. Expected one of {sorted(VALID_STATUSES)}")

    # 4. Verification enum
    ver = record.get("verification_status")
    if ver and ver not in VALID_VERIFICATION:
        errors.append(f"[{filename} - {pid}] Invalid verification_status '{ver}'. Expected one of {sorted(VALID_VERIFICATION)}")

    # 5. Scientific name format (at least binomial)
    sci = record.get("scientific_name", "")
    if len(sci.split()) < 2:
        errors.append(f"[{filename} - {pid}] Scientific name '{sci}' should contain at least genus and species.")

    return errors

def validate_all() -> bool:
    if not CATALOG_DIR.exists():
        print(f"[ERROR] Catalog directory not found: {CATALOG_DIR}")
        return False

    all_errors = []
    total_records = 0
    seen_ids = set()
    seen_scientific = set()

    json_files = list(CATALOG_DIR.glob("*.json"))
    if not json_files:
        print(f"[ERROR] No JSON files found in {CATALOG_DIR}")
        return False

    print(f"[INFO] Validating plant catalog across {len(json_files)} files...")

    for jf in json_files:
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            all_errors.append(f"[JSON ERROR] Failed to parse {jf.name}: {e}")
            continue

        if not isinstance(data, list):
            all_errors.append(f"[SCHEMA ERROR] {jf.name} root must be a JSON list of records.")
            continue

        for i, item in enumerate(data):
            total_records += 1
            errs = validate_record(item, jf.name, i)
            all_errors.extend(errs)

            # Check uniqueness
            pid = item.get("id")
            if pid:
                if pid in seen_ids:
                    all_errors.append(f"[{jf.name}] Duplicate plant ID detected: '{pid}'")
                seen_ids.add(pid)

            sci = item.get("scientific_name", "").lower()
            if sci:
                if sci in seen_scientific:
                    all_errors.append(f"[{jf.name}] Duplicate scientific name detected: '{item.get('scientific_name')}'")
                seen_scientific.add(sci)

    if all_errors:
        print(f"[FAILED] Found {len(all_errors)} validation errors across {total_records} records:")
        for err in all_errors[:20]:
            print(f"  - {err}")
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors) - 20} more errors.")
        return False
    else:
        print(f"[SUCCESS] All {total_records} plant records passed validation with 0 errors!")
        print(f"[STATS] Unique species: {len(seen_scientific)} | Unique IDs: {len(seen_ids)}")
        return True

if __name__ == "__main__":
    success = validate_all()
    sys.exit(0 if success else 1)
