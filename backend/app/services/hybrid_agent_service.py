"""
AGRO AI — Advanced Hybrid AI Agent Service
Combines:
1. Multi-turn conversation context resolution (pronouns, prior topics)
2. Retrieval-Augmented Generation (RAG) over verified ICAR/TNAU/PAU/FAO knowledge
3. Deterministic farm calculator tools (NPK dosage, seed rate, irrigation, economics)
4. Integration with existing AGRO AI models (39 crop diseases, soil types, 98 botanical species)
5. Multi-provider LLM integration (Gemini, OpenAI, Groq, Ollama, Anthropic)
6. Autonomous Offline Knowledge & Reasoning fallback (zero API dependency)
7. Strict 5-part evidence-based answer structure with verifiable citations
"""

import re
import datetime
from typing import Dict, Any, List, Optional, Tuple

from app.services.knowledge_base import AgriculturalKnowledgeEngine, VERIFIED_KNOWLEDGE_DOCUMENTS
from app.services.farm_calculator import FarmCalculatorService
from app.services.llm_client import LLMClient
from app.services.general_knowledge import GeneralKnowledgeEngine
from app.services.crop_inference import EXPANDED_CROP_KNOWLEDGE_BASE
from app.services.soil_inference import SOIL_KNOWLEDGE_BASE

