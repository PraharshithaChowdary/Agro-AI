"""
AGRO AI — Assistant Service
Upgraded to use HybridAgentService combining multi-turn context resolution,
retrieval-augmented generation (RAG) over verified ICAR/TNAU/FAO knowledge,
deterministic farm calculation tools, and configurable LLM integration.
"""

from typing import Dict, Any, List, Optional
from app.services.hybrid_agent_service import HybridAgentService

class AssistantService:
    @staticmethod
    def process_query(
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes query via the Hybrid AI Agent Engine.
        """
        return HybridAgentService.process_query(message, history=history, user_id=user_id)
