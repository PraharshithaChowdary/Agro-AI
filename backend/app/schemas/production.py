from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class RecommendationSchema(BaseModel):
    title: str
    description: str
    type: str  # 'action' | 'organic' | 'chemical' | 'prevention' | 'info'

class CropAnalysisOut(BaseModel):
    isAgricultural: bool
    predictedCrop: str
    predictedCondition: str
    isHealthy: bool
    healthPercentage: Optional[float] = 95.0
    damageSeverityPercentage: Optional[float] = 5.0
    confidence: float
    severityLevel: Optional[str] = "None"
    explanation: str
    recommendations: List[RecommendationSchema]
    preventionTips: List[str]
    scientificName: Optional[str] = None
    modelStatus: str
    analysisTimestamp: str
    imageUrl: Optional[str] = None
    savedToAccount: bool = False
    persistenceMessage: Optional[str] = None
    imageType: Optional[str] = None
    visibleCondition: Optional[str] = None
    ripenessStatus: Optional[str] = None
    spoilageStatus: Optional[str] = None
    visibleObservations: List[str] = Field(default_factory=list)
    possibleIssues: List[dict] = Field(default_factory=list)
    summary: Optional[str] = None
    precautions: List[str] = Field(default_factory=list)
    analysisProvider: Optional[str] = None
    limitationsDisclaimer: Optional[str] = None

class SoilAnalysisOut(BaseModel):
    isAgricultural: bool
    predictedSoilCategory: str
    hindiName: Optional[str] = None
    geography: Optional[str] = None
    coverageIndia: Optional[str] = None
    pHRange: Optional[str] = None
    confidence: float
    visualObservations: List[str]
    suitableCrops: List[str]
    soilImprovementGuidance: List[str]
    fertilizerGuidance: List[str]
    limitationsDisclaimer: str
    modelStatus: str
    analysisTimestamp: str
    imageUrl: Optional[str] = None
    savedToAccount: bool = False
    persistenceMessage: Optional[str] = None
    summary: Optional[str] = None
    analysisProvider: Optional[str] = None
    report: Optional[Dict[str, str]] = None

class RelevanceCheckOut(BaseModel):
    isAgricultural: bool
    relevanceType: str  # 'agriculture' | 'non_agriculture' | 'uncertain'
    detectedModality: Optional[str] = "unknown"
    confidence: float
    message: str
    reason: Optional[str] = None

class ObservedSymptomSchema(BaseModel):
    name: str
    severity: str  # 'None' | 'Mild' | 'Moderate' | 'Severe'
    percentage: float
    observation: str

class PlantCareGuideSchema(BaseModel):
    watering: str
    sunlight: str
    soil: str
    humidity: Optional[str] = None
    nutrition: str

class NamedPlantAnalysisOut(BaseModel):
    isPlantImage: bool
    validationStatus: str
    validationMessage: str
    userPlantName: str
    hindiName: Optional[str] = None
    scientificName: Optional[str] = None
    cropType: Optional[str] = None
    growingLocation: Optional[str] = None
    healthAssessment: str  # 'Healthy-looking' | 'Possible Symptoms / Damage Observed' | 'Uncertain / Inconclusive'
    healthScorePercentage: float
    observedSymptoms: List[ObservedSymptomSchema]
    hasSymptoms: bool
    diseaseModelAvailable: bool
    possibleDisease: Optional[str] = None
    diseaseConfidence: Optional[float] = None
    diseaseDiagnosisNotice: str
    careGuide: PlantCareGuideSchema
    recommendations: List[RecommendationSchema]
    generalManagementTips: List[str]
    disclaimer: str
    analysisTimestamp: str
    imageUrl: Optional[str] = None
    savedToAccount: bool = False
    persistenceMessage: Optional[str] = None
    imageType: Optional[str] = None
    detectedSubject: Optional[str] = None
    visibleCondition: Optional[str] = None
    ripenessStatus: Optional[str] = None
    spoilageStatus: Optional[str] = None
    visualSummary: Optional[str] = None
    visualObservations: List[str] = Field(default_factory=list)
    possibleIssues: List[dict] = Field(default_factory=list)
    precautions: List[str] = Field(default_factory=list)
    analysisSource: Optional[str] = None

class SupportedPlantItem(BaseModel):
    id: str
    name: str
    hindiName: Optional[str] = None
    scientificName: str
    category: str
    indianSeason: Optional[str] = None
    majorStates: Optional[str] = None
    diseaseModelAvailable: bool
    supportedDiseasesCount: int

class IndianSoilItem(BaseModel):
    soilType: str
    category: str
    hindiName: Optional[str] = None
    geography: Optional[str] = None
    coverageIndia: Optional[str] = None
    pHRange: Optional[str] = None
    suitableCrops: List[str]
    visualObservations: List[str]
    soilImprovement: List[str]
    fertilizerGuidance: List[str]

