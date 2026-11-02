import json
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy import Column, String, Boolean, Text, DateTime, Index
from app.database import Base

class PlantSpecies(Base):
    __tablename__ = "plant_species"

    id = Column(String(100), primary_key=True, index=True)
    scientific_name = Column(String(150), nullable=False, unique=True, index=True)
    common_name = Column(String(150), nullable=False, index=True)
    hindi_name = Column(String(150), nullable=True, index=True)
    telugu_name = Column(String(150), nullable=True, index=True)
    tamil_name = Column(String(150), nullable=True, index=True)
    other_regional_names_json = Column(Text, nullable=True)  # JSON dict {kannada, marathi, etc.}
    synonyms_json = Column(Text, nullable=True)  # JSON list of synonyms
    family = Column(String(100), nullable=False, index=True)
    genus = Column(String(100), nullable=False, index=True)
    species = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False, index=True)  # crop, fruit plant, vegetable, etc.
    status_in_india = Column(String(50), nullable=False, default="native")  # native, naturalized, cultivated
    indian_states_json = Column(Text, nullable=True)  # JSON list of states
    
    # Identification characteristics
    leaf_characteristics_json = Column(Text, nullable=True)  # JSON dict
    stem_characteristics = Column(Text, nullable=True)
    flower_characteristics = Column(Text, nullable=True)
    fruit_characteristics = Column(Text, nullable=True)
    growth_habit = Column(Text, nullable=True)
    
    # Growing & Care
    habitat_and_climate = Column(Text, nullable=True)
    sunlight_requirements = Column(String(150), nullable=True)
    water_requirements = Column(String(150), nullable=True)
    soil_preferences = Column(String(150), nullable=True)
    growing_season = Column(String(150), nullable=True)
    propagation_methods_json = Column(Text, nullable=True)  # JSON list
    
    # Uses, Safety, Pests & Diseases
    uses_json = Column(Text, nullable=True)  # JSON list
    safety_notes = Column(Text, nullable=True)
    is_toxic = Column(Boolean, default=False)
    common_pests_and_diseases_json = Column(Text, nullable=True)  # JSON list of objects
    prevention_guidance_json = Column(Text, nullable=True)  # JSON list of strings
    
    # Media & Provenance
    image_references_json = Column(Text, nullable=True)  # JSON list of image objects
    sources_json = Column(Text, nullable=True)  # JSON list of source objects
    verification_status = Column(String(50), nullable=False, default="verified")
    last_checked_date = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes plant entity to dictionary with parsed JSON fields."""
        return {
            "id": self.id,
            "scientificName": self.scientific_name,
            "commonName": self.common_name,
            "hindiName": self.hindi_name or "",
            "teluguName": self.telugu_name or "",
            "tamilName": self.tamil_name or "",
            "otherRegionalNames": json.loads(self.other_regional_names_json) if self.other_regional_names_json else {},
            "synonyms": json.loads(self.synonyms_json) if self.synonyms_json else [],
            "family": self.family,
            "genus": self.genus,
            "species": self.species,
            "category": self.category,
            "statusInIndia": self.status_in_india,
            "indianStates": json.loads(self.indian_states_json) if self.indian_states_json else [],
            "leafCharacteristics": json.loads(self.leaf_characteristics_json) if self.leaf_characteristics_json else {},
            "stemCharacteristics": self.stem_characteristics or "",
            "flowerCharacteristics": self.flower_characteristics or "",
            "fruitCharacteristics": self.fruit_characteristics or "",
            "growthHabit": self.growth_habit or "",
            "habitatAndClimate": self.habitat_and_climate or "",
            "sunlightRequirements": self.sunlight_requirements or "",
            "waterRequirements": self.water_requirements or "",
            "soilPreferences": self.soil_preferences or "",
            "growingSeason": self.growing_season or "",
            "propagationMethods": json.loads(self.propagation_methods_json) if self.propagation_methods_json else [],
            "uses": json.loads(self.uses_json) if self.uses_json else [],
            "safetyNotes": self.safety_notes or "",
            "isToxic": bool(self.is_toxic),
            "commonPestsAndDiseases": json.loads(self.common_pests_and_diseases_json) if self.common_pests_and_diseases_json else [],
            "preventionGuidance": json.loads(self.prevention_guidance_json) if self.prevention_guidance_json else [],
            "imageReferences": json.loads(self.image_references_json) if self.image_references_json else [],
            "sources": json.loads(self.sources_json) if self.sources_json else [],
            "verificationStatus": self.verification_status,
            "lastCheckedDate": self.last_checked_date or "",
        }

    def to_summary_dict(self) -> Dict[str, Any]:
        """Compact representation for list views and autocomplete."""
        return {
            "id": self.id,
            "scientificName": self.scientific_name,
            "commonName": self.common_name,
            "hindiName": self.hindi_name or "",
            "teluguName": self.telugu_name or "",
            "tamilName": self.tamil_name or "",
            "family": self.family,
            "category": self.category,
            "statusInIndia": self.status_in_india,
            "soilPreferences": self.soil_preferences or "",
            "verificationStatus": self.verification_status,
        }
