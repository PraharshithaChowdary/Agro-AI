"""Create the schema and import the bundled botanical catalogue if it is empty.

No demo users or default credentials are created. User accounts are created through
AGRO AI's registration interface.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import app.models  # noqa: F401 - register all SQLAlchemy models
from app.database import Base, SessionLocal, engine
from app.models.plant import PlantSpecies

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("agro_ai.bootstrap")


def bootstrap() -> int:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        count = db.query(PlantSpecies).count()
    finally:
        db.close()
    if count:
        logger.info("Botanical catalogue already contains %s records; leaving it unchanged.", count)
        return count

    importer_path = BACKEND_DIR / "data" / "import_plant_catalog.py"
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location("agro_ai_plant_catalog_importer", importer_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Plant catalogue importer is missing: {importer_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    total = module.import_plants()
    logger.info("Botanical catalogue ready (%s records).", total)
    return int(total or 0)

if __name__ == "__main__":
    bootstrap()
