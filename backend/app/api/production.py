import uuid
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.database import get_db
from app.config import settings
from app.models.production import ProductionAnalysis
from app.models.user import User
from app.api.auth import get_current_user_optional, get_current_user
from app.services.image_validation import AgriculturalRelevanceService
from app.services.crop_inference import CropInferenceService
from app.services.soil_inference import SoilInferenceService
from app.services.plant_health_service import PlantHealthByNameService
from app.services.ollama_service import OllamaNotReadyError, OllamaServiceError
from app.services.ollama_reports import named_plant_report, crop_report, soil_report
from app.schemas.production import (
    CropAnalysisOut,
    SoilAnalysisOut,
    RelevanceCheckOut,
    NamedPlantAnalysisOut,
    SupportedPlantItem,
    IndianSoilItem
)

router = APIRouter(prefix="/api/production", tags=["Better Production"])

def _append_role_guidance(result: dict, user: User, module: str) -> None:
    """Append practical next steps for the authenticated account role without changing model scores."""
    role = user.get_role_value()
    if role == "farmer":
        note = "For farm decisions: use this as preliminary screening, compare symptoms in the field, and confirm uncertain cases with a local KVK/agricultural extension officer before treatment."
    elif role == "buyer":
        note = "For procurement: do not accept/reject a lot or set a price from this image result alone. Inspect a representative sample and verify grade, moisture, storage, and traceability separately."
    elif role == "general":
        note = "For learning: this is an educational visual screening result, not a certified diagnosis or soil laboratory report."
    else:
        note = "Review the screening limitation and confirm high-impact decisions independently."
    if module in {"crop", "named_plant"}:
        result["disclaimer"] = (result.get("disclaimer", "") + " " + note).strip()
        result["explanation"] = (result.get("explanation", "") + "\n\n" + note).strip()
    elif module == "soil":
        result["limitationsDisclaimer"] = (result.get("limitationsDisclaimer", "") + " " + note).strip()


@router.get("/health")
def production_health():
    return {
        "status": "online",
        "service": "Better Production Vision Service",
        "supported_analyses": ["plant_health_by_name", "crop_disease", "soil_category", "agricultural_relevance"]
    }

@router.get("/supported-plants", response_model=List[SupportedPlantItem])
def get_supported_plants():
    """
    Returns the catalogue of recognized plants with care profiles, Hindi names, seasons, and model training status.
    """
    return PlantHealthByNameService.get_supported_plants_list()

@router.get("/soil-types", response_model=List[IndianSoilItem])
def get_soil_types():
    """
    Returns the catalogue of all 12 ICAR Indian Soil Types with characteristics, geography, and suitable crops.
    """
    return SoilInferenceService.get_all_soil_types()