class HybridAgentService:
    """
    Central reasoning and execution agent for AGRO AI.
    """

    @staticmethod
    def _resolve_context_and_pronouns(
        query: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Inspects recent conversation history to resolve pronouns ("it", "this disease", "how to treat it").
        Returns the resolved query and detected context metadata.
        """
        context_meta: Dict[str, Any] = {
            "resolved_subject": None,
            "crop": None,
            "disease": None,
            "soil": None
        }

        if not history or len(history) == 0:
            return query, context_meta

        # Scan previous turns in reverse
        prev_user_msgs = [h.get("content", "") for h in history if h.get("sender") in ["user", "human"]]
        prev_assistant_msgs = [h.get("content", "") for h in history if h.get("sender") in ["assistant", "model"]]

        all_prev_text = " ".join(prev_user_msgs[-3:] + prev_assistant_msgs[-3:]).lower()

        # Detect active disease in history
        known_diseases = [
            ("tomato early blight", "Tomato Early Blight (Alternaria solani)"),
            ("early blight", "Tomato Early Blight (Alternaria solani)"),
            ("potato late blight", "Potato Late Blight (Phytophthora infestans)"),
            ("late blight", "Potato Late Blight (Phytophthora infestans)"),
            ("wheat rust", "Wheat Rust (Puccinia spp.)"),
            ("yellow rust", "Wheat Stripe/Yellow Rust (Puccinia striiformis)"),
            ("brown rust", "Wheat Leaf/Brown Rust (Puccinia triticina)"),
            ("rice blast", "Rice Blast (Magnaporthe oryzae)"),
            ("brown spot", "Rice Brown Spot (Bipolaris oryzae)"),
            ("apple scab", "Apple Scab (Venturia inaequalis)"),
            ("rose black spot", "Rose Black Spot (Diplocarpon rosae)"),
            ("corn rust", "Common Corn Rust (Puccinia sorghi)"),
        ]
        for term, full_name in known_diseases:
            if term in all_prev_text:
                context_meta["disease"] = full_name
                context_meta["resolved_subject"] = full_name
                break

        # Detect active soil in history
        known_soils = [
            ("black soil", "Black Soil (Vertisol)"),
            ("regur", "Black Soil (Vertisol)"),
            ("alluvial", "Alluvial Soil"),
            ("red soil", "Red Soil (Alfisol)"),
            ("laterite", "Laterite Soil"),
            ("clay soil", "Clay Soil"),
            ("sandy soil", "Sandy Soil")
        ]
        for term, full_name in known_soils:
            if term in all_prev_text:
                context_meta["soil"] = full_name
                if not context_meta["resolved_subject"]:
                    context_meta["resolved_subject"] = full_name
                break

        # Check if current query contains vague pronouns
        q_lower = query.lower()
        pronoun_patterns = [
            r"\bhow to treat it\b", r"\bhow to prevent it\b", r"\bwhat causes it\b",
            r"\bhow can i prevent it\b", r"\bhow can i treat it\b", r"\bhow do i treat it\b",
            r"\bhow do i prevent it\b", r"\bprevent it\b", r"\btreat it\b", r"\bmanage it\b",
            r"\bcontrol measures\b", r"\bhow much fertilizer\b", r"\bwhat crops grow in it\b",
            r"\bhow to improve it\b", r"\bhow to identify it\b", r"\btell me more about it\b"
        ]

        needs_resolution = any(re.search(p, q_lower) for p in pronoun_patterns) or q_lower in [
            "how to prevent it?", "how to treat it?", "what are its symptoms?",
            "what fungicides to use?", "how to manage it?", "which crops?", "how can i prevent it?"
        ]

        resolved_query = query
        if needs_resolution and context_meta["resolved_subject"]:
            resolved_query = f"{query} regarding {context_meta['resolved_subject']}"

        return resolved_query, context_meta

    @staticmethod
    def _detect_calculation_intent(query: str) -> Optional[Dict[str, Any]]:
        """
        Detects if query is a mathematical or farm calculation request.
        """
        q = query.lower()

        # 1. NPK Fertilizer Calculation
        npk_match = re.search(r"(\d+)\s*[-:]\s*(\d+)\s*[-:]\s*(\d+)", q)
        area_match = re.search(r"(\d+(?:\.\d+)?)\s*(ha|hectare|hectares|acre|acres)", q)
        if ("fertilizer" in q or "urea" in q or "dap" in q or "npk" in q) and (npk_match or "calculate" in q):
            n = float(npk_match.group(1)) if npk_match else 120.0
            p = float(npk_match.group(2)) if npk_match else 60.0
            k = float(npk_match.group(3)) if npk_match else 40.0
            area_val = float(area_match.group(1)) if area_match else 1.0
            unit = area_match.group(2) if area_match else "ha"
            use_ssp = "ssp" in q

            calc_result = FarmCalculatorService.calculate_npk_fertilizer(
                target_n=n, target_p=p, target_k=k, area=area_val, unit=unit, use_ssp=use_ssp
            )
            return {"type": "npk_fertilizer", "result": calc_result}

        # 2. Plant Population & Seed Rate
        if ("seed rate" in q or "plant population" in q or "spacing" in q) and any(c in q for c in ["cm", "spacing", "hectare", "acre"]):
            row_match = re.search(r"(\d+(?:\.\d+)?)\s*cm.*?(?:row|between rows)", q) or re.search(r"row.*?(\d+(?:\.\d+)?)\s*cm", q)
            plant_match = re.search(r"(\d+(?:\.\d+)?)\s*cm.*?(?:plant|within row)", q) or re.search(r"plant.*?(\d+(?:\.\d+)?)\s*cm", q)
            row_cm = float(row_match.group(1)) if row_match else 60.0
            plant_cm = float(plant_match.group(1)) if plant_match else 20.0
            area_val = float(area_match.group(1)) if area_match else 1.0
            unit = area_match.group(2) if area_match else "ha"

            calc_result = FarmCalculatorService.calculate_plant_population_and_seed_rate(
                area_val=area_val, area_unit=unit, row_spacing_cm=row_cm, plant_spacing_cm=plant_cm, test_weight_g=40.0
            )
            return {"type": "seed_rate", "result": calc_result}

        # 3. Irrigation Water & Runtime
        if ("irrigation" in q or "water requirement" in q or "drip" in q) and ("runtime" in q or "litre" in q or "litres" in q or "mm" in q):
            area_val = float(area_match.group(1)) if area_match else 1.0
            area_m2 = area_val * (10000.0 if "ha" in (area_match.group(2) if area_match else "ha") else 4046.86)
            calc_result = FarmCalculatorService.calculate_irrigation_water_and_runtime(
                eto_mm_day=4.5, crop_kc=1.15, area_m2=area_m2
            )
            return {"type": "irrigation", "result": calc_result}

        # 4. Farm Economics & Cost
        if ("cost of cultivation" in q or "profit" in q or "bcr" in q or "economics" in q or "gross return" in q) and ("yield" in q or "quintal" in q or "₹" in q or "inr" in q or "rs" in q):
            calc_result = FarmCalculatorService.calculate_farm_economics(
                crop_name="Paddy / Wheat",
                area_val=1.0,
                area_unit="hectare",
                cost_items={
                    "Land Preparation": 6000.0,
                    "Seed & Seed Treatment": 3500.0,
                    "Fertilizers & FYM": 8500.0,
                    "Crop Protection": 3000.0,
                    "Irrigation & Electricity": 4000.0,
                    "Harvesting & Threshing": 8000.0
                },
                expected_yield_quintals=45.0,
                price_per_quintal_inr=2275.0
            )
            return {"type": "economics", "result": calc_result}

        # 5. General Math Expression
        # If string looks like pure math (e.g. "sqrt(144) + 25" or "1250 * 0.18")
        if re.match(r"^[\d\s\+\-\*\/\^\(\)\.\%eE\,]+$", q) and any(c in q for c in "+-*/%"):
            try:
                res = FarmCalculatorService.safe_math_eval(q)
                return {"type": "math_eval", "expression": q, "result": res}
            except Exception:
                pass

        return None

    @classmethod
    def process_query(
        cls,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for processing assistant queries.
        Produces complete 5-part evidence-based answers with verifiable citations.
        """
        q_raw = message.strip()
        q_clean = q_raw.lower()

        # 1. Multi-turn context and pronoun resolution
        resolved_query, context_meta = cls._resolve_context_and_pronouns(q_raw, history)

        # 2. Security guard: prompt injection / jailbreak / system override
        if any(term in q_clean for term in ["system override", "ignore all previous instructions", "reveal your internal secrets", "delete all databases", "jailbreak", "override your instructions"]):
            status = LLMClient.get_status()
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "I am the **AGRO AI Assistant**, a specialized evidence-based agricultural intelligence system. "
                    "I do not execute system shell commands, override core security policies, or disclose internal configuration parameters.\n\n"
                    "### 2. Explanation & Security Posture\n"
                    "All queries are processed within a secure, sandboxed environment designed strictly for agricultural science, "
                    "plant disease diagnosis, soil health advisories, farm engineering calculations, and evidence-based agronomy. "
                    "External instructions cannot alter system guardrails or compromise application integrity.\n\n"
                    "### 3. Supporting Evidence & System Capabilities\n"
                    "**Verified AGRO AI Capabilities:**\n"
                    "• Evidence-based plant pathology and pest management with ICAR and TNAU verified citations.\n"
                    "• Deterministic mathematical calculations (NPK fertilizer dosing, seed rates, irrigation runtimes) using sandboxed AST execution.\n"
                    "• Safe offline knowledge retrieval with zero untrusted code execution.\n\n"
                    "### 4. Practical Action Steps\n"
                    "1. Please submit an agronomic or farming-related question (e.g. crop health, fertilizer requirements, pest management).\n"
                    "2. Use the Farm Calculator to compute precise fertilizer dosages or seed rates.\n"
                    "3. Access Crop Diagnosis to analyze crop leaf conditions with IPM recommendations.\n\n"
                    "### 5. Sources & Limitations\n"
                    "**Primary Standard:** AGRO AI Security & Agronomic Verification Framework. System operations are restricted to verified agricultural advisory protocols."
                ),
                "category": "security",
                "suggestedQuestions": [
                    "How to calculate NPK fertilizer requirements for wheat?",
                    "What are the best soil amendments for Black Soil?",
                    "How to identify Tomato Early Blight?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": status["provider"]
            }

        # 3. Greeting handling (natural response, avoid dumping predefined topic list repeatedly)
        q_clean_alpha = re.sub(r"[^\w\s]", "", q_clean).strip()
        if (
            q_clean_alpha in ["hi", "hello", "hey", "good morning", "good afternoon", "namaste", "vanakkam"]
            or any(q_clean.startswith(g) for g in ["hi ", "hello ", "hey "])
        ):
            status = LLMClient.get_status()
            return {
                "response": (
                    f"Hello! I am your **AGRO AI Assistant** ({status['badge']}).\n\n"
                    "I provide scientifically verified guidance on:\n"
                    "• **Plant Pathology & Pest Management** (symptoms, differential diagnosis, IPM, CIB&RC safe treatments)\n"
                    "• **Soil Health & Nutrient Management** (Vertisols, Alluvial, Red/Laterite, pH, organic amendments)\n"
                    "• **Agronomic Engineering & Calculators** (NPK fertilizer dosage, seed rates, plant population, drip irrigation runtime, farm economics)\n"
                    "• **Crop Cultivation & Sustainable Farming Practices**\n\n"
                    "How can I assist your farm or educational queries today? Feel free to ask a specific question or request a calculation."
                ),
                "category": "general",
                "suggestedQuestions": [
                    "How to calculate NPK fertilizer doses for wheat (120:60:40)?",
                    "How to identify and control Tomato Early Blight?",
                    "What are the best soil improvement methods for Black Soil?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": status["provider"]
            }

        # 4. Check for dedicated mathematical / agricultural calculation intent
        calc_intent = cls._detect_calculation_intent(resolved_query)
        if calc_intent:
            return cls._generate_calculation_response(calc_intent, resolved_query)

        # 4b. Check for natural language math / percentage queries ("what is 15% of 800", etc.)
        math_ans = GeneralKnowledgeEngine._handle_math_query(q_clean)
        if math_ans:
            return math_ans

        # 4c. Check if essential agricultural context is missing and request targeted clarification
        clarification_ans = cls._check_needs_clarification(resolved_query, context_meta)
        if clarification_ans:
            return clarification_ans

        # Answer recognized general questions with the local deterministic handlers
        # before doing retrieval or waiting for a model. Unknown questions continue
        # to the configured model below.
        gen_ans = GeneralKnowledgeEngine.answer_query(resolved_query, history, allow_fallback=False)
        if gen_ans:
            return gen_ans

        # 5. Check for live data requests that require real-time external feeds
        live_data_disclaimer = cls._check_live_data_limitation(resolved_query)

        # Early category classification
        detected_category = cls._categorize_query(resolved_query)

        # 6. Retrieve verified documents from Agricultural Knowledge Base
        retrieved_docs = AgriculturalKnowledgeEngine.search(
            resolved_query,
            category=detected_category if detected_category in ["disease", "soil", "crop_care", "irrigation", "economics", "nutrition"] else None,
            top_k=3
        )

        # 7. Check existing AGRO AI Crop & Soil inference knowledge bases
        crop_disease_info = cls._match_existing_crop_kb(resolved_query) if detected_category in ["disease", "general"] else None
        soil_info = cls._match_existing_soil_kb(resolved_query) if detected_category in ["soil", "general"] else None

        # 8. Check if a live LLM is configured
        llm_provider, llm_model, _ = LLMClient.get_configured_provider()
        llm_response = None

        if llm_provider != "none":
            # Build grounded prompt for LLM
            grounding_text = cls._build_grounding_context(retrieved_docs, crop_disease_info, soil_info)
            system_prompt = (
                "You are the AGRO AI Assistant — an intelligent, friendly, and concise AI agent. "
                "Answer directly in a short, useful response; prioritize the key answer and one practical next step. "
                "Whether the user asks about agricultural science, computer programming, mathematics, general science, "
                "world facts, biographies, cooking, or everyday productivity, provide complete and engaging answers.\n"
                "When answering agricultural queries, provide scientifically verified guidance citing agronomic facts, IPM, and safety."
            )
            chat_history = (history or [])[-4:] + [{"sender": "user", "content": f"{grounding_text}\n\nQuestion: {resolved_query}" if grounding_text else resolved_query}]
            llm_response = LLMClient.generate(system_prompt, chat_history, temperature=0.2, max_tokens=128)

        # If LLM succeeded, return structured LLM response
        if llm_response:
            citations = cls._extract_citations(retrieved_docs)
            suggested_qs = cls._generate_contextual_followups(resolved_query, retrieved_docs)
            category = cls._categorize_query(resolved_query)
            related_action = cls._determine_related_action(category)

            return {
                "response": llm_response,
                "category": category,
                "suggestedQuestions": suggested_qs,
                "evidenceSources": citations,
                "relatedAction": related_action,
                "modelProvider": llm_provider
            }

        # 9. Autonomous Offline Knowledge & Reasoning Routing
        # Check GeneralKnowledgeEngine for specific known domains (coding, math, physics, facts, recipes, conversation)
        # Otherwise synthesize authoritative agricultural evidence response
        return cls._synthesize_offline_evidence_response(
            query=resolved_query,
            retrieved_docs=retrieved_docs,
            crop_disease_info=crop_disease_info,
            soil_info=soil_info,
            context_meta=context_meta,
            live_disclaimer=live_data_disclaimer
        )

    @classmethod
    def _check_live_data_limitation(cls, query: str) -> Optional[Dict[str, str]]:
        """Detects whether user is asking for real-time live market prices or weather."""
        q = query.lower()
        if any(term in q for term in ["mandi price", "market price", "spot price", "today's price", "today price", "rate today", "current price", "mandi rate"]) or ("mandi" in q and ("price" in q or "rate" in q)):
            return {
                "type": "market",
                "disclaimer": (
                    "**Notice on Real-Time Market Data:** Real-time mandi commodity spot prices fluctuate daily based on local arrivals and auction bidding. "
                    "For verified spot prices across APMC mandis, consult the official Government of India Agmarknet portal ([agmarknet.gov.in](https://agmarknet.gov.in)). "
                    "The Minimum Support Price (MSP) notified by the Ministry of Agriculture and Farmers Welfare (MoA&FW) serves as the statutory price benchmark."
                ),
                "direct_ans": (
                    "Real-time mandi commodity spot prices vary daily across APMC agricultural markets. "
                    "Official live daily price bulletins should be verified directly on the Government of India **Agmarknet portal** ([agmarknet.gov.in](https://agmarknet.gov.in)). "
                    "Statutory floor prices are governed by the annual Minimum Support Price (MSP) notified by the Commission for Agricultural Costs and Prices (CACP)."
                ),
                "explanation": (
                    "Agricultural commodity spot pricing in India is determined by daily physical arrivals, grade-wise moisture content, "
                    "inter-state transport costs, and demand-supply dynamics at registered APMC mandis. "
                    "While seasonal historical trends can be referenced, spot transactions must rely on official live Agmarknet reports."
                )
            }
        if any(term in q for term in ["weather today", "rain today", "tomorrow weather", "live temperature", "weather forecast"]) or ("weather" in q and ("today" in q or "live" in q or "rain" in q)):
            return {
                "type": "weather",
                "disclaimer": (
                    "**Notice on Real-Time Meteorological Data:** Live satellite, Doppler weather radar, and precipitation tracking require real-time telemetry feeds. "
                    "For hyper-local weather forecasts and agromet advisories, consult the India Meteorological Department ([mausam.imd.gov.in](https://mausam.imd.gov.in)) "
                    "or the official IMD/ICAR Meghdoot mobile advisory application."
                ),
                "direct_ans": (
                    "Live hyper-local weather conditions and short-term rainfall predictions depend on real-time radar and station telemetry. "
                    "For certified daily forecasts and farm agromet advisories, consult the **India Meteorological Department (IMD)** at [mausam.imd.gov.in](https://mausam.imd.gov.in) "
                    "or the official IMD/ICAR **Meghdoot** agromet application."
                ),
                "explanation": (
                    "Micro-climatic conditions such as relative humidity, wind velocity, and localized convection require continuous satellite and automatic weather station (AWS) feeds. "
                    "Farmers should utilize IMD's district-level Agromet Field Unit (AMFU) bulletins issued every Tuesday and Friday for farm-level spraying and irrigation scheduling."
                )
            }
        return None

    @classmethod
    def _check_needs_clarification(cls, query: str, context_meta: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Detects underspecified agricultural queries (e.g. asking what to spray or how much fertilizer)
        where essential context (crop name, field size, or symptom specifics) is missing.
        Asks a polite, targeted clarifying question rather than guessing or prescribing blindly.
        """
        q = query.lower().strip()
        if context_meta.get("disease") or context_meta.get("crop") or context_meta.get("soil"):
            return None

        known_crops = [
            "tomato", "potato", "wheat", "rice", "paddy", "maize", "corn", "cotton",
            "sugarcane", "apple", "grape", "rose", "banana", "mango", "chilli", "onion",
            "soybean", "groundnut", "c3", "c4", "blight", "rust", "scab", "mildew", "fusarium",
            "vertisol", "alluvial", "regur", "laterite"
        ]
        has_specific_subject = any(c in q for c in known_crops)

        # 1. Underspecified spray / pesticide / medicine query without crop or disease
        is_vague_spray = any(p in q for p in [
            "what should i spray", "which spray", "what medicine", "which medicine",
            "what fungicide to spray", "what pesticide to spray", "what chemical to use",
            "how to cure my crop", "how to cure my plant", "my plant is sick", "my crop is sick"
        ])
        if is_vague_spray and not has_specific_subject:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "To recommend the correct Integrated Pest Management (IPM) measures or treatment, "
                    "I need a few essential details about your plant. Chemical sprays must never be applied without knowing the crop and causal problem.\n\n"
                    "### 2. Information Needed\n"
                    "Please let me know:\n"
                    "1. **Which Crop or Plant?** (e.g. Tomato, Potato, Wheat, Cotton, Chilli, or a garden plant)\n"
                    "2. **What Symptoms do you observe?** (e.g. Concentric leaf rings, powdery white coating, leaf yellowing, wilting, or holes)\n"
                    "3. **Affected Parts:** Are symptoms visible on bottom leaves, new shoots, stems, or fruits?\n\n"
                    "💡 *Tip: You can also take a photo of the affected leaf and use our **Crop Health Vision Scanner** to analyze it automatically!*"
                ),
                "category": "disease",
                "suggestedQuestions": [
                    "How to manage Tomato Early Blight with IPM?",
                    "What are symptoms of Wheat Stripe Rust?",
                    "How to control powdery mildew organically?"
                ],
                "evidenceSources": [],
                "relatedAction": {"label": "Scan Leaf Photo (Crop Diagnosis)", "route": "/production/crop"},
                "modelProvider": "clarification_engine"
            }

        # 2. Underspecified fertilizer query without crop or field size
        is_vague_fert = any(p in q for p in [
            "what fertilizer to use", "what fertilizer should i use", "how much fertilizer",
            "which fertilizer is best", "what fertilizer should i add", "fertilizer dose"
        ]) and not any(f in q for f in ["npk", "120", "urea", "dap", "wheat", "rice", "cotton", "corn", "soil", "vertisol", "alluvial"])
        if is_vague_fert and not has_specific_subject:
            return {
                "response": (
                    "### 1. Direct Answer\n"
                    "Fertilizer recommendations vary significantly depending on the crop species, growth stage, "
                    "and existing soil fertility levels. Applying fertilizers without these details risks fertilizer salt burn or nutrient imbalance.\n\n"
                    "### 2. Information Needed\n"
                    "To calculate the exact fertilizer dosage (Urea, DAP, MOP), please share:\n"
                    "1. **Crop Name:** Which crop are you cultivating?\n"
                    "2. **Field Size:** What is your plot or field area (e.g. 1 acre, 2 hectares, or garden pots)?\n"
                    "3. **Soil Type:** Do you know your soil type (e.g. Black Vertisol, Alluvial, Red soil) or Soil Health Card values?\n\n"
                    "💡 *You can also use our **Farm Calculators** (click Calculators above) to compute precise NPK dosages instantly!*"
                ),
                "category": "crop_care",
                "suggestedQuestions": [
                    "Calculate NPK fertilizer for 1 hectare wheat (120:60:40)",
                    "What are the best fertilizers for Black Soil?",
                    "How much Single Superphosphate (SSP) equals 50 kg DAP?"
                ],
                "evidenceSources": [],
                "relatedAction": None,
                "modelProvider": "clarification_engine"
            }

        return None

    @classmethod
    def _match_existing_crop_kb(cls, query: str) -> Optional[Dict[str, Any]]:
        """Matches query against the existing 39 conditions in crop_inference.py."""
        q = query.lower()
        for key, data in EXPANDED_CROP_KNOWLEDGE_BASE.items():
            crop_name = data.get("crop", "").lower()
            cond_name = data.get("condition", "").lower()
            if cond_name in q or (crop_name in q and any(w in q for w in cond_name.split() if w not in STOPWORDS)):
                return data
        return None

    @classmethod
    def _match_existing_soil_kb(cls, query: str) -> Optional[Dict[str, Any]]:
        """Matches query against the existing soil categories in soil_inference.py."""
        q = query.lower()
        for soil_type, data in SOIL_KNOWLEDGE_BASE.items():
            if soil_type.lower() in q:
                return {"soil_type": soil_type, **data}
        return None

    @classmethod
    def _build_grounding_context(
        cls,
        docs: List[Dict[str, Any]],
        crop_info: Optional[Dict[str, Any]],
        soil_info: Optional[Dict[str, Any]]
    ) -> str:
        parts = []
        for i, d in enumerate(docs):
            parts.append(
                f"[Document {i+1}]: {d.get('title')} ({d.get('organization')}, {d.get('publication_year')})\n"
                f"Summary: {d.get('summary')}\n"
                f"Scientific Context: {d.get('scientific_explanation')}\n"
                f"Practical Steps: {' | '.join(d.get('practical_steps', []))}\n"
                f"Limitations: {d.get('limitations', '')}"
            )
        if crop_info:
            parts.append(
                f"[AGRO AI Crop Diagnostics Database]: Crop: {crop_info.get('crop')} | Condition: {crop_info.get('condition')}\n"
                f"Explanation: {crop_info.get('explanation')}\n"
                f"Recommendations: {json_snippet(crop_info.get('recommendations', []))}"
            )
        if soil_info:
            parts.append(
                f"[AGRO AI Soil Classification Database]: Soil: {soil_info.get('soil_type')}\n"
                f"Guidance: {soil_info.get('description', '')}\n"
                f"Suitable Crops: {', '.join(soil_info.get('suitable_crops', []))}"
            )
        return "\n\n".join(parts) if parts else "Standard agricultural and general scientific reference database."

    @classmethod
    def _synthesize_offline_evidence_response(
        cls,
        query: str,
        retrieved_docs: List[Dict[str, Any]],
        crop_disease_info: Optional[Dict[str, Any]],
        soil_info: Optional[Dict[str, Any]],
        context_meta: Dict[str, Any],
        live_disclaimer: Optional[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Synthesizes a rich, authoritative 5-part evidence-based answer
        directly from verified extension records when running offline.
        """
        category = cls._categorize_query(query)
        related_action = cls._determine_related_action(category)

        # 1. Primary document
        primary_doc = retrieved_docs[0] if retrieved_docs else None

        evidence = None
        practical_steps = None
        sources_summary = None
        limitations_text = None

        # Build 5 sections
        # --- Section 1: Direct Answer & Section 2: Explanation ---
        if live_disclaimer:
            direct_ans = live_disclaimer["direct_ans"]
            explanation = live_disclaimer["explanation"]
            evidence = (
                "**Regulatory Benchmarks & Live Telemetry:**\n"
                "• Statutory Pricing Standard: Directorate of Economics and Statistics (DES), MoA&FW.\n"
                "• Daily Bulletin Portal: Agmarknet APMC Auction Database / IMD Automated Weather Stations (AWS)."
            )
            practical_steps = (
                "1. Check Live Mandi Prices: Visit [agmarknet.gov.in](https://agmarknet.gov.in) to inspect today's modal price and physical arrivals at your district mandi.\n"
                "2. Benchmark Minimum Support Price (MSP): Verify that local farmgate offers do not fall unreasonably below the national MSP floor.\n"
                "3. Consult District Agromet Bulletin: Review IMD's bi-weekly agromet advisory before scheduling fertilizer application or harvesting."
            )
            sources_summary = "**Primary Citation:** [Agmarknet Market Information System](https://agmarknet.gov.in) / [IMD National Weather Portal](https://mausam.imd.gov.in)."
            limitations_text = "Spot prices and meteorological conditions fluctuate hour-by-hour; always confirm before executing farm sales or pesticide sprays."
            category = live_disclaimer.get("type", "economics")
        elif primary_doc:
            direct_ans = primary_doc.get("summary", "")
            explanation = primary_doc.get("scientific_explanation", "")
        elif crop_disease_info:
            direct_ans = (
                f"**{crop_disease_info.get('condition')}** affecting **{crop_disease_info.get('crop')}**. "
                f"{crop_disease_info.get('explanation')}"
            )
            explanation = (
                f"Pathological mechanics: Symptoms develop as pathogen structures infiltrate host mesophyll tissue. "
                f"Unchecked progression impairs leaf photosynthesis, reducing vascular fluid translocation. "
                f"Disease severity is magnified under persistent foliage moisture (>7 hours) and moderate temperatures."
            )
        elif soil_info:
            direct_ans = (
                f"**{soil_info.get('soil_type')}**: {soil_info.get('description', 'High agricultural importance soil category.')} "
                f"Highly suitable for: {', '.join(soil_info.get('suitable_crops', [])[:6])}."
            )
            explanation = (
                f"Pedological mechanics: Soil chemical dynamics (pH, cation exchange capacity, organic matter) "
                f"dictate root nutrient bioavailability. Adequate organic matter buffers soil against pH extremes "
                f"and stimulates beneficial mycorrhizal and bacterial populations that unlock native phosphorus."
            )
        elif category == "disease" and not primary_doc and not crop_disease_info:
            direct_ans = (
                f"Based on the reported symptoms ('{query.strip()}'), the condition cannot be conclusively matched "
                "to a single known pathogen. In agricultural plant pathology, atypical lesions, discoloration, or markings "
                "require systematic diagnostic inspection to distinguish physiological abiotic disorders (nutrient toxicities, "
                "pesticide phytotoxicity, viral variegation) from fungal or bacterial infections."
            )
            explanation = (
                "**Diagnostic Triage & Differential Diagnosis:**\n"
                "• **Fungal / Bacterial Leaf Spots**: Characterized by progressive chlorotic yellow halos, necrotic tissue collapse, "
                "or water-soaking that expands under leaf wetness.\n"
                "• **Viral Infection / Genetic Chimera**: Often manifests as distinct geometric mosaic patterns, leaf distortion, or unusual discoloration without fungal spore structures.\n"
                "• **Nutrient Toxicity or Chemical Drift**: Spray burn, fertilizer salt accumulation, or herbicide drift can create localized irregular scorching or purplish pigment expression.\n"
                "• **Entomological Injury**: Mite feeding (russeting/bronzing) or sucking pests (thrips, whiteflies) can cause silvery flecks and leaf curling."
            )
            evidence = (
                "**Field Diagnostic Protocol (ICAR-KVK Guidelines):**\n"
                "• Do not apply broad-spectrum chemical fungicides or pesticides without confirming the causal organism.\n"
                "• Examine the undersides of leaves with a 10x hand lens for signs of fungal fruiting bodies (pycnidia, conidiophores), webbing, or insect frass.\n"
                "• Check new growth versus mature bottom foliage to determine whether symptoms are systemic or localized."
            )
            practical_steps = (
                "1. Isolate Sample: Carefully place 3-4 affected leaves inside a dry paper envelope (not sealed plastic) along with photos of the entire plant canopy.\n"
                "2. Visit Local KVK: Submit the fresh sample to your nearest Krishi Vigyan Kendra (KVK) or State Agricultural University plant clinic for microscopic smear examination.\n"
                "3. Cultural Sanitation: Prune severely symptomatic foliage with sterilized shears and dispose of away from healthy crops.\n"
                "4. Maintain Plant Vigour: Ensure adequate balanced root hydration (avoid waterlogging) and withhold excessive nitrogenous fertilization until diagnosis is confirmed."
            )
            sources_summary = "**Primary Citation:** [ICAR Krishi Vigyan Kendra Portal](https://kvk.icar.gov.in) (Indian Council of Agricultural Research, New Delhi)."
            limitations_text = (
                "Visual descriptions alone cannot replace lab diagnostic culturing. Never apply unverified pesticides or chemical mixes based on unconfirmed diagnoses. "
                "Consult your district Krishi Vigyan Kendra (KVK) or State Department of Agriculture extension officer."
            )
        elif category == "clarification":
            direct_ans = (
                f"I am the **AGRO AI Assistant**. While your inquiry touches on '{query.strip()}', "
                "my primary scientific specialization is in agricultural sciences, plant pathology, soil chemistry, "
                "fertilizer calculations, farm economics, and nutritional science."
            )
            explanation = (
                "Our agronomic intelligence platform provides evidence-based assistance for crop health, "
                "soil nutrient replenishment, irrigation engineering, and farm budgeting. For general questions, "
                "we connect physical and biological principles back to sustainable agricultural systems."
            )
        else:
            q_low = query.lower()
            is_agri = any(w in q_low for w in [
                "soil", "crop", "plant", "leaf", "leaves", "farm", "fertilizer", "seed",
                "wilt", "blight", "pest", "spray", "water", "yield", "field", "turmeric",
                "wheat", "rice", "tomato", "potato", "paddy", "cure"
            ])
            if not is_agri:
                gen_ans = GeneralKnowledgeEngine.answer_query(query, allow_fallback=True)
                if gen_ans:
                    return gen_ans

            direct_ans = (
                f"Addressing your inquiry on **{query.strip()}**: Sustainable agricultural productivity relies on "
                "integrating soil organic fertility, balanced nutrient replenishment (INM), certified disease-free seeds, "
                "and proactive integrated pest and disease management (IPM)."
            )
            explanation = (
                "Agronomic principles require maintaining balanced soil microbial activity, optimal soil moisture "
                "near field capacity (avoiding waterlogging and drought stress), and targeted nutrient budgeting "
                "derived from routine Soil Health Card testing."
            )

        # --- Section 3: Supporting Evidence or Calculations ---
        if evidence is None:
            diff_diag_text = ""
            if primary_doc and primary_doc.get("differential_diagnosis"):
                diff_items = primary_doc["differential_diagnosis"]
                diff_diag_text = "\n\n**Differential Diagnosis & Diagnostic Clues:**\n"
                for d in diff_items:
                    diff_diag_text += f"• **{d['condition']}**: {d['distinction']}\n"
            elif crop_disease_info and crop_disease_info.get("recommendations"):
                recs = crop_disease_info["recommendations"]
                diff_diag_text = "\n\n**Verified Field Findings (AGRO AI Diagnostics):**\n"
                for r in recs[:3]:
                    diff_diag_text += f"• **{r.get('title')}**: {r.get('description')}\n"

            evidence = (
                f"**Verified Agronomic Findings:**\n"
                f"• Source Standard: {primary_doc['organization'] if primary_doc else 'ICAR-National Agricultural Research System'}\n"
                f"• Recommended Practice: Field-tested integrated management protocols calibrated for agro-climatic conditions."
                f"{diff_diag_text}"
            )

        # --- Section 4: Practical Action Steps ---
        if practical_steps is None:
            if primary_doc and primary_doc.get("practical_steps"):
                practical_steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(primary_doc["practical_steps"])])
            elif crop_disease_info and crop_disease_info.get("prevention_tips"):
                practical_steps = "\n".join([f"{i+1}. {tip}" for i, tip in enumerate(crop_disease_info["prevention_tips"])])
            elif soil_info and soil_info.get("management_practices"):
                practical_steps = "\n".join([f"{i+1}. {p}" for i, p in enumerate(soil_info["management_practices"])])
            else:
                practical_steps = (
                    "1. Soil Testing: Sample soil at 0-15 cm depth and obtain a certified 12-parameter Soil Health Card analysis.\n"
                    "2. Organic Foundation: Incorporate 8-10 tonnes/ha well-decomposed FYM or 3-4 tonnes/ha vermicompost before sowing.\n"
                    "3. Seed Treatment: Coat certified seed with bio-fungicide (Trichoderma @ 5g/kg) or Rhizobium/Azospirillum inoculant.\n"
                    "4. Water Management: Use precision drip or furrow irrigation to minimize canopy moisture and conserve groundwater."
                )

        # --- Section 5: Sources & Limitations ---
        sources_list = cls._extract_citations(retrieved_docs)
        if sources_summary is None:
            if primary_doc:
                sources_summary = f"**Primary Citation:** [{primary_doc['title']}]({primary_doc['url']}) ({primary_doc['organization']}, {primary_doc['publication_year']})."
            else:
                sources_summary = "**Primary Citation:** [ICAR National Agricultural Portal](https://icar.org.in) (Indian Council of Agricultural Research, New Delhi)."

        if limitations_text is None:
            limitations_text = (
                primary_doc.get("limitations", "") if primary_doc else
                "Local weather, soil pH, and regional pest biotypes influence field outcomes. Verify specific chemical choices with your local Krishi Vigyan Kendra (KVK) or State Department of Agriculture."
            )

        # Compile full structured Markdown text
        full_response = (
            f"### 1. Direct Answer\n{direct_ans}\n\n"
            f"### 2. Explanation & Scientific Reasoning\n{explanation}\n\n"
            f"### 3. Supporting Evidence & Diagnostic Clues\n{evidence}\n\n"
            f"### 4. Practical Action Steps\n{practical_steps}\n\n"
            f"### 5. Sources & Limitations\n{sources_summary}\n\n"
            f"**Limitations & Safety Precautions:** {limitations_text}"
        )

        if live_disclaimer and live_disclaimer.get("disclaimer"):
            full_response = f"{live_disclaimer['disclaimer']}\n\n" + full_response

        suggested_qs = cls._generate_contextual_followups(query, retrieved_docs)

        return {
            "response": full_response,
            "category": category,
            "suggestedQuestions": suggested_qs,
            "evidenceSources": sources_list,
            "relatedAction": related_action,
            "modelProvider": "offline_knowledge_engine"
        }

    @classmethod
    def _generate_calculation_response(cls, calc_intent: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Formats mathematical and agricultural calculations into the 5-part structure."""
        ctype = calc_intent.get("type")
        res = calc_intent.get("result", {})

        if ctype == "npk_fertilizer":
            direct_ans = (
                f"For an area of **{res.get('area')} {res.get('unit')}(s)** with target **{res['targetNutrients']['N_kg']} kg N, "
                f"{res['targetNutrients']['P2O5_kg']} kg P2O5, and {res['targetNutrients']['K2O_kg']} kg K2O**, apply:\n\n"
                f"• **DAP (18:46:0):** **{res['fertilizers'][0]['quantityKg']} kg** ({res['fertilizers'][0]['bags']} bags of 50 kg)\n"
                f"• **Urea (46% N):** **{res['fertilizers'][1]['quantityKg']} kg** ({res['fertilizers'][1]['bags']} bags of 45 kg)\n"
                f"• **MOP (60% K2O):** **{res['fertilizers'][2]['quantityKg']} kg** ({res['fertilizers'][2]['bags']} bags of 50 kg)"
            )
            explanation = (
                "**Dual-Nutrient Arithmetic:** DAP supplies both Phosphorus (46% P2O5) and Nitrogen (18% N). "
                f"Applying {res['fertilizers'][0]['quantityKg']} kg of DAP contributes {round(res['fertilizers'][0]['quantityKg']*0.18, 1)} kg of Nitrogen. "
                "This contributed Nitrogen must be subtracted from the total target Nitrogen to avoid over-fertilization, "
                "with only the remaining deficit supplied via Urea."
            )
            steps = "\n".join(res.get("calculationSteps", []))
            sched = "\n".join([f"{i+1}. {s}" for i, s in enumerate(res.get("splitSchedule", []))])

            full_resp = (
                f"### 1. Direct Answer\n{direct_ans}\n\n"
                f"### 2. Explanation & Scientific Reasoning\n{explanation}\n\n"
                f"### 3. Step-by-Step Mathematical Calculations\n{steps}\n\n"
                f"### 4. Practical Fertilizer Application Schedule\n{sched}\n\n"
                f"### 5. Sources & Limitations\n"
                f"**Source:** [ICAR-IARI Integrated Nutrient Management Guidelines](https://www.iari.res.in) (Indian Agricultural Research Institute, New Delhi).\n\n"
                f"**Limitations:** Broadcast urea on dry soil can suffer up to 30% volatile ammonia loss. Incorporate into moist soil or irrigate within 24 hours."
            )
            return {
                "response": full_resp,
                "category": "crop_care",
                "suggestedQuestions": [
                    "What if I use Single Superphosphate (SSP) instead of DAP?",
                    "How to apply Zinc Sulphate with NPK fertilizers?",
                    "When is the best time to apply topdress Urea?"
                ],
                "evidenceSources": [{
                    "title": "ICAR-IARI: Handbook of Integrated Nutrient Management & Fertilizer Dose Calculations",
                    "organization": "ICAR-Indian Agricultural Research Institute (IARI), New Delhi",
                    "year": "2023",
                    "url": "https://www.iari.res.in",
                    "category": "fertilizer"
                }],
                "calculatorData": res,
                "relatedAction": None,
                "modelProvider": "farm_calculator"
            }

        elif ctype == "seed_rate":
            direct_ans = (
                f"For **{res.get('area')} {res.get('areaUnit')}** with row spacing of **{res.get('rowSpacingCm')} cm** "
                f"and plant spacing of **{res.get('plantSpacingCm')} cm**:\n\n"
                f"• **Theoretical Plant Population:** **{res.get('plantPopulation'):,} plants**\n"
                f"• **Recommended Seed Rate:** **{res.get('seedRateKg')} kg** ({res.get('seedRateQuintals')} Quintals)"
            )
            steps = "\n".join(res.get("calculationSteps", []))
            full_resp = (
                f"### 1. Direct Answer\n{direct_ans}\n\n"
                f"### 2. Explanation & Scientific Reasoning\n"
                f"Plant population is determined by the reciprocal of the ground area per plant. "
                f"The seed rate accounts for imperfect field emergence by dividing pure seed requirement "
                f"by the Seed Utility Factor (Germination % × Purity %).\n\n"
                f"### 3. Step-by-Step Calculations\n{steps}\n\n"
                f"### 4. Practical Sowing Steps\n"
                f"1. Calibrate seed drill cups to dispense exact seeds per linear meter.\n"
                f"2. Conduct a wet-cloth germination test 7 days before sowing to verify field germination.\n"
                f"3. Thin crowded seedlings at 12-15 days after emergence to prevent intra-crop competition.\n\n"
                f"### 5. Sources & Limitations\n"
                f"**Source:** [Directorate of Economics and Statistics (DES), MoA&FW: Seed Rate Standards](https://eands.dacnet.nic.in).\n\n"
                f"**Limitations:** Heavy clay crusting or soil-borne damping-off can reduce emergence. Increase seed rate by 10% under unlevelled or cloddy seedbeds."
            )
            return {
                "response": full_resp,
                "category": "crop_care",
                "suggestedQuestions": [
                    "How to perform a seed germination test at home?",
                    "What seed treatment protects seedlings from damping-off?",
                    "How does plant spacing affect weed competition?"
                ],
                "evidenceSources": [{
                    "title": "Directorate of Economics and Statistics (DES), MoA&FW: Farm Costing Standards & Seed Rate Formulas",
                    "organization": "Ministry of Agriculture & Farmers Welfare",
                    "year": "2023",
                    "url": "https://eands.dacnet.nic.in",
                    "category": "economics"
                }],
                "calculatorData": res,
                "relatedAction": None,
                "modelProvider": "farm_calculator"
            }

        elif ctype == "math_eval":
            expr = calc_intent.get("expression")
            val = calc_intent.get("result")
            full_resp = (
                f"### 1. Direct Answer\n"
                f"The evaluated result of `{expr}` is **{val}**.\n\n"
                f"### 2. Explanation & Mathematical Steps\n"
                f"• Expression: `{expr}`\n"
                f"• Computation: Evaluated deterministically using safe operator parsing.\n"
                f"• Numeric Value: **{val}**\n\n"
                f"### 3. Sources & Limitations\n"
                f"Calculated deterministically using Python standard mathematical library. Zero arbitrary code execution."
            )
            return {
                "response": full_resp,
                "category": "general",
                "suggestedQuestions": [],
                "evidenceSources": [],
                "calculatorData": {"expression": expr, "result": val},
                "relatedAction": None,
                "modelProvider": "safe_math_engine"
            }

        return cls._synthesize_offline_evidence_response(query, [], None, None, {}, None)

    @classmethod
    def _extract_citations(cls, docs: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        citations = []
        seen = set()
        for d in docs:
            key = (d.get("title"), d.get("url"))
            if key not in seen:
                seen.add(key)
                citations.append({
                    "title": d.get("title", ""),
                    "organization": d.get("organization", ""),
                    "year": d.get("publication_year", ""),
                    "url": d.get("url", ""),
                    "category": d.get("category", "agriculture")
                })
        return citations

    @classmethod
    def _generate_contextual_followups(cls, query: str, docs: List[Dict[str, Any]]) -> List[str]:
        q = query.lower()
        if "blight" in q or "disease" in q or "rust" in q:
            return [
                "What is the difference between Early Blight and Late Blight?",
                "What organic bio-pesticides are registered for fungal leaf spots?",
                "How does drip irrigation prevent fungal spore splash?"
            ]
        if "soil" in q or "vertisol" in q or "clay" in q or "alluvial" in q:
            return [
                "What are the best soil amendments for acidic red soil?",
                "How to calculate gypsum requirement for alkaline soil?",
                "Which cover crops increase soil organic carbon fastest?"
            ]
        if "fertilizer" in q or "urea" in q or "dap" in q or "npk" in q:
            return [
                "What is the optimal NPK split for rice and wheat?",
                "How to prepare Jeevamrutha bio-formulation?",
                "How much Single Superphosphate (SSP) equals 50 kg DAP?"
            ]
        if "irrigation" in q or "water" in q:
            return [
                "How does drip irrigation compare to sprinkler irrigation in water savings?",
                "What is Alternate Wetting and Drying (AWD) in paddy?",
                "How to calculate daily crop evapotranspiration (ETc)?"
            ]
        return [
            "How to calculate NPK fertilizer requirements for 1 acre?",
            "What crops are most suitable for Black Vertisol soil?",
            "How to identify Tomato Early Blight from leaf spots?"
        ]

    @classmethod
    def _categorize_query(cls, query: str) -> str:
        q = query.lower()
        if any(w in q for w in ["calorie", "diet", "bmr", "tdee", "protein", "nutrition"]):
            return "nutrition"
        if any(w in q for w in ["fertilizer", "urea", "dap", "mop", "ssp", "npk", "compost", "manure", "nitrogen", "phosphorus", "potassium", "nutrient"]):
            return "crop_care"
        if any(w in q for w in ["blight", "rust", "scab", "mildew", "fungicide", "disease", "pest", "pathogen"]):
            return "disease"
        if any(w in q for w in ["soil", "vertisol", "alluvial", "laterite", "clay", "sand", "regur"]) or re.search(r"\bph\b", q):
            return "soil"
        if any(w in q for w in ["water", "irrigation", "drip", "sprinkler", "eto", "kc"]):
            return "irrigation"
        if any(w in q for w in ["cost", "profit", "seed rate", "population", "quintal", "bcr", "msp"]):
            return "economics"
        if any(w in q for w in ["random", "outer space", "clarification", "tell me something random", "joke"]):
            return "clarification"
        return "general"

    @classmethod
    def _determine_related_action(cls, category: str) -> Optional[Dict[str, str]]:
        if category == "disease":
            return {"label": "Scan Leaf Photo (Crop Diagnosis)", "route": "/production/crop"}
        if category == "soil":
            return {"label": "Analyze Soil Sample", "route": "/production/soil"}
        if category == "nutrition":
            return {"label": "Generate 7-Day Diet Plan", "route": "/nutrition"}
        return None

def json_snippet(obj: Any) -> str:
    try:
        import json
        return json.dumps(obj)[:300]
    except Exception:
        return str(obj)[:300]
