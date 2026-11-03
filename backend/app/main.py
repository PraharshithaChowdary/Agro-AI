from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
import logging
import threading

from app.config import settings
from app.database import engine, Base
import app.models  # Import all models for declarative base reflection
from app.api import auth, production, nutrition, assistant, plants

# Create database tables automatically
Base.metadata.create_all(bind=engine)

logger = logging.getLogger("agro_ai.startup")

app = FastAPI(
    title=settings.APP_NAME,
    description="AGRO AI — Smart Agriculture. Healthy Lives. Better Future. High-performance REST API for crop & soil vision diagnosis, scientific nutrition planning, and agricultural knowledge assistant.",
    version="1.0.0",
)

@app.on_event("startup")
def bootstrap_plant_catalogue_if_needed():
    """Seed the bundled botanical catalogue only on a fresh database."""
    try:
        from app.models.plant import PlantSpecies
        from app.database import SessionLocal
        with SessionLocal() as db:
            catalogue_count = db.query(PlantSpecies).count()
        if catalogue_count == 0:
            from pathlib import Path
            import subprocess
            bootstrap_script = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap_database.py"
            logger.info("Empty botanical catalogue; importing the bundled seed manifest.")
            subprocess.run([os.sys.executable, str(bootstrap_script)], check=True, timeout=180)
        else:
            logger.info("Botanical catalogue ready: %s records.", catalogue_count)
    except Exception:
        logger.exception("Could not seed botanical catalogue. Plant search may be empty until backend/scripts/bootstrap_database.py is run.")

@app.on_event("startup")
def warm_image_analysis_model():
    """Warm image inference in the background; API startup stays available immediately."""
    from app.services.ollama_service import OllamaService
    threading.Thread(
        target=lambda: (OllamaService.preload_vision_model(), OllamaService.preload_chat_model()),
        name="agro-image-report-warmup",
        daemon=True,
    ).start()

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router)
app.include_router(plants.router)
app.include_router(production.router)
app.include_router(nutrition.router)
app.include_router(assistant.router)

@app.get("/api/health", tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "tagline": settings.APP_TAGLINE,
        "environment": settings.ENVIRONMENT,
        "features": [
            "Better Production (Crop & Soil Vision ML)",
            "Better Nutrition (BMR/TDEE & 7-Day Diet Planner)",
            "AGRO AI Assistant (Zero External Paid AI APIs)"
        ]
    }

@app.get("/api/ollama/status", tags=["General"])
def ollama_status():
    """Return safe readiness booleans without exposing internal model IDs."""
    from app.services.ollama_service import OllamaService
    data = OllamaService.status()
    return {
        "connected": bool(data.get("connected")),
        "visionReady": bool(data.get("visionReady")),
        "chatReady": bool(data.get("chatReady")),
        "ready": bool(data.get("ready")),
        "message": data.get("message", "Local AI status unavailable."),
    }

@app.get("/api/datasets/download-pdf", tags=["Datasets"])
def download_datasets_pdf():
    """Download the complete AGRO AI Training Datasets Specification PDF."""
    pdf_path = Path(__file__).resolve().parents[2] / "datasets" / "AGRO_AI_Training_Datasets_Documentation.pdf"
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="Datasets documentation PDF not found.")
    return FileResponse(
        path=str(pdf_path),
        filename="AGRO_AI_Training_Datasets_Documentation.pdf",
        media_type="application/pdf"
    )

@app.get("/api/datasets/download/{filename}", tags=["Datasets"])
def download_dataset_file(filename: str):
    """Download any training dataset CSV or documentation PDF."""
    allowed_files = {
        "agricultural_relevance": "agricultural_relevance_dataset.csv",
        "crop_disease": "crop_disease_dataset.csv",
        "plant_species": "plant_species_dataset.csv",
        "soil_pedological": "soil_pedological_dataset.csv",
        "documentation_pdf": "AGRO_AI_Training_Datasets_Documentation.pdf",
    }
    clean_name = filename.lower().replace(".csv", "").replace(".pdf", "")
    target_file = allowed_files.get(clean_name) or allowed_files.get(filename)
    if not target_file:
        raise HTTPException(status_code=404, detail="Dataset file not found.")
    file_path = Path(__file__).resolve().parents[2] / "datasets" / target_file
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File {target_file} not found on disk.")
    media_type = "application/pdf" if target_file.endswith(".pdf") else "text/csv"
    return FileResponse(path=str(file_path), filename=target_file, media_type=media_type)

@app.get("/", tags=["General"])
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API. Visit /docs for interactive Swagger API documentation.",
        "tagline": settings.APP_TAGLINE,
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
