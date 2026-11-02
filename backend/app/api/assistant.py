import os
import uuid
import json
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models.chat import ChatMessage
from app.models.user import User
from app.api.auth import get_current_user_optional, get_current_user
from app.services.assistant_service import AssistantService
from app.services.farm_calculator import FarmCalculatorService
from app.services.llm_client import LLMClient
from app.schemas.assistant import (
    ChatRequestSchema,
    ChatResponseSchema,
    CalculatorRequestSchema,
    SessionSummarySchema,
    StoredChatMessageSchema,
    ModelConfigRequestSchema
)

router = APIRouter(prefix="/api/assistant", tags=["AGRO AI Assistant"])

@router.get("/status")
def get_assistant_engine_status():
    """Returns the active AI provider, model, and operational mode."""
    return LLMClient.get_status()

@router.post("/config")
def update_assistant_config(payload: ModelConfigRequestSchema, user: User = Depends(get_current_user)):
    """Only administrators may alter process-wide LLM configuration."""
    if user.get_role_value() != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can change global assistant configuration.")
    provider = payload.provider.lower().strip()
    if provider in ["none", "offline"]:
        LLMClient.set_dynamic_config("none", "offline_knowledge_engine", "")
    elif provider == "ollama":
        # Local Ollama is keyless. Never require or ask users to paste a secret for it.
        chosen_model = payload.model or os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:1.5b")
        LLMClient.set_dynamic_config("ollama", chosen_model, "")
    else:
        if not payload.apiKey:
            raise HTTPException(status_code=400, detail="API key is required for an external AI provider")
        default_models = {
            "groq": "llama-3.1-8b-instant",
            "gemini": "gemini-1.5-flash",
            "openai": "gpt-4o-mini",
            "anthropic": "claude-3-haiku-20240307"
        }
        chosen_model = payload.model or default_models.get(provider, "llama-3.1-8b-instant")
        LLMClient.set_dynamic_config(provider, chosen_model, payload.apiKey)
    return LLMClient.get_status()

@router.delete("/config")
def reset_assistant_config(user: User = Depends(get_current_user)):
    """Only administrators may reset process-wide LLM configuration."""
    if user.get_role_value() != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can reset global assistant configuration.")
    LLMClient.clear_dynamic_config()
    return LLMClient.get_status()

@router.post("/chat", response_model=ChatResponseSchema)
def chat_with_assistant(
    payload: ChatRequestSchema,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    session_id = payload.sessionId or str(uuid.uuid4())

    history_dicts = [h.model_dump() for h in payload.history] if payload.history else []

    # If user is logged in and no history passed in body, load last 6 messages for this session
    if user and not history_dicts and payload.sessionId:
        recent_db_msgs = db.query(ChatMessage).filter(
            ChatMessage.user_id == user.id,
            ChatMessage.session_id == payload.sessionId
        ).order_by(ChatMessage.created_at.desc()).limit(6).all()
        history_dicts = [
            {"sender": m.sender, "content": m.content}
            for m in reversed(recent_db_msgs)
        ]

    result = AssistantService.process_query(
        message=payload.message,
        history=history_dicts,
        user_id=user.id if user else None
    )

    # Apply a role lens from the server-side account, never from client-supplied text.
    # Keep this concise and avoid inventing local prices, weather, dosage, or yields.
    if user:
        role = user.get_role_value()
        role_guidance = {
            "farmer": "**For your farm:** confirm crop, growth stage, district, and recent weather before acting. Treat visual results as screening, verify uncertain disease diagnoses with a KVK/agricultural officer, and follow locally registered product labels for any crop-protection chemical.",
            "buyer": "**For procurement:** verify crop/variety, grade, moisture/quality parameters, lot traceability, storage conditions, and current local market data before making a purchase decision. This assistant does not have live mandi prices unless a live-data source is explicitly shown.",
            "general": "**Practical next step:** share the crop/plant, location, and goal to get a more specific answer. Distinguish general guidance from a confirmed field diagnosis.",
        }.get(role)
        if role_guidance and result.get("response"):
            result["response"] += "\n\n### Guidance for your account role\n" + role_guidance

    result["sessionId"] = session_id
    result["savedToAccount"] = bool(user)
    result["persistenceMessage"] = "Conversation saved to your account." if user else "Conversation preview only — sign in to keep account history."

    # Record message logs in DB
    if user:
        try:
            user_msg = ChatMessage(
                id=str(uuid.uuid4()),
                user_id=user.id,
                session_id=session_id,
                sender="user",
                content=payload.message,
                category=result.get("category")
            )
            bot_msg = ChatMessage(
                id=str(uuid.uuid4()),
                user_id=user.id,
                session_id=session_id,
                sender="assistant",
                content=result.get("response", ""),
                category=result.get("category"),
                evidence_sources_json=json.dumps(result.get("evidenceSources", [])),
                suggested_questions_json=json.dumps(result.get("suggestedQuestions", [])),
                calculator_data_json=json.dumps(result.get("calculatorData")) if result.get("calculatorData") else None,
                model_provider=result.get("modelProvider", "offline_knowledge_engine")
            )
            db.add_all([user_msg, bot_msg])
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="The answer was generated but could not be saved to your account history. Please retry."
            ) from e

    return result

