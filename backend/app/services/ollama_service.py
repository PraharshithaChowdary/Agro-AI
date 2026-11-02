"""Ollama integration for AGRO AI.

- Uses the local model server's native /api/chat endpoint for text and image inputs.
- Keeps vision and chat calls serial to avoid competing for limited Codespaces RAM.
- Keeps models warm between requests by default to avoid repeated load delays.
- Treats visual diagnoses as screening hypotheses, never as verified pathology.
"""
from __future__ import annotations

import base64
import io
import json
import logging
import os
import re
import threading
from typing import Any, Dict, List, Optional

import httpx
from PIL import Image, ImageOps

logger = logging.getLogger("agro_ai.ollama")
_INFERENCE_LOCK = threading.Lock()


class OllamaServiceError(RuntimeError):
    """Raised when Ollama cannot complete a requested operation."""


class OllamaNotReadyError(OllamaServiceError):
    """Raised when Ollama or a configured model is not available."""


class OllamaService:
    @staticmethod
    def base_url() -> str:
        raw = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").strip().rstrip("/")
        return raw[:-3] if raw.endswith("/v1") else raw

    @staticmethod
    def vision_model() -> str:
        return os.getenv("OLLAMA_VISION_MODEL", "qwen2.5vl:3b").strip()

    @staticmethod
    def chat_model() -> str:
        return os.getenv("OLLAMA_CHAT_MODEL", os.getenv("LLM_MODEL", "qwen2.5:1.5b")).strip()

    @staticmethod
    def timeout_seconds() -> float:
        try:
            return max(30.0, float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "360")))
        except ValueError:
            return 360.0

    @staticmethod
    def keep_alive() -> str | int:
        # Loading a quantized model often costs more time than generating a short
        # answer. Keep it resident for a while unless deployment config overrides it.
        return os.getenv("OLLAMA_KEEP_ALIVE", "10m").strip() or "10m"

    @classmethod
    def preload_vision_model(cls) -> None:
        """Warm the vision runner in the background so the first image avoids model load time."""
        if os.getenv("OLLAMA_PRELOAD_VISION", "true").strip().lower() not in {"1", "true", "yes", "on"}:
            return
        model = cls.vision_model()
        if not cls._server_reachable() or not cls._model_installed(model, cls._installed_models()):
            logger.info("Vision warmup skipped; the local vision model is not ready.")
            return

        # Include a tiny image so the vision path is initialized, not just the text decoder.
        buffer = io.BytesIO()
        Image.new("RGB", (32, 32), (112, 128, 96)).save(buffer, format="JPEG", quality=60)
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Reply OK.", "images": [encoded]}],
            "stream": False,
            "keep_alive": cls.keep_alive(),
            "options": {"num_predict": 1, "num_ctx": 2048, "temperature": 0},
        }
        try:
            with _INFERENCE_LOCK:
                response = httpx.post(
                    f"{cls.base_url()}/api/chat",
                    json=payload,
                    timeout=cls.timeout_seconds(),
                )
            response.raise_for_status()
            logger.info("Vision model warmup completed.")
        except Exception as exc:
            logger.info("Vision model warmup did not complete: %s", exc)

    @classmethod
    def preload_chat_model(cls) -> None:
        """Warm the small text model used to turn image findings into a readable report."""
        if os.getenv("OLLAMA_PRELOAD_CHAT", "true").strip().lower() not in {"1", "true", "yes", "on"}:
            return
        model = cls.chat_model()
        if not cls._server_reachable() or not cls._model_installed(model, cls._installed_models()):
            logger.info("Chat warmup skipped; the local chat model is not ready.")
            return
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Reply OK."}],
            "stream": False,
            "keep_alive": cls.keep_alive(),
            "options": {"num_predict": 1, "num_ctx": 2048, "temperature": 0},
        }
        try:
            with _INFERENCE_LOCK:
                response = httpx.post(f"{cls.base_url()}/api/chat", json=payload, timeout=cls.timeout_seconds())
            response.raise_for_status()
            logger.info("Chat model warmup completed.")
        except Exception as exc:
            logger.info("Chat model warmup did not complete: %s", exc)

    @classmethod
    def _installed_models(cls) -> List[str]:
        try:
            response = httpx.get(f"{cls.base_url()}/api/tags", timeout=5.0)
            response.raise_for_status()
            models = response.json().get("models", [])
            return [str(m.get("name", "")) for m in models if m.get("name")]
        except Exception as exc:
            logger.debug("Ollama tags unavailable: %s", exc)
            return []

    @staticmethod
    def _model_installed(configured: str, installed: List[str]) -> bool:
        wanted = configured.strip()
        if not wanted:
            return False
        if wanted in installed:
            return True
        # If no tag was configured, Ollama's implicit :latest tag is acceptable.
        # If a tag such as :3b was explicitly requested, do not mistake :7b or
        # :1.5b for it; otherwise readiness can pass and the actual request 404s.
        if ":" not in wanted:
            return any(name.split(":", 1)[0] == wanted for name in installed)
        return False

    @classmethod
    def status(cls) -> Dict[str, Any]:
        connected = cls._server_reachable()
        installed = cls._installed_models() if connected else []
        vision_installed = cls._model_installed(cls.vision_model(), installed)
        chat_installed = cls._model_installed(cls.chat_model(), installed)
        return {
            "provider": "ollama",
            "connected": connected,
            "visionReady": connected and vision_installed,
            "chatReady": connected and chat_installed,
            "ready": connected and vision_installed and chat_installed,
            "installedModels": installed,
            "visionModelConfigured": cls.vision_model(),
            "chatModelConfigured": cls.chat_model(),
            "message": cls._status_message(connected, vision_installed, chat_installed),
        }

    @classmethod
    def _server_reachable(cls) -> bool:
        try:
            response = httpx.get(f"{cls.base_url()}/api/version", timeout=1.5)
            return response.status_code == 200
        except Exception:
            return False

    @staticmethod
    def _status_message(connected: bool, vision_installed: bool, chat_installed: bool) -> str:
        if not connected:
            return "Local AI service is not reachable. Start the model service, then retry."
        if not vision_installed and not chat_installed:
            return "The local AI service is running, but its vision and chat models are missing. Follow the model setup steps in the project guide."
        if not vision_installed:
            return "The local AI service is running, but its vision model is missing. Follow the model setup steps in the project guide."
        if not chat_installed:
            return "The local AI service is running, but its chat model is missing. Follow the model setup steps in the project guide."
        return "Local AI is ready for image screening and agricultural chat."

    @classmethod
    def _assert_model_ready(cls, model: str) -> None:
        # Check the lightweight version endpoint first; a stopped local server should
        # fail quickly instead of waiting for the model-list request timeout.
        if not cls._server_reachable():
            raise OllamaNotReadyError(
                "The local AI service is not reachable. Start the model service, then retry."
            )
        installed = cls._installed_models()
        if not cls._model_installed(model, installed):
            raise OllamaNotReadyError(
                "A required local AI model is not installed. On Windows, run download_models.bat; on Linux, run scripts/pull_models.sh."
            )

    @classmethod
    def chat_text(
        cls,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 128,
    ) -> Optional[str]:
        model = cls.chat_model()
        cls._assert_model_ready(model)
        ollama_messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
        for message in messages[-10:]:
            sender = str(message.get("sender", message.get("role", "user"))).lower()
            role = "assistant" if sender in {"assistant", "model", "bot"} else "user"
            content = str(message.get("content", "")).strip()
            if content:
                ollama_messages.append({"role": role, "content": content[:6000]})
        payload = {
            "model": model,
            "messages": ollama_messages,
            "stream": False,
            "keep_alive": cls.keep_alive(),
            "options": {
                "temperature": float(temperature),
                "num_predict": int(max(64, min(max_tokens, 256))),
                "num_ctx": max(2048, min(int(os.getenv("OLLAMA_NUM_CTX", "2048")), 8192)),
            },
        }
        try:
            with _INFERENCE_LOCK:
                response = httpx.post(
                    f"{cls.base_url()}/api/chat",
                    json=payload,
                    timeout=cls.timeout_seconds(),
                )
            response.raise_for_status()
            data = response.json()
            content = data.get("message", {}).get("content", "")
            return content.strip() or None
        except Exception as exc:
            logger.warning("Ollama text request failed: %s", exc)
            return None

    @classmethod
    def analyze_image(
        cls,
        image_bytes: bytes,
        task: str = "general",
        plant_name: Optional[str] = None,
        crop_type: Optional[str] = None,
        growing_location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Return a normalized structured visual screening report from a real image input."""
        model = cls.vision_model()
        cls._assert_model_ready(model)
        encoded = cls._prepare_image(image_bytes)
        prompt = cls._build_vision_prompt(task, plant_name, crop_type, growing_location)
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt, "images": [encoded]}],
            "stream": False,
            "format": "json",
            "keep_alive": cls.keep_alive(),
            "options": {
                "temperature": 0.1,
                # Keep responses long enough for the JSON report but bounded for local RAM.
                "num_predict": max(96, min(int(os.getenv("OLLAMA_VISION_NUM_PREDICT", "160")), 192)),
                "num_ctx": max(2048, min(int(os.getenv("OLLAMA_NUM_CTX", "2048")), 8192)),
            },
        }
        try:
            # Serialize vision requests. Large image models can consume most of a small Codespace.
            with _INFERENCE_LOCK:
                response = httpx.post(
                    f"{cls.base_url()}/api/chat",
                    json=payload,
                    timeout=cls.timeout_seconds(),
                )
            response.raise_for_status()
            data = response.json()
            raw = str(data.get("message", {}).get("content", "")).strip()
            if not raw:
                raise OllamaServiceError("The vision model returned an empty report. Try a clearer, well-lit image.")
            parsed = cls._parse_json(raw)
            return cls._normalize_report(parsed, raw)
        except OllamaServiceError:
            raise
        except httpx.HTTPStatusError as exc:
            body = exc.response.text[:400]
            logger.warning("Ollama vision HTTP error %s: %s", exc.response.status_code, body)
            if exc.response.status_code == 404:
                raise OllamaNotReadyError(
                    "The configured local vision model is missing. Run download_models.bat on Windows, or scripts/pull_models.sh on Linux."
                ) from exc
            body_lower = body.lower()
            if any(marker in body_lower for marker in ("unexpected eof", "runner process has terminated", "signal: killed", "out of memory", "failed to load model")):
                raise OllamaServiceError(
                    "The vision model runner stopped unexpectedly. Close memory-heavy apps, retry with a clear image, and inspect the local model-service log."
                ) from exc
            raise OllamaServiceError(
                "The local vision model could not analyze this image. Check that the model service is running and the configured vision model is installed."
            ) from exc
        except Exception as exc:
            logger.exception("Ollama image analysis failed")
            if isinstance(exc, OllamaNotReadyError):
                raise
            raise OllamaServiceError(
                "Image analysis did not complete. Check available memory and the local AI service status, then retry."
            ) from exc

    @classmethod
    def _prepare_image(cls, image_bytes: bytes) -> str:
        try:
            with Image.open(io.BytesIO(image_bytes)) as original:
                image = ImageOps.exif_transpose(original).convert("RGB")
                # Keep vision tensors manageable on ordinary laptops; original uploads
                # remain untouched in the UI/history while this compact copy goes to Ollama.
                max_side = max(256, min(int(os.getenv("OLLAMA_IMAGE_MAX_SIDE", "256")), 1536))
                quality = max(55, min(int(os.getenv("OLLAMA_IMAGE_JPEG_QUALITY", "60")), 85))
                image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
                buffer = io.BytesIO()
                image.save(buffer, format="JPEG", quality=quality, subsampling=2, optimize=False)
                return base64.b64encode(buffer.getvalue()).decode("ascii")
        except Exception as exc:
            raise OllamaServiceError("The uploaded image could not be decoded. Upload a valid JPG, PNG, or WebP image.") from exc

    @classmethod
    def _build_vision_prompt(
        cls, task: str, plant_name: Optional[str], crop_type: Optional[str], growing_location: Optional[str]
    ) -> str:
        context = []
        if plant_name and plant_name.strip():
            context.append(f"User-supplied name (treat as a hint, verify from visible evidence): {plant_name.strip()[:120]}")
        if crop_type and crop_type.strip():
            context.append(f"User-supplied category: {crop_type.strip()[:80]}")
        if growing_location and growing_location.strip():
            context.append(f"Growing environment: {growing_location.strip()[:100]}")
        context_text = "\n".join(context) if context else "No user-supplied crop name. Identify only as specifically as the pixels support."

        task_text = {
            "plant": "Focus on identifying the visible botanical or produce subject and its condition, including leaves, flowers, stems, fruits, and vegetables.",
            "crop": "Focus on crop/plant/fruit/vegetable identity, visible symptoms, maturity, freshness, and possible external spoilage.",
            "soil": "Focus only on the visible soil surface: apparent color, visible particle/aggregate texture, stones, organic matter, crusting, and moisture appearance.",
            "identify": "Focus on the broad subject and likely common name, then say how certain the visual identification is.",
            "health": "Focus on observable plant/produce symptoms and cautious next steps.",
            "general": "Describe and classify the subject visible in the uploaded image.",
        }.get(task, "Describe and classify the subject visible in the uploaded image.")
        soil_note = (
            "For soil images, describe only visible color, texture, aggregates, stones, surface cover, or apparent moisture. "
            "Do not describe plant health, disease, stress, or spoilage. Do not infer pH or nutrient levels."
            if task == "soil" else ""
        )

        return f"""You are AGRO AI's image screening component.
{task_text}
{soil_note}
Context:
{context_text}

Return JSON only with keys image_type, subject_name, visible_condition, visible_observations, possible_issues, summary. Keep subject_name to 3 words, observations to one short visible fact, possible_issues to at most one item, and summary to one short sentence. Use an empty list if no issue is visible.
Use image_type leaf|flower|fruit|vegetable|whole_plant|crop|soil|grain|seed|non_agricultural|uncertain and visible_condition healthy-looking|possible_stress|unripe|ripe|overripe|possible_spoilage|uncertain. Each issue has name, evidence, likelihood low|moderate|high.
Use only visible evidence. No diagnosis, inferred cause, confidence score, or chemical dose. Reject unrelated images. Never infer soil lab measurements. Distinguish produce ripeness from spoilage and mark uncertainty when needed.
"""

    @staticmethod
    def _parse_json(raw: str) -> Dict[str, Any]:
        text = raw.strip()
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
        try:
            item = json.loads(text)
            if isinstance(item, dict):
                return item
        except Exception:
            pass
        # Some lightweight vision models wrap JSON with an explanatory sentence.
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            try:
                item = json.loads(text[start:end + 1])
                if isinstance(item, dict):
                    return item
            except Exception:
                pass
        # Preserve what the model said, but mark every unsupported field as uncertain.
        return {
            "is_agricultural": True,
            "image_type": "uncertain",
            "subject_name": "Uncertain subject",
            "visible_condition": "uncertain",
            "ripeness_status": "uncertain",
            "spoilage_status": "uncertain",
            "visible_observations": [],
            "possible_issues": [],
            "summary": text[:1500] or "The model did not produce a parseable visual report.",
            "recommendations": [],
            "precautions": [],
            "uncertainty_notes": ["The response could not be parsed into the structured report format; repeat with a clearer image."],
        }

    @staticmethod
    def _normalize_report(data: Dict[str, Any], raw: str) -> Dict[str, Any]:
        valid_types = {"leaf", "flower", "fruit", "vegetable", "whole_plant", "crop", "soil", "grain", "seed", "non_agricultural", "uncertain"}
        valid_conditions = {"healthy-looking", "possible_stress", "unripe", "ripe", "overripe", "possible_spoilage", "uncertain"}
        valid_ripeness = {"not_applicable", "unripe", "ripe", "overripe", "uncertain"}
        valid_spoilage = {"not_applicable", "no_visible_spoilage", "possible_visible_spoilage", "uncertain"}

        def clean(value: Any, limit: int = 300) -> str:
            return re.sub(r"\s+", " ", str(value or "")).strip()[:limit]

        def string_list(value: Any, limit: int = 8) -> List[str]:
            if isinstance(value, str):
                value = [value]
            if not isinstance(value, list):
                return []
            result = []
            for item in value[:limit]:
                if isinstance(item, dict):
                    text = clean(item.get("text") or item.get("description") or item.get("name"), 400)
                else:
                    text = clean(item, 400)
                if text and text not in result:
                    result.append(text)
            return result

        def enum(value: Any, allowed: set[str], fallback: str) -> str:
            val = clean(value, 60).lower().replace(" ", "_").replace("-", "_")
            aliases = {
                "healthy": "healthy-looking", "healthy_looking": "healthy-looking", "appears_healthy": "healthy-looking",
                "stress": "possible_stress", "symptoms": "possible_stress", "damage": "possible_stress",
                "spoiled": "possible_spoilage", "rotten": "possible_spoilage", "rot": "possible_spoilage",
                "nonagricultural": "non_agricultural", "non_agriculture": "non_agricultural",
                "fruit_vegetable": "fruit", "plant": "whole_plant", "leaf_or_plant": "leaf",
            }
            val = aliases.get(val, val)
            return val if val in allowed else fallback

        issues = []
        raw_issues = data.get("possible_issues", data.get("possibleIssues", []))
        if isinstance(raw_issues, list):
            for issue in raw_issues[:6]:
                if isinstance(issue, dict):
                    name = clean(issue.get("name") or issue.get("issue"), 160)
                    evidence = clean(issue.get("evidence") or issue.get("visible_evidence") or issue.get("description"), 300)
                    likelihood = clean(issue.get("likelihood", "uncertain"), 30).lower()
                    if likelihood not in {"low", "moderate", "high"}:
                        likelihood = "low"
                    if name and evidence:
                        issues.append({"name": name, "evidence": evidence, "likelihood": likelihood})

        image_type = enum(data.get("image_type", data.get("imageType")), valid_types, "uncertain")
        condition = enum(data.get("visible_condition", data.get("visibleCondition")), valid_conditions, "uncertain")
        ripeness = enum(data.get("ripeness_status", data.get("ripenessStatus")), valid_ripeness, "uncertain")
        spoilage = enum(data.get("spoilage_status", data.get("spoilageStatus")), valid_spoilage, "uncertain")
        agri_default = image_type != "non_agricultural"
        is_agri = data.get("is_agricultural", data.get("isAgricultural", agri_default))
        if not isinstance(is_agri, bool):
            is_agri = agri_default
        if image_type == "non_agricultural":
            is_agri = False

        observations = string_list(data.get("visible_observations", data.get("visual_observations", data.get("visibleObservations", []))))
        recommendations = string_list(data.get("recommendations", []))
        precautions = string_list(data.get("precautions", data.get("prevention_tips", [])))
        uncertainty = string_list(data.get("uncertainty_notes", data.get("limitations", [])))
        subject = clean(data.get("subject_name") or data.get("subject") or data.get("common_name") or "Unknown", 120)
        sci = clean(data.get("scientific_name") or data.get("scientificName"), 120) or None
        summary = clean(data.get("summary") or data.get("image_summary") or data.get("description"), 1500)
        if not summary:
            if image_type == "uncertain" or condition == "uncertain":
                summary = "The subject or its condition could not be confidently classified from this photograph. Try a sharper image with the subject filling the frame."
            else:
                category_label = image_type.replace("_", " ")
                condition_label = condition.replace("_", " ")
                observation_note = " Visible observations: " + "; ".join(observations[:3]) + "." if observations else ""
                summary = f"The photograph appears to show {subject} ({category_label}). The visible condition is assessed as {condition_label}.{observation_note} This is preliminary visual screening, not a confirmed diagnosis."
        # A defensive final check prevents unsupported chemical instructions from reaching the UI.
        unsafe_terms = re.compile(
            r"\b(pesticide|fungicide|insecticide|herbicide|acaricide|spray|tank mix|carbendazim|mancozeb|chlorpyrifos|glyphosate|propiconazole|imidacloprid|metalaxyl|chlorantraniliprole|emamectin|tricyclazole|streptocycline|dose|dosage|concentration|dilution)\b"
            r"|\b\d+(?:\.\d+)?\s*(?:mg|g|kg|ml|mL|l|litre|liter|%|percent)\b",
            re.I,
        )
        safe_recs = []
        for rec in recommendations:
            if unsafe_terms.search(rec):
                safe_recs.append("Do not choose a chemical treatment from an image-only result; confirm the cause with a qualified local agricultural adviser and follow registered product labels.")
            else:
                safe_recs.append(rec)
        safe_precautions = []
        for rec in precautions:
            if unsafe_terms.search(rec):
                safe_precautions.append("Confirm any treatment with a local KVK/agricultural extension officer before application.")
            else:
                safe_precautions.append(rec)

        return {
            "is_agricultural": is_agri,
            "image_type": image_type,
            "subject_name": subject,
            "scientific_name": sci,
            "visible_condition": condition,
            "ripeness_status": ripeness,
            "spoilage_status": spoilage,
            "visible_observations": observations,
            "possible_issues": issues,
            "summary": summary,
            "recommendations": safe_recs[:6],
            "precautions": safe_precautions[:8],
            "uncertainty_notes": uncertainty[:6],
        }

    @classmethod
    def generate_text(cls, system_prompt: str, messages: List[Dict[str, str]], temperature: float = 0.2, max_tokens: int = 128) -> Optional[str]:
        """Shared local-language-model entrypoint used by the assistant."""
        return cls.chat_text(system_prompt, messages, temperature, max_tokens)
