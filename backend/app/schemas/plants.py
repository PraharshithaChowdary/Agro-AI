from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PlantSummaryOut(BaseModel):
    id: str
    scientificName: str
    commonName: str
    hindiName: Optional[str] = ""
    teluguName: Optional[str] = ""
    tamilName: Optional[str] = ""
    family: str
    category: str
    statusInIndia: str
    soilPreferences: Optional[str] = ""
    verificationStatus: str

class PlantSearchResponse(BaseModel):
    total: int
    page: int
    limit: int
    totalPages: int
    items: List[PlantSummaryOut]

class PlantCategoryCount(BaseModel):
    category: str
    count: int

class PlantCandidateOut(BaseModel):
    rank: int
    plantId: Optional[str] = None
    id: Optional[str] = None
    scientificName: Optional[str] = None
    commonName: Optional[str] = None
    hindiName: Optional[str] = ""
    teluguName: Optional[str] = ""
    tamilName: Optional[str] = ""
    family: Optional[str] = ""
    category: Optional[str] = ""
    confidence: float
    confidencePercentage: float

class PlantAutocompleteItem(BaseModel):
    id: str
    scientificName: str
    commonName: str
    hindiName: Optional[str] = ""
    teluguName: Optional[str] = ""
    tamilName: Optional[str] = ""
    category: str
    family: str
    highlight: str
    matchSource: str
    statusInIndia: Optional[str] = "native"

class PlantIdentificationOut(BaseModel):
    success: bool
    mode: str
    isAgricultural: bool
    detectedOrgan: str
    organAnalysis: Optional[Dict[str, Any]] = None
    organHonestyNotice: Optional[str] = None
    isAmbiguous: bool
    ambiguityMessage: Optional[str] = None
    inDistribution: Optional[bool] = True
    directorySearchQuery: Optional[str] = None
    topCandidate: Optional[Dict[str, Any]] = None
    candidates: List[Dict[str, Any]]
    normalizedEntropy: Optional[float] = None
    savedToAccount: bool = False
    persistenceMessage: Optional[str] = None
    visualEvidence: List[str]
    nameAssistedAnalysis: Optional[Dict[str, Any]] = None
    targetedPlant: Optional[Dict[str, Any]] = None
    analysisTimestamp: str
    healthAssessment: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    visualCondition: Optional[str] = None
    ripenessStatus: Optional[str] = None
    spoilageStatus: Optional[str] = None
    visualSummary: Optional[str] = None
    possibleIssues: List[Dict[str, Any]] = Field(default_factory=list)
    precautions: List[str] = Field(default_factory=list)
    analysisSource: Optional[str] = None

class HealthSymptomOut(BaseModel):
    symptom: str
    severityPercentage: float
    severityLevel: str
    description: str

class RecommendationOut(BaseModel):
    title: str
    description: str
    type: str

class PlantHealthAnalysisOut(BaseModel):
    success: bool
    plantName: str
    healthStatus: str
    healthScorePercentage: float
    observedSymptoms: List[HealthSymptomOut]
    diseaseModelAvailable: bool
    diseaseDiagnosis: Optional[Dict[str, Any]] = None
    diagnosisNotice: str
    recommendations: List[RecommendationOut]
    disclaimer: str
    analysisTimestamp: str
    savedToAccount: bool = False
    persistenceMessage: Optional[str] = None
    error: Optional[str] = None
    imageType: Optional[str] = None
    detectedSubject: Optional[str] = None
    visualCondition: Optional[str] = None
    ripenessStatus: Optional[str] = None
    spoilageStatus: Optional[str] = None
    visualSummary: Optional[str] = None
    visualObservations: List[str] = Field(default_factory=list)
    possibleIssues: List[Dict[str, Any]] = Field(default_factory=list)
    precautions: List[str] = Field(default_factory=list)
    analysisSource: Optional[str] = None