@router.post("/analyze-named-plant", response_model=NamedPlantAnalysisOut)
async def analyze_named_plant(
    image: UploadFile = File(...),
    plant_name: str = Form(...),
    crop_type: Optional[str] = Form(None),
    growing_location: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Analyse My Plant (Plant Health Analysis by Name):
    Accepts plant image + user-provided plant name, detects visible symptoms (chlorosis, necrosis, mildew),
    evaluates plant health status, runs disease classifier when supported, and returns verified care guidance.
    """
    image_bytes = await image.read()
    valid, err_msg = AgriculturalRelevanceService.validate_image_file(image_bytes, max_size_mb=15)
    if not valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_msg)
    try:
        analysis_result = await run_in_threadpool(
            named_plant_report, image_bytes, plant_name, crop_type, growing_location
        )
    except OllamaNotReadyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except OllamaServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    if analysis_result.get("_wrong_module"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=analysis_result["_wrong_module"])
    if not analysis_result.get("isPlantImage"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=analysis_result.get("validationMessage", "Upload a clear plant or produce image."))

    # Persist to the signed-in user's account only; guest previews are not claimed as saved.
    analysis_result["savedToAccount"] = bool(user)
    analysis_result["persistenceMessage"] = "Saved to your account history." if user else "Preview only — sign in to save this result to your account."
    if user:
        _append_role_guidance(analysis_result, user, "named_plant")
    if user:
        try:
            history_record = ProductionAnalysis(
                id=str(uuid.uuid4()), user_id=user.id, analysis_type="named_plant",
                image_filename=image.filename, is_agricultural=True,
                predicted_class=analysis_result["userPlantName"],
                sub_category=analysis_result.get("possibleDisease") or analysis_result["healthAssessment"],
                confidence=analysis_result.get("diseaseConfidence") or (analysis_result["healthScorePercentage"] / 100.0),
                severity_level=analysis_result.get("healthAssessment"),
                explanation=analysis_result.get("disclaimer") or analysis_result.get("diseaseDiagnosisNotice"),
                recommendations_json=json.dumps(analysis_result.get("recommendations", [])),
                prevention_tips_json=json.dumps(analysis_result.get("generalManagementTips", [])),
                input_json=json.dumps({"plantName": plant_name, "cropType": crop_type, "growingLocation": growing_location, "imageFilename": image.filename}, ensure_ascii=False)
            )
            db.add(history_record)
            db.commit()
        except Exception as db_err:
            db.rollback()
            raise HTTPException(status_code=500, detail="Analysis completed but could not be saved to your account.") from db_err

    return analysis_result


@router.post("/crop-analysis", response_model=CropAnalysisOut)
async def analyze_crop(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    # 1. Read bytes and enforce format/size limits
    image_bytes = await image.read()
    valid, err_msg = AgriculturalRelevanceService.validate_image_file(image_bytes, max_size_mb=15)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg
        )

    # Use direct visual input with the locally hosted Ollama vision model. Avoid
    # pixel heuristics that can reject fruit, vegetables, flowers, or new crop types.
    try:
        analysis_result = await run_in_threadpool(crop_report, image_bytes)
    except OllamaNotReadyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except OllamaServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    if analysis_result.get("_wrong_module"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=analysis_result["_wrong_module"])

    # 4. Persist to the signed-in user's account only.
    analysis_result["savedToAccount"] = bool(user)
    analysis_result["persistenceMessage"] = "Saved to your account history." if user else "Preview only — sign in to save this result to your account."
    if user:
        _append_role_guidance(analysis_result, user, "crop")
    if user:
        try:
            history_record = ProductionAnalysis(
                id=str(uuid.uuid4()), user_id=user.id, analysis_type="crop",
                image_filename=image.filename, is_agricultural=True,
                predicted_class=analysis_result["predictedCrop"],
                sub_category=analysis_result["predictedCondition"],
                confidence=analysis_result["confidence"],
                severity_level=analysis_result.get("severityLevel"),
                explanation=analysis_result.get("explanation"),
                recommendations_json=json.dumps(analysis_result.get("recommendations", [])),
                prevention_tips_json=json.dumps(analysis_result.get("preventionTips", [])),
                input_json=json.dumps({"imageFilename": image.filename, "module": "crop_disease", "accountRole": user.get_role_value()}, ensure_ascii=False)
            )
            db.add(history_record)
            db.commit()
        except Exception as db_err:
            db.rollback()
            raise HTTPException(status_code=500, detail="Analysis completed but could not be saved to your account.") from db_err

    return analysis_result

@router.post("/soil-analysis", response_model=SoilAnalysisOut)
async def analyze_soil(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    # 1. Read bytes & check size/integrity
    image_bytes = await image.read()
    valid, err_msg = AgriculturalRelevanceService.validate_image_file(image_bytes, max_size_mb=15)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg
        )

    # A photo can support only an appearance-based soil observation; it cannot
    # measure pH, nutrients, salinity, or texture values reliably.
    try:
        analysis_result = await run_in_threadpool(soil_report, image_bytes)
    except OllamaNotReadyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except OllamaServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    if analysis_result.get("_wrong_module"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=analysis_result["_wrong_module"])

    # 4. Add role-specific next steps, then save to this account.
    if user:
        _append_role_guidance(analysis_result, user, "soil")
    analysis_result["savedToAccount"] = bool(user)
    analysis_result["persistenceMessage"] = "Saved to your account history." if user else "Preview only — sign in to save this result to your account."
    if user:
        try:
            history_record = ProductionAnalysis(
                id=str(uuid.uuid4()), user_id=user.id, analysis_type="soil",
                image_filename=image.filename, is_agricultural=True,
                predicted_class=analysis_result["predictedSoilCategory"],
                sub_category=None, confidence=analysis_result["confidence"],
                severity_level="Visual Assessment",
                explanation=analysis_result.get("limitationsDisclaimer"),
                recommendations_json=json.dumps(analysis_result.get("soilImprovementGuidance", [])),
                prevention_tips_json=json.dumps(analysis_result.get("suitableCrops", [])),
                input_json=json.dumps({"imageFilename": image.filename, "module": "soil_category", "accountRole": user.get_role_value()}, ensure_ascii=False)
            )
            db.add(history_record)
            db.commit()
        except Exception as db_err:
            db.rollback()
            raise HTTPException(status_code=500, detail="Analysis completed but could not be saved to your account.") from db_err

    return analysis_result

@router.get("/history")
def get_production_history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    records = (db.query(ProductionAnalysis)
        .filter(ProductionAnalysis.user_id == user.id)
        .order_by(ProductionAnalysis.created_at.desc()).limit(50).all())
    return [r.to_history_dict() for r in records]
