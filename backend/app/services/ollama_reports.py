"""Translate Ollama's normalized visual report into the stable AGRO AI API contracts."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.services.ollama_service import OllamaService


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _text(value: Any, fallback: str = "") -> str:
    val = str(value or "").strip()
    return val or fallback


def _expand_crop_report(report: Dict[str, Any]) -> Optional[str]:
    """Use the fast text model to turn image findings into a readable short report."""
    evidence = {
        "image_type": report.get("image_type"),
        "subject_name": report.get("subject_name"),
        "visible_condition": report.get("visible_condition"),
        "visible_observations": report.get("visible_observations", []),
        "possible_issues": report.get("possible_issues", []),
        "image_summary": report.get("summary"),
        "ripeness_status": report.get("ripeness_status"),
        "spoilage_status": report.get("spoilage_status"),
    }
    system_prompt = (
        "Write a useful, concise crop-photo report using only the supplied image findings. "
        "Use these headings: Image finding, Assessment, Next steps. Restate only the listed visible signs; "
        "do not add symptoms, diagnoses, or causes. Assessment may only restate the supplied condition and possible issue. "
        "Next steps must be low-risk observation, sanitation, or local expert confirmation. "
        "No pesticide, chemical, fertilizer, or dosage advice, and no measured percentages. "
        "If findings are uncertain, say so. Keep the report under 70 words."
    )
    try:
        narrative = OllamaService.generate_text(
            system_prompt,
            [{"sender": "user", "content": json.dumps(evidence, ensure_ascii=False)}],
            temperature=0.1,
            max_tokens=128,
        )
        if not narrative:
            return None
        source_text = json.dumps(evidence, ensure_ascii=False).lower()
        unsupported_causes = (
            "dehydration", "drought", "nutrient deficiency", "fungal infection",
            "bacterial infection", "viral infection", "pest attack", "overwatering",
        )
        if any(term in narrative.lower() and term not in source_text for term in unsupported_causes):
            return None
        # Lightweight chat models sometimes echo the prompt's schema instead of
        # producing a useful report. Treat those as a failed expansion.
        lower_narrative = narrative.lower()
        if any(token in lower_narrative for token in (
            "one short visible fact", "possible issue: possible issue",
            "visible observations: []", "subject_name", "image_type",
            "no further action is necessary", "no action is needed",
            "possible issue: uncertain", "possible issue: unknown",
        )):
            return None
        headings = ("Image finding", "Assessment", "Next steps")
        if not all(re.search(rf"\b{heading}\s*:", narrative, re.IGNORECASE) for heading in headings):
            return None
        next_steps = re.search(r"(?is)Next steps\s*:\s*(.+)$", narrative)
        action_verbs = r"\b(monitor|inspect|check|retake|take|compare|ask|consult|confirm|photograph|observe|review|isolate|remove|record|continue)\b"
        if not next_steps or not re.search(action_verbs, next_steps.group(1), re.IGNORECASE):
            return None
        narrative = re.sub(
            r"\s*(Image finding|Assessment|Next steps)\s*:",
            r"\n\1:",
            narrative,
            flags=re.IGNORECASE,
        ).lstrip()
        return narrative
    except Exception:
        return None


def _crop_report_from_findings(report: Dict[str, Any]) -> str:
    """Build a complete, evidence-grounded report when Qwen is unavailable or unhelpful."""
    subject = _text(report.get("subject_name"), report.get("image_type", "crop").replace("_", " "))
    condition = _text(report.get("visible_condition"), "uncertain").replace("_", " ")
    observations = report.get("visible_observations") or []
    issues = report.get("possible_issues") or []

    finding = "; ".join(str(item) for item in observations[:2] if str(item).strip())
    if not finding and issues:
        finding = _text(issues[0].get("evidence"))
    if not finding:
        summary = _text(report.get("summary"))
        if summary.lstrip().startswith("{") or "image_type" in summary.lower():
            summary = "The photo needs a clearer view for a reliable identification."
        finding = summary or "No distinct visual sign was confidently identified."

    assessment = f"The image appears to show {subject}. Visible condition: {condition}."
    if issues:
        issue = issues[0]
        assessment += f" Possible issue: {_text(issue.get('name'), 'visible stress')} ({_text(issue.get('likelihood'), 'low')} likelihood), based on the image only."
    elif condition == "uncertain":
        assessment += " The photo does not support a more specific assessment."

    if condition in {"possible stress", "possible spoilage", "overripe"} or issues:
        next_steps = "Inspect the same area and nearby plants, take a clear close-up in natural light, and ask a local agricultural adviser to confirm the cause before treatment."
    elif condition == "uncertain":
        next_steps = "Retake a sharp close-up in natural daylight with the subject filling the frame; include a second photo of the whole plant for context."
    else:
        next_steps = "Continue routine monitoring and compare a follow-up photo of the same area if its appearance changes."

    return f"Image finding: {finding}\n\nAssessment: {assessment}\n\nNext steps: {next_steps}"


def _condition(report: Dict[str, Any]) -> str:
    return str(report.get("visible_condition", "uncertain"))


def _health_assessment(report: Dict[str, Any]) -> tuple[str, float]:
    condition = _condition(report)
    issues = report.get("possible_issues") or []
    # This general vision model has no field-calibrated health scoring benchmark.
    # Keep the required legacy numeric field at zero to mean "not calibrated";
    # the UI explains the qualitative status instead of showing a fake percentage.
    if condition == "healthy-looking" and not issues:
        return "Healthy-looking", 0.0
    if condition in {"ripe", "unripe"} and not issues:
        return "Healthy-looking", 0.0
    if condition == "possible_spoilage" or report.get("spoilage_status") == "possible_visible_spoilage":
        return "Possible Symptoms / Damage Observed", 0.0
    if condition == "possible_stress" or condition == "overripe" or issues:
        return "Possible Symptoms / Damage Observed", 0.0
    return "Uncertain / Inconclusive", 0.0


def _observed_symptoms(report: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues = report.get("possible_issues") or []
    result: List[Dict[str, Any]] = []
    if issues:
        for issue in issues[:5]:
            likelihood = str(issue.get("likelihood", "low")).lower()
            level, _qualitative_weight = {"low": ("Mild", 1), "moderate": ("Moderate", 2), "high": ("Severe", 3)}.get(likelihood, ("Mild", 1))
            score = 0.0  # not a measured severity percentage
            name = _text(issue.get("name"), "Possible visible issue")
            evidence = _text(issue.get("evidence"), "The model did not describe distinct visual evidence.")
            result.append({
                "name": name,
                "severity": level,
                "percentage": score,
                "observation": f"Possible issue, not confirmed. Visible evidence noted: {evidence} These values are qualitative screening indicators, not measured affected area.",
            })
        return result
    for observation in (report.get("visible_observations") or [])[:4]:
        result.append({
            "name": "Visual observation",
            "severity": "None",
            "percentage": 0.0,
            "observation": str(observation),
        })
    if not result:
        result.append({
            "name": "No specific symptom confidently identified",
            "severity": "Uncertain",
            "percentage": 0.0,
            "observation": "The image did not support a reliable symptom statement. Try a sharp close-up in natural light.",
        })
    return result


def _recommendation_objects(report: Dict[str, Any], fallback: Optional[List[str]] = None) -> List[Dict[str, str]]:
    texts = list(report.get("recommendations") or [])
    if fallback:
        texts += fallback
    unique: List[str] = []
    for item in texts:
        text = _text(item)
        if text and text not in unique:
            unique.append(text)
    return [
        {"title": f"Recommended next step {i + 1}", "description": text, "type": "prevention" if i else "action"}
        for i, text in enumerate(unique[:5])
    ]


def _precautions(report: Dict[str, Any]) -> List[str]:
    values = list(report.get("precautions") or [])
    values.extend(report.get("uncertainty_notes") or [])
    values.extend([
        "Take a clear follow-up photograph and compare the same area over time.",
        "If symptoms spread or crop value is at risk, ask a local KVK/agricultural extension officer to confirm the cause before treatment.",
    ])
    return list(dict.fromkeys(_text(x) for x in values if _text(x)))[:8]


def _care_guide(plant_name: str) -> tuple[Dict[str, str], Optional[Dict[str, Any]]]:
    # Reuse the existing locally bundled botanical care catalogue where it has an entry.
    try:
        from app.services.plant_health_service import PlantHealthByNameService
        _, info = PlantHealthByNameService.find_plant_entry(plant_name)
    except Exception:
        info = None
    if info:
        guide = info.get("care_guide", {})
        return ({
            "watering": _text(guide.get("watering"), "Water according to crop stage and soil moisture; avoid waterlogging."),
            "sunlight": _text(guide.get("sunlight"), "Check crop-specific light needs."),
            "soil": _text(guide.get("soil"), "Use a well-drained soil suited to the crop."),
            "humidity": _text(guide.get("humidity"), "Monitor humidity and airflow."),
            "nutrition": _text(guide.get("nutrition"), "Base fertilizer amounts on soil testing and local recommendations."),
        }, info)
    return ({
        "watering": "Check soil moisture before watering and provide drainage; watering needs differ by species and growth stage.",
        "sunlight": "Compare the plant's light requirements with its current growing environment.",
        "soil": "Use a well-drained growing medium appropriate for the correctly identified species.",
        "humidity": "Maintain airflow and avoid prolonged leaf wetness where fungal disease is a concern.",
        "nutrition": "Use soil-test results and locally recommended crop guidance rather than guessing fertilizer doses.",
    }, None)


def named_plant_report(image_bytes: bytes, user_plant_name: str, crop_type: Optional[str], growing_location: Optional[str]) -> Dict[str, Any]:
    report = OllamaService.analyze_image(
        image_bytes, task="plant", plant_name=user_plant_name, crop_type=crop_type, growing_location=growing_location
    )
    is_botanical_or_produce = report["image_type"] in {"leaf", "flower", "fruit", "vegetable", "whole_plant", "crop", "grain", "seed", "uncertain"}
    if not report["is_agricultural"] or report["image_type"] in {"non_agricultural", "soil"}:
        is_botanical_or_produce = False
    assessment, score = _health_assessment(report)
    care_guide, plant_info = _care_guide(user_plant_name)
    visible = report.get("visible_observations") or []
    issues = report.get("possible_issues") or []
    possible_disease = None
    disease_words = ("disease", "blight", "rust", "mildew", "rot", "scab", "spot", "mold", "mould", "fungal", "bacterial")
    for issue in issues:
        issue_name = _text(issue.get("name"))
        if any(word in issue_name.lower() for word in disease_words):
            possible_disease = f"Possible, unconfirmed: {issue_name}"
            break
    recommendations = _recommendation_objects(report, [
        "Avoid applying a chemical treatment until the suspected cause is confirmed.",
        "If damage is spreading, isolate affected potted plants or keep suspect produce separate while inspecting it.",
    ])
    subject = _text(report.get("subject_name"), "Uncertain botanical subject")
    if plant_info:
        scientific = _text(report.get("scientific_name"), _text(plant_info.get("scientific_name"), "Not confidently identified from the photo"))
        hindi = _text(plant_info.get("hindi_name"))
        category = _text(crop_type, _text(plant_info.get("category"), report["image_type"].replace("_", " ").title()))
        management = list(plant_info.get("default_management", []))[:5]
    else:
        scientific = _text(report.get("scientific_name"), "Not confidently identified from the photo")
        hindi = ""
        category = _text(crop_type, report["image_type"].replace("_", " ").title())
        management = _precautions(report)[:5]

    return {
        "isPlantImage": bool(is_botanical_or_produce),
        "validationStatus": "Photo-based visual screening" if is_botanical_or_produce else "Image category mismatch or uncertain",
        "validationMessage": (
            f"The image model classified the visible subject as '{subject}' ({report['image_type'].replace('_', ' ')}). "
            "This is a visual candidate, not a verified species identification."
            if is_botanical_or_produce else
            "This photo appears to show soil, an unrelated object, or an uncertain subject. Use the matching analysis section or upload a clearer image."
        ),
        "userPlantName": _text(user_plant_name, subject),
        "hindiName": hindi,
        "scientificName": scientific,
        "cropType": category,
        "growingLocation": growing_location or "Not specified",
        "healthAssessment": assessment,
        "healthScorePercentage": score,
        "observedSymptoms": _observed_symptoms(report),
        "hasSymptoms": bool(issues) or report["visible_condition"] in {"possible_stress", "possible_spoilage", "overripe"},
        "diseaseModelAvailable": False,
        "possibleDisease": possible_disease,
        "diseaseConfidence": None,
        "diseaseDiagnosisNotice": "General-purpose local vision model screening only; no dedicated, independently validated disease classifier was used for this result.",
        "careGuide": care_guide,
        "recommendations": recommendations,
        "generalManagementTips": management or _precautions(report)[:5],
        "disclaimer": "The local vision model provides preliminary observations. It cannot confirm a plant pathogen, internal fruit rot, food safety, measured disease severity, or soil chemistry from a photograph. Confirm important decisions with a qualified local agricultural adviser/KVK.",
        "analysisTimestamp": _now(),
        "imageType": report["image_type"],
        "detectedSubject": subject,
        "visibleCondition": report["visible_condition"],
        "ripenessStatus": report["ripeness_status"],
        "spoilageStatus": report["spoilage_status"],
        "visualSummary": report["summary"],
        "visualObservations": visible,
        "possibleIssues": issues,
        "precautions": _precautions(report),
        "analysisSource": "ollama_vision_screening_unvalidated",
    }


def crop_report(image_bytes: bytes) -> Dict[str, Any]:
    report = OllamaService.analyze_image(image_bytes, task="crop")
    if report["image_type"] == "soil":
        return {"_wrong_module": "This image appears to show soil. Open the Soil Analysis module to assess its visible characteristics."}
    if not report["is_agricultural"] or report["image_type"] == "non_agricultural":
        return {"_wrong_module": "This image does not appear to show a crop, plant, fruit, vegetable, flower, grain, or soil. Upload a clear agricultural photograph."}
    issues = report.get("possible_issues") or []
    evidence_text = json.dumps({"observations": report.get("visible_observations", []), "issues": issues}, ensure_ascii=False).lower()
    disease_terms = ("blight", "rust", "mildew", "scab", "fungal", "bacterial", "viral", "disease")
    if not issues and any(term in str(report.get("summary", "")).lower() for term in disease_terms) and not any(term in evidence_text for term in disease_terms):
        subject = _text(report.get("subject_name"), "a crop subject")
        observations = report.get("visible_observations") or []
        report["summary"] = (
            f"The image appears to show {subject}; visible finding: {observations[0]}."
            if observations else f"The image appears to show {subject}; no distinct visible symptom was documented."
        )
    condition = report["visible_condition"]
    ripeness = report["ripeness_status"]
    spoilage = report["spoilage_status"]
    if issues:
        predicted_condition = "Possible issue: " + _text(issues[0].get("name"), "visible symptom")
    elif condition == "possible_spoilage" or spoilage == "possible_visible_spoilage":
        predicted_condition = "Possible visible spoilage — confirm physically"
    elif condition in {"ripe", "unripe", "overripe"}:
        predicted_condition = condition.replace("_", " ").title() + (f" (ripeness: {ripeness.replace('_', ' ')})" if ripeness != "uncertain" else "")
    elif condition == "healthy-looking":
        predicted_condition = "Appears generally healthy in this photo"
    elif condition == "possible_stress":
        predicted_condition = "Possible visible stress or damage"
    else:
        predicted_condition = "Uncertain — image does not support a confident condition label"
    is_healthy = condition in {"healthy-looking", "unripe", "ripe"} and not issues and spoilage != "possible_visible_spoilage"
    recommendations = _recommendation_objects(report, [
        "Take a close-up of the affected area and a second image of the whole plant or produce for context.",
        "Confirm any suspected disease with a local KVK/agricultural extension officer before choosing a treatment.",
    ])
    explanation = _expand_crop_report(report) or _crop_report_from_findings(report)
    return {
        "isAgricultural": True,
        "predictedCrop": _text(report.get("subject_name"), report["image_type"].replace("_", " ").title()),
        "predictedCondition": predicted_condition,
        "isHealthy": is_healthy,
        "healthPercentage": None,
        "damageSeverityPercentage": None,
        "confidence": 0.0,
        "severityLevel": "None" if is_healthy else ("Uncertain" if condition == "uncertain" else "Needs review"),
        "explanation": explanation,
        "recommendations": recommendations,
        "preventionTips": _precautions(report),
        "scientificName": report.get("scientific_name"),
        "modelStatus": "ollama_vision_screening_unvalidated",
        "analysisTimestamp": _now(),
        "imageType": report["image_type"],
        "visibleCondition": report["visible_condition"],
        "ripenessStatus": ripeness,
        "spoilageStatus": spoilage,
        "visibleObservations": report.get("visible_observations", []),
        "possibleIssues": issues,
        "summary": report["summary"],
        "precautions": _precautions(report),
        "analysisProvider": "Local vision analysis",
        "limitationsDisclaimer": "Photo-based screening can describe visible signs, but it cannot confirm a pathogen, internal rot, or disease severity. Verify important crop problems with a local agricultural expert.",
    }


def _soil_catalog_match(hint: str) -> Optional[tuple[str, Dict[str, Any]]]:
    from app.services.soil_inference import SOIL_KNOWLEDGE_BASE
    text = hint.lower()
    tests = [
        ("black", ["black cotton soil", "black soil", "vertisol", "regur"]),
        ("red", ["red soil", "alfisol", "ferruginous"]),
        ("yellow", ["yellow soil"]),
        ("laterite", ["laterite"]),
        ("arid", ["arid", "desert", "sandy soil"]),
        ("saline", ["saline", "alkaline", "usar", "sodic"]),
        ("peat", ["peat", "marsh", "organic muck"]),
        ("mountain", ["mountain", "forest soil", "humus"]),
        ("clay", ["clay loam", "clay soil"]),
        ("sandy loam", ["sandy loam"]),
        ("tarai", ["tarai", "bhabhar", "sub-montane"]),
        ("alluvial", ["alluvial", "riverine", "khadar", "bhangar"]),
    ]
    for _, patterns in tests:
        if any(p in text for p in patterns):
            for key, info in SOIL_KNOWLEDGE_BASE.items():
                haystack = f"{key} {info.get('category', '')}".lower()
                if any(p in haystack for p in patterns):
                    return key, info
    return None


def soil_report(image_bytes: bytes) -> Dict[str, Any]:
    report = OllamaService.analyze_image(image_bytes, task="soil")
    if report["image_type"] not in {"soil", "uncertain"}:
        return {"_wrong_module": "This image looks more like a plant/produce or unrelated object than soil. Open Crop Analysis or upload a soil-surface photo."}
    hint = " ".join([_text(report.get("subject_name")), _text(report.get("summary")), *report.get("visible_observations", [])])
    matched = _soil_catalog_match(hint) if report["image_type"] == "soil" else None
    observations = [
        _text(item) for item in (report.get("visible_observations") or [])
        if _text(item) and not _text(item).lstrip().startswith("{")
        and "image_type" not in _text(item).lower()
        and "one short visible fact" not in _text(item).lower()
    ]
    if not observations:
        observations = ["The model could not confidently describe soil color or texture from this photograph."]
    if matched:
        _, info = matched
        category = _text(info.get("category"), "Visual soil category candidate")
        hindi = _text(info.get("hindi_name"))
        geography = _text(info.get("geography"))
        coverage = _text(info.get("coverage_india"))
        ph_range = _text(info.get("pH_range"), "Not measured") + " (typical reference range only; not measured from this image)"
        suitable = list(info.get("suitable_crops", []))[:12]
        improvements = list(info.get("soil_improvement", []))[:5]
        fertilizers = list(info.get("fertilizer_guidance", []))[:5]
        base_disclaimer = _text(info.get("disclaimer"))
    else:
        category = "Uncertain from photo — soil testing recommended"
        hindi = ""
        geography = ""
        coverage = ""
        ph_range = "Cannot be determined from a photograph"
        suitable = []
        improvements = [
            "Collect representative soil samples from multiple locations and depths according to local extension guidance.",
            "Maintain ground cover and prevent erosion until soil characteristics are measured.",
        ]
        fertilizers = ["Do not calculate lime, gypsum, fertilizer, pH, or NPK applications from visual appearance alone; wait for a soil test."]
        base_disclaimer = "Soil category was not confidently identified. Soil chemistry and crop nutrient requirements require a laboratory test."
    model_observations = observations
    visual_finding = "; ".join(str(item) for item in model_observations[:3] if str(item).strip())
    if not visual_finding or visual_finding.startswith("{") or "image_type" in visual_finding.lower():
        visual_finding = "No distinct soil color or texture features were confidently recorded from this image."
    soil_summary = _text(report.get("summary"), visual_finding)
    if (
        soil_summary.lstrip().startswith("{")
        or "image_type" in soil_summary.lower()
        or "one short visible fact" in soil_summary.lower()
        or any(term in soil_summary.lower() for term in ("healthy-looking", "healthy looking", "spoilage", "plant stress"))
    ):
        soil_summary = visual_finding
    limitations = (soil_summary + " " + base_disclaimer + " A photograph cannot measure pH, available NPK, salinity, organic carbon, or fertilizer requirement. This category is a visual candidate only; use a soil laboratory result for amendments.").strip()
    if matched:
        category_interpretation = (
            f"The visible surface is a broad visual match for {category}. "
            "This is a soil-group candidate based on the photograph, not a confirmed field or laboratory classification."
        )
        next_steps = (
            "Collect a representative composite sample from several spots in the field and request pH, electrical conductivity, "
            "organic carbon, and available NPK tests before choosing amendments or fertilizer."
        )
    else:
        category_interpretation = (
            "The image does not provide enough distinct surface detail for a useful soil-group match. "
            "Soil type and chemistry remain undetermined."
        )
        next_steps = (
            "Retake a close soil-surface photo in daylight, then collect a representative composite sample and use a soil-test result "
            "for crop and amendment decisions."
        )
    return {
        "isAgricultural": True,
        "predictedSoilCategory": category,
        "hindiName": hindi,
        "geography": geography,
        "coverageIndia": coverage,
        "pHRange": ph_range,
        "confidence": 0.0,
        "visualObservations": model_observations[:8],
        "suitableCrops": suitable,
        "soilImprovementGuidance": improvements,
        "fertilizerGuidance": fertilizers,
        "limitationsDisclaimer": limitations,
        "modelStatus": "ollama_vision_screening_unvalidated" if matched else "ollama_vision_uncertain",
        "analysisTimestamp": _now(),
        "summary": soil_summary,
        "analysisProvider": "Local vision analysis",
        "report": {
            "visualFinding": visual_finding,
            "categoryInterpretation": category_interpretation,
            "nextSteps": next_steps,
        },
    }


def identification_report(image_bytes: bytes, user_plant_name: Optional[str] = None, organ: Optional[str] = None, db: Any = None) -> Dict[str, Any]:
    report = OllamaService.analyze_image(image_bytes, task="identify", plant_name=user_plant_name)
    image_type = report["image_type"]
    if image_type == "soil":
        return {"_wrong_module": "This image appears to show soil. Use the Soil Analysis module."}
    if not report["is_agricultural"] or image_type == "non_agricultural":
        return {"_wrong_module": "The image does not appear to show a recognizable plant or produce. Upload a clear photo in natural light."}
    expected_organ = (organ or "leaf").strip().lower().replace(" ", "_")
    compatible_image_types = {
        "leaf": {"leaf", "whole_plant", "crop"},
        "flower": {"flower"},
        "fruit": {"fruit"},
        "stem": {"whole_plant", "crop"},
        "root": {"whole_plant", "crop"},
        "whole_plant": {"whole_plant", "crop"},
    }
    organ_mismatch = (
        expected_organ in compatible_image_types
        and image_type != "uncertain"
        and image_type not in compatible_image_types[expected_organ]
    )
    expected_label = expected_organ.replace("_", " ").title()
    detected_label = image_type.replace("_", " ").title()
    mismatch_message = (
        f"You selected {expected_label}, but this photo appears to show {detected_label}. "
        f"This result describes the {detected_label.lower()}; upload a {expected_label.lower()} photo for {expected_label.lower()} analysis."
        if organ_mismatch else None
    )
    subject = _text(report.get("subject_name"), "Uncertain botanical subject")
    candidate = {
        "rank": 1,
        "plantId": None,
        "id": None,
        "scientificName": _text(report.get("scientific_name"), "Not confidently identified"),
        "commonName": subject,
        "hindiName": "",
        "teluguName": "",
        "tamilName": "",
        "family": "",
        "category": image_type.replace("_", " ").title(),
        "confidence": 0.0,
        "confidencePercentage": 0.0,
    }
    catalog_matches = []
    if db is not None and subject and subject.lower() not in {"unknown", "uncertain subject", "uncertain botanical subject"}:
        try:
            from app.services.plant_identifier_service import PlantIdentifierService
            match_data = PlantIdentifierService.search_plants(query=subject, page=1, limit=3, db=db)
            catalog_matches = match_data.get("items", [])
            if catalog_matches:
                first = catalog_matches[0]
                candidate.update({
                    "plantId": first.get("id"), "id": first.get("id"),
                    "commonName": first.get("commonName", subject),
                    "scientificName": _text(report.get("scientific_name"), first.get("scientificName", "Not confidently identified")),
                    "hindiName": first.get("hindiName", ""), "teluguName": first.get("teluguName", ""),
                    "tamilName": first.get("tamilName", ""), "family": first.get("family", ""),
                    "category": first.get("category", candidate["category"]),
                })
        except Exception:
            catalog_matches = []
    assessment, score = _health_assessment(report)
    features = list(report.get("visible_observations") or [])
    features.extend([f"Possible issue (unconfirmed): {i['name']} — {i['evidence']}" for i in report.get("possible_issues", []) if i.get("name")])
    if not features:
        features = ["The model did not identify distinct visual features confidently."]
    return {
        "success": True,
        "mode": "ollama_vision_screening",
        "isAgricultural": True,
        "detectedOrgan": image_type,
        "organAnalysis": {
            "organ": image_type, "confidence": 0.0,
            "evidence": "; ".join(features[:3]) if features else "No distinct visual evidence could be extracted confidently.",
            "imageType": image_type, "condition": report["visible_condition"],
            "ripeness": report["ripeness_status"], "spoilage": report["spoilage_status"]
        },
        "organHonestyNotice": "Image results are preliminary visual estimates. Check the detected plant part and subject against the uploaded photo.",
        "isAmbiguous": organ_mismatch or image_type == "uncertain" or "uncertain" in subject.lower() or not report.get("scientific_name"),
        "ambiguityMessage": mismatch_message or ("Only a broad visual candidate is available; compare it with botanical references or provide a clearer close-up." if image_type == "uncertain" or "uncertain" in subject.lower() or not report.get("scientific_name") else None),
        "inDistribution": None,
        "directorySearchQuery": subject,
        "topCandidate": candidate,
        "candidates": [candidate],
        "normalizedEntropy": None,
        "savedToAccount": False,
        "persistenceMessage": None,
        "visualEvidence": features[:8],
        "nameAssistedAnalysis": {
            "status": "Not independently verified", "isConsistent": None,
            "explanation": "The supplied name was treated only as a hint. This general-purpose vision model cannot independently confirm or refute species identity."
        } if user_plant_name else None,
        "targetedPlant": catalog_matches[0] if catalog_matches else None,
        "analysisTimestamp": _now(),
        "healthAssessment": {
            "healthStatus": assessment, "healthScorePercentage": 0.0,
            "chlorosisPercentage": 0.0, "necrosisPercentage": 0.0, "mildewPercentage": 0.0,
            "symptoms": features[:6] or ["Visual screening only; no specific symptom could be established confidently."],
            "summary": report["summary"]
        },
        "recommendations": _recommendation_objects(report),
        "visualCondition": report["visible_condition"],
        "ripenessStatus": report["ripeness_status"],
        "spoilageStatus": report["spoilage_status"],
        "visualSummary": report["summary"],
        "possibleIssues": report.get("possible_issues", []),
        "precautions": _precautions(report),
        "analysisSource": "ollama_vision_screening_unvalidated",
    }


def health_report(image_bytes: bytes, plant_id: Optional[str], plant_name: Optional[str], db: Any = None) -> Dict[str, Any]:
    report = OllamaService.analyze_image(image_bytes, task="health", plant_name=plant_name)
    named = named_plant_report_from_normalized(report, plant_name or _text(report.get("subject_name"), "Unknown plant"))
    return {
        "success": bool(named["isPlantImage"]),
        "plantName": named["detectedSubject"],
        "healthStatus": named["healthAssessment"],
        "healthScorePercentage": named["healthScorePercentage"],
        "observedSymptoms": [
            {"symptom": s["name"], "severityPercentage": s["percentage"], "severityLevel": s["severity"], "description": s["observation"]}
            for s in named["observedSymptoms"]
        ],
        "diseaseModelAvailable": False,
        "diseaseDiagnosis": ({"candidate": named["possibleDisease"], "confirmed": False, "analysisSource": named["analysisSource"]} if named.get("possibleDisease") else None),
        "diagnosisNotice": named["diseaseDiagnosisNotice"],
        "recommendations": named["recommendations"],
        "disclaimer": named["disclaimer"],
        "analysisTimestamp": named["analysisTimestamp"],
        "imageType": named["imageType"],
        "visibleCondition": named["visibleCondition"],
        "ripenessStatus": named["ripenessStatus"],
        "spoilageStatus": named["spoilageStatus"],
        "visualSummary": named["visualSummary"],
        "possibleIssues": named["possibleIssues"],
        "precautions": named["precautions"],
        "analysisSource": named["analysisSource"],
    }


def named_plant_report_from_normalized(report: Dict[str, Any], user_plant_name: str) -> Dict[str, Any]:
    """Map an already normalized image report without making a second model call."""
    # Reuse the normal mapper's response contract, but do not call Ollama a second time.
    from app.services.plant_health_service import PlantHealthByNameService
    is_botanical = report["image_type"] in {"leaf", "flower", "fruit", "vegetable", "whole_plant", "crop", "grain", "seed"} and report["is_agricultural"]
    assessment, score = _health_assessment(report)
    guide, info = _care_guide(user_plant_name)
    issues = report.get("possible_issues") or []
    possible_disease = next((f"Possible, unconfirmed: {_text(i.get('name'))}" for i in issues if any(t in _text(i.get("name")).lower() for t in ("disease", "blight", "rust", "mildew", "rot", "scab", "spot", "fungal", "bacterial"))), None)
    subject = _text(report.get("subject_name"), "Uncertain botanical subject")
    return {
        "isPlantImage": is_botanical,
        "validationStatus": "Ollama visual screening" if is_botanical else "Image category mismatch or uncertain",
        "validationMessage": f"Visual candidate: {subject}. Species identity and health status are not confirmed.",
        "userPlantName": user_plant_name,
        "hindiName": _text(info.get("hindi_name")) if info else "",
        "scientificName": _text(report.get("scientific_name"), _text(info.get("scientific_name"), "Not confidently identified")) if info else _text(report.get("scientific_name"), "Not confidently identified"),
        "cropType": _text(info.get("category"), report["image_type"].replace("_", " ").title()) if info else report["image_type"].replace("_", " ").title(),
        "growingLocation": "Not specified",
        "healthAssessment": assessment,
        "healthScorePercentage": score,
        "observedSymptoms": _observed_symptoms(report),
        "hasSymptoms": bool(issues) or report["visible_condition"] in {"possible_stress", "possible_spoilage", "overripe"},
        "diseaseModelAvailable": False,
        "possibleDisease": possible_disease,
        "diseaseConfidence": None,
        "diseaseDiagnosisNotice": "General-purpose local vision model screening only; no dedicated, independently validated disease classifier was used for this result.",
        "careGuide": guide,
        "recommendations": _recommendation_objects(report),
        "generalManagementTips": _precautions(report)[:5],
        "disclaimer": "The local vision model provides preliminary observations only. It cannot confirm pathogen identity, internal fruit rot, food safety, measured disease severity, or soil chemistry from a photo. Consult a qualified local agricultural adviser/KVK for important decisions.",
        "analysisTimestamp": _now(),
        "imageType": report["image_type"],
        "detectedSubject": subject,
        "visibleCondition": report["visible_condition"],
        "ripenessStatus": report["ripeness_status"],
        "spoilageStatus": report["spoilage_status"],
        "visualSummary": report["summary"],
        "visualObservations": report.get("visible_observations", []),
        "possibleIssues": issues,
        "precautions": _precautions(report),
        "analysisSource": "ollama_vision_screening_unvalidated",
    }