@router.get("/sessions", response_model=List[SessionSummarySchema])
def list_user_sessions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Lists conversation sessions for the authenticated user."""
    # Find distinct session_ids
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == user.id,
        ChatMessage.session_id.isnot(None)
    ).order_by(desc(ChatMessage.created_at)).all()

    sessions_map = {}
    for m in messages:
        sid = m.session_id
        if sid not in sessions_map:
            sessions_map[sid] = {
                "sessionId": sid,
                "lastMessage": m.content[:80] + ("..." if len(m.content) > 80 else ""),
                "messageCount": 1,
                "updatedAt": m.created_at.isoformat()
            }
        else:
            sessions_map[sid]["messageCount"] += 1

    return list(sessions_map.values())

@router.get("/sessions/{session_id}", response_model=List[StoredChatMessageSchema])
def get_session_history(
    session_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Retrieves all message history for a specific session belonging to the user."""
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == user.id,
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at.asc()).all()

    result = []
    for m in messages:
        sources = []
        if m.evidence_sources_json:
            try:
                sources = json.loads(m.evidence_sources_json)
            except Exception:
                sources = []
        calc_data = None
        if m.calculator_data_json:
            try:
                calc_data = json.loads(m.calculator_data_json)
            except Exception:
                calc_data = None

        result.append(StoredChatMessageSchema(
            id=m.id,
            sender=m.sender,
            content=m.content,
            category=m.category,
            createdAt=m.created_at.strftime("%I:%M %p"),
            evidenceSources=sources,
            calculatorData=calc_data
        ))

    return result

@router.delete("/sessions/{session_id}")
def clear_session_history(
    session_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Clears all messages for a specific session belonging to the user."""
    deleted_count = db.query(ChatMessage).filter(
        ChatMessage.user_id == user.id,
        ChatMessage.session_id == session_id
    ).delete()
    db.commit()
    return {"message": f"Cleared {deleted_count} messages in session {session_id}.", "deletedCount": deleted_count}

@router.post("/calculate")
def execute_farm_calculation(payload: CalculatorRequestSchema):
    """Dedicated endpoint for executing validated farm calculations."""
    ctype = payload.calcType.lower()
    p = payload.params

    try:
        if ctype == "npk_fertilizer":
            return FarmCalculatorService.calculate_npk_fertilizer(
                target_n=float(p.get("targetN", 120)),
                target_p=float(p.get("targetP", 60)),
                target_k=float(p.get("targetK", 40)),
                area=float(p.get("area", 1.0)),
                unit=str(p.get("unit", "ha")),
                use_ssp=bool(p.get("useSSP", False))
            )
        elif ctype == "seed_rate":
            return FarmCalculatorService.calculate_plant_population_and_seed_rate(
                area_val=float(p.get("area", 1.0)),
                area_unit=str(p.get("areaUnit", "ha")),
                row_spacing_cm=float(p.get("rowSpacingCm", 60)),
                plant_spacing_cm=float(p.get("plantSpacingCm", 20)),
                test_weight_g=float(p.get("testWeightG", 40)),
                germination_pct=float(p.get("germinationPct", 85)),
                purity_pct=float(p.get("purityPct", 98))
            )
        elif ctype == "irrigation":
            return FarmCalculatorService.calculate_irrigation_water_and_runtime(
                eto_mm_day=float(p.get("etoMmDay", 4.5)),
                crop_kc=float(p.get("cropKc", 1.15)),
                area_m2=float(p.get("areaM2", 4047)),
                emitter_discharge_lph=float(p.get("emitterDischargeLph", 2.0)),
                emitters_per_plant=int(p.get("emittersPerPlant", 1))
            )
        elif ctype == "economics":
            return FarmCalculatorService.calculate_farm_economics(
                crop_name=str(p.get("cropName", "Paddy / Wheat")),
                area_val=float(p.get("area", 1.0)),
                area_unit=str(p.get("areaUnit", "hectare")),
                cost_items=dict(p.get("costItems", {
                    "Land Preparation": 6000.0,
                    "Seed & Sowing": 3500.0,
                    "Fertilizers": 8500.0,
                    "Plant Protection": 3000.0,
                    "Irrigation": 4000.0,
                    "Harvesting": 8000.0
                })),
                expected_yield_quintals=float(p.get("expectedYieldQuintals", 45)),
                price_per_quintal_inr=float(p.get("pricePerQuintalINR", 2275))
            )
        elif ctype == "math_eval":
            expr = str(p.get("expression", "0"))
            val = FarmCalculatorService.safe_math_eval(expr)
            return {"expression": expr, "result": val}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown calculation type '{ctype}'. Supported: npk_fertilizer, seed_rate, irrigation, economics, math_eval."
            )
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Calculation error: {str(e)}")
