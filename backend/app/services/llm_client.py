"""
AGRO AI — Configurable Multi-Provider LLM Client
Supports:
- Google Gemini (REST API)
- OpenAI (REST API)
- Groq (Ultra-fast Llama-3.1 inference)
- Anthropic Claude
- Local Ollama / vLLM (OpenAI-compatible)
- Autonomous Offline Fallback (when no API key or provider is configured)

All API keys are read strictly from environment variables.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple

import httpx

logger = logging.getLogger("agro_ai.llm")

class LLMClient:
    """
    Unified client for communicating with configured LLM providers.
    Fails gracefully to offline mode on any timeout, network error, or missing configuration.
    """

    _dynamic_config: Optional[Dict[str, str]] = None

    @classmethod
    def set_dynamic_config(cls, provider: str, model: str, api_key: str):
        cls._dynamic_config = {
            "provider": provider.lower().strip(),
            "model": model.strip(),
            "api_key": api_key.strip()
        }

    @classmethod
    def clear_dynamic_config(cls):
        cls._dynamic_config = None

    @classmethod
    def get_configured_provider(cls) -> Tuple[str, str, Optional[str]]:
        """Return the configured provider, model and provider credential/base URL.

        Ollama is the default for this student project. The existing grounded offline
        knowledge engine is still used automatically if Ollama is unavailable.
        """
        if cls._dynamic_config:
            dyn_p = cls._dynamic_config.get("provider", "ollama")
            dyn_m = cls._dynamic_config.get("model", "qwen2.5:1.5b")
            dyn_k = cls._dynamic_config.get("api_key", "")
            if dyn_p == "ollama" and not dyn_k:
                dyn_k = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
            return dyn_p, dyn_m, dyn_k

        forced_provider = os.getenv("LLM_PROVIDER", "ollama").lower().strip()
        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        groq_key = os.getenv("GROQ_API_KEY", "").strip()
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1").strip()

        if forced_provider in {"none", "offline"}:
            return "none", "offline_knowledge_engine", None
        if forced_provider == "gemini" and gemini_key:
            return "gemini", os.getenv("LLM_MODEL", "gemini-1.5-flash"), gemini_key
        if forced_provider == "openai" and openai_key:
            return "openai", os.getenv("LLM_MODEL", "gpt-4o-mini"), openai_key
        if forced_provider == "groq" and groq_key:
            return "groq", os.getenv("LLM_MODEL", "llama-3.1-8b-instant"), groq_key
        if forced_provider == "anthropic" and anthropic_key:
            return "anthropic", os.getenv("LLM_MODEL", "claude-3-haiku-20240307"), anthropic_key
        if forced_provider == "ollama":
            return "ollama", os.getenv("OLLAMA_CHAT_MODEL", os.getenv("LLM_MODEL", "qwen2.5:1.5b")), ollama_url

        # Auto-detect external keys only when the user explicitly selects auto mode.
        if gemini_key:
            return "gemini", os.getenv("LLM_MODEL", "gemini-1.5-flash"), gemini_key
        if groq_key:
            return "groq", os.getenv("LLM_MODEL", "llama-3.1-8b-instant"), groq_key
        if openai_key:
            return "openai", os.getenv("LLM_MODEL", "gpt-4o-mini"), openai_key
        if anthropic_key:
            return "anthropic", os.getenv("LLM_MODEL", "claude-3-haiku-20240307"), anthropic_key
        return "ollama", os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:1.5b"), ollama_url

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """Return a user-safe status without exposing internal model identifiers in the UI."""
        provider, model, _ = cls.get_configured_provider()
        if provider == "ollama":
            try:
                from app.services.ollama_service import OllamaService
                state = OllamaService.status()
                return {
                    "provider": "ollama",
                    "model": "Configured assistant",
                    "is_live_llm": bool(state.get("chatReady")),
                    "mode": "Assistant ready" if state.get("chatReady") else "Assistant setup required",
                    "badge": "Assistant ready" if state.get("chatReady") else "Setup needed",
                    "vision_ready": bool(state.get("visionReady")),
                    "chat_ready": bool(state.get("chatReady")),
                    "message": "Assistant services are ready." if state.get("ready") else "Complete the local model setup steps in the project README." ,
                }
            except Exception:
                return {
                    "provider": "configured", "model": "Configured assistant", "is_live_llm": False,
                    "mode": "Assistant setup required",
                    "badge": "Setup needed", "vision_ready": False, "chat_ready": False,
                    "message": "Complete the setup steps in the project README. General reference answers remain available when possible.",
                }
        if provider != "none":
            return {
                "provider": provider, "model": "Configured AI provider", "is_live_llm": True,
                "mode": "Configured AI provider", "badge": "AI Powered",
            }
        return {
            "provider": "offline", "model": "Offline knowledge engine", "is_live_llm": False,
            "mode": "Grounded offline knowledge engine", "badge": "Offline Knowledge",
        }

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 128
    ) -> Optional[str]:
        """
        Dispatches prompt to the active provider with a 15-second timeout.
        Returns generated string, or None if offline or failed.
        """
        provider, model, key = cls.get_configured_provider()
        if provider == "none" or (provider != "ollama" and not key):
            return None

        try:
            if provider == "ollama":
                from app.services.ollama_service import OllamaService
                return OllamaService.generate_text(system_prompt, messages, temperature, max_tokens)
            elif provider == "gemini":
                return cls._call_gemini(model, key, system_prompt, messages, temperature, max_tokens)
            elif provider in ["openai", "groq"]:
                base_url = "https://api.groq.com/openai/v1" if provider == "groq" else "https://api.openai.com/v1"
                return cls._call_openai_compatible(base_url, model, key, system_prompt, messages, temperature, max_tokens)
            elif provider == "anthropic":
                return cls._call_anthropic(model, key, system_prompt, messages, temperature, max_tokens)
        except Exception as e:
            logger.warning(f"LLM API call failed ({provider}): {e}. Falling back to Offline Knowledge Engine.")
            return None

        return None

    @classmethod
    def _call_gemini(
        cls,
        model: str,
        api_key: str,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> Optional[str]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        contents = []
        for m in messages:
            role = "user" if m.get("sender") in ["user", "human"] else "model"
            contents.append({
                "role": role,
                "parts": [{"text": m.get("content", "")}]
            })

        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }

        with httpx.Client(timeout=15.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
            else:
                logger.warning(f"Gemini error {resp.status_code}: {resp.text}")
        return None

    @classmethod
    def _call_openai_compatible(
        cls,
        base_url: str,
        model: str,
        api_key: str,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> Optional[str]:
        url = f"{base_url.rstrip('/')}/chat/completions"

        formatted_msgs = [{"role": "system", "content": system_prompt}]
        for m in messages:
            role = "user" if m.get("sender") in ["user", "human"] else "assistant"
            formatted_msgs.append({"role": role, "content": m.get("content", "")})

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": formatted_msgs,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        with httpx.Client(timeout=15.0) as client:
            resp = client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
            else:
                logger.warning(f"OpenAI-compatible error {resp.status_code}: {resp.text}")
        return None

    @classmethod
    def _call_anthropic(
        cls,
        model: str,
        api_key: str,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> Optional[str]:
        url = "https://api.anthropic.com/v1/messages"

        formatted_msgs = []
        for m in messages:
            role = "user" if m.get("sender") in ["user", "human"] else "assistant"
            formatted_msgs.append({"role": role, "content": m.get("content", "")})

        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "system": system_prompt,
            "messages": formatted_msgs,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        with httpx.Client(timeout=15.0) as client:
            resp = client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                content_blocks = data.get("content", [])
                if content_blocks and content_blocks[0].get("type") == "text":
                    return content_blocks[0].get("text", "")
            else:
                logger.warning(f"Anthropic error {resp.status_code}: {resp.text}")
        return None
