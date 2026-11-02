from typing import Optional, List, Dict, Any
import uuid
import json
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, HTTPException, status
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.database import get_db
from app.models.plant_analysis import PlantAnalysisHistory
from app.models.user import User
from app.api.auth import get_current_user_optional, get_current_user
from app.services.image_validation import AgriculturalRelevanceService
from app.services.plant_identifier_service import PlantIdentifierService
from app.services.ollama_service import OllamaNotReadyError, OllamaServiceError
from app.services.ollama_reports import identification_report, health_report
from app.schemas.plants import (
    PlantSearchResponse,
    PlantCategoryCount,
    PlantIdentificationOut,
    PlantHealthAnalysisOut,
    PlantAutocompleteItem
)

router = APIRouter(prefix="/api/plants", tags=["Indian Plant Explorer & Health Analyzer"])

@router.get("/autocomplete", response_model=List[PlantAutocompleteItem])
def autocomplete_plants(
    q: str = Query(..., min_length=1, description="Search term matching scientific, common, Hindi, Telugu, or Tamil names"),
    limit: int = Query(10, ge=1, le=25, description="Max suggestions returned"),
    db: Session = Depends(get_db)
):
    """
    Instant Google-style botanical autocomplete across 10,000+ species.
    Matches partial prefixes, scientific binomials, English names, and Indian regional vernaculars.
    """
    return PlantIdentifierService.autocomplete_plants(query=q, limit=limit, db=db)

@router.get("/search", response_model=PlantSearchResponse)
def search_plants(
    q: Optional[str] = Query(None, description="Search term matching scientific name, common English, Hindi, Telugu, Tamil, or regional names"),
    category: Optional[str] = Query(None, description="Filter by category (crop, vegetable, fruit plant, medicinal plant, etc.)"),
    state: Optional[str] = Query(None, description="Filter by Indian state or region"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Records per page"),
    db: Session = Depends(get_db)
):
    """
    Search Indian plant species database with pagination, text matching, and category filtering.
    """
    return PlantIdentifierService.search_plants(
        query=q,
        category=category,
        state=state,
        page=page,
        limit=limit,
        db=db
    )

@router.get("/categories", response_model=List[PlantCategoryCount])
def get_categories(db: Session = Depends(get_db)):
    """
    Returns distinct plant categories and count of records in each.
    """
    return PlantIdentifierService.get_categories(db=db)

@router.get("/stats")
def get_catalog_stats(db: Session = Depends(get_db)):
    """
    Returns high-level catalog statistics (total species, poisonous species count, target progress).
    """
    return PlantIdentifierService.get_catalog_stats(db=db)

@router.get("/history")
def get_plant_analysis_history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Return only the signed-in user's plant-identification and health-analysis history."""
    rows = (db.query(PlantAnalysisHistory)
        .filter(PlantAnalysisHistory.user_id == user.id)
        .order_by(PlantAnalysisHistory.created_at.desc())
        .limit(50).all())
    return [row.to_dict() for row in rows]


@router.get("/{plant_id}")
def get_plant_details(plant_id: str, db: Session = Depends(get_db)):
    """
    Retrieves full verified botanical record, taxonomy, growing guide, uses, and disease profiles.
    """
    details = PlantIdentifierService.get_plant_details(plant_id=plant_id, db=db)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plant record '{plant_id}' not found in database."
        )
    return details

@router.post("/identify", response_model=PlantIdentificationOut)
async def identify_plant(
    image: UploadFile = File(...),
    plant_name: Optional[str] = Form(None),
    organ: Optional[str] = Form("leaf"),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Indian Plant Explorer & Visual Identifier:
    - Mode A: Automatic image identification returning up to five candidate species with uncalibrated model scores.
    - Mode B: Identification assisted by user plant name with morphological consistency verification.
    """
    image_bytes = await image.read()
    valid_image, validation_message = AgriculturalRelevanceService.validate_image_file(image_bytes, max_size_mb=15)
    if not valid_image:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=validation_message)
    try:
        res = await run_in_threadpool(identification_report, image_bytes, plant_name, organ, db)
    except OllamaNotReadyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except OllamaServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    if res.get("_wrong_module"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res["_wrong_module"])
    if not res.get("success", False) or not res.get("isAgricultural", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.get("error") or res.get("rejectionReason") or "Uploaded image does not appear to contain recognizable agricultural or botanical flora."
        )
    res["savedToAccount"] = bool(user)
    res["persistenceMessage"] = "Saved to your account history." if user else "Preview only — sign in to save this result to your account."
    if user:
        try:
            row = PlantAnalysisHistory(
                id=str(uuid.uuid4()), user_id=user.id, analysis_type="identification",
                image_filename=image.filename, plant_name=plant_name or None,
                organ=res.get("detectedOrgan") or organ or "leaf",
                result_json=json.dumps(res, ensure_ascii=False)
            )
            db.add(row)
            db.commit()
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail="Plant identification completed but could not be saved to your account.") from exc
    return res

@router.post("/analyze-health", response_model=PlantHealthAnalysisOut)
async def analyze_plant_health(
    image: UploadFile = File(...),
    plant_id: Optional[str] = Form(None),
    plant_name: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Dedicated Plant Health Analysis Pipeline:
    Extracts observable symptoms (chlorosis, necrotic spots, mildew), evaluates overall health score,
    applies available crop disease screening when supported; real-photo validation is not established, and delivers 4-5 verified actionable management practices.
    """
    image_bytes = await image.read()
    valid_image, validation_message = AgriculturalRelevanceService.validate_image_file(image_bytes, max_size_mb=15)
    if not valid_image:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=validation_message)
    try:
        res = await run_in_threadpool(health_report, image_bytes, plant_id, plant_name, db)
    except OllamaNotReadyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except OllamaServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    if not res.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.get("error", "Plant health analysis could not be completed.")
        )
    res["savedToAccount"] = bool(user)
    res["persistenceMessage"] = "Saved to your account history." if user else "Preview only — sign in to save this result to your account."
    if user:
        try:
            row = PlantAnalysisHistory(
                id=str(uuid.uuid4()), user_id=user.id, analysis_type="health",
                image_filename=image.filename, plant_name=plant_name or plant_id,
                organ=res.get("detectedOrgan"), result_json=json.dumps(res, ensure_ascii=False)
            )
            db.add(row)
            db.commit()
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail="Plant health analysis completed but could not be saved to your account.") from exc
    return res
