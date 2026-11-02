export type UserRole = 'farmer' | 'buyer' | 'general' | 'admin';

export interface User {
  id: string;
  fullName: string;
  email: string;
  role: UserRole;
  createdAt?: string;
}

export interface AuthResponse {
  token: string;
  user: User;
  message?: string;
}

// ----------------- Better Production Types -----------------

export type ImageRelevanceType = 'agriculture' | 'non_agriculture' | 'uncertain';

export interface RelevanceCheckResult {
  isAgricultural: boolean;
  relevanceType: ImageRelevanceType;
  confidence: number;
  message: string;
  reason?: string;
}

export interface Recommendation {
  title: string;
  description: string;
  type: 'action' | 'organic' | 'chemical' | 'prevention' | 'info';
}

export interface CropAnalysisResult {
  savedToAccount?: boolean;
  persistenceMessage?: string;
  isAgricultural: boolean;
  predictedCrop: string;
  predictedCondition: string; // 'Healthy' or specific disease
  isHealthy: boolean;
  healthPercentage?: number; // e.g. 96.0
  damageSeverityPercentage?: number; // e.g. 4.0
  confidence: number; // e.g. 0.94
  severityLevel?: 'None' | 'Low' | 'Moderate' | 'Severe' | string;
  explanation: string;
  recommendations: Recommendation[];
  preventionTips: string[];
  scientificName?: string;
  modelStatus: 'trained_model' | 'fallback_inference' | 'model_unavailable' | string;
  analysisTimestamp: string;
  imageUrl?: string;
  imageType?: string;
  visibleCondition?: string;
  ripenessStatus?: string;
  spoilageStatus?: string;
  visibleObservations?: string[];
  possibleIssues?: Array<{ name?: string; evidence?: string; likelihood?: string }>;
  summary?: string;
  precautions?: string[];
  analysisProvider?: string;
  limitationsDisclaimer?: string;
}

export interface SoilAnalysisResult {
  savedToAccount?: boolean;
  persistenceMessage?: string;
  isAgricultural: boolean;
  predictedSoilCategory: string; // e.g. 'Alluvial Soil', 'Black Soil', 'Clay Soil', 'Red Soil', 'Sandy Soil'
  confidence: number;
  visualObservations: string[];
  suitableCrops: string[];
  soilImprovementGuidance: string[];
  fertilizerGuidance: string[];
  limitationsDisclaimer: string;
  modelStatus: 'trained_model' | 'fallback_inference' | 'model_unavailable' | 'ollama_vision_screening_unvalidated' | 'ollama_vision_uncertain';
  analysisTimestamp: string;
  imageUrl?: string;
  summary?: string;
  analysisProvider?: string;
  pHRange?: string;
  geography?: string;
  coverageIndia?: string;
  hindiName?: string;
  report?: {
    visualFinding: string;
    categoryInterpretation: string;
    nextSteps: string;
  };
}

export interface ProductionHistoryItem {
  id: string;
  type: 'crop' | 'soil' | 'named_plant';
  predictedClass: string;
  confidence: number;
  date: string;
  imageUrl?: string;
  status: 'valid' | 'invalid_image' | 'uncertain';
}

export interface ObservedSymptom {
  name: string;
  severity: 'None' | 'Mild' | 'Moderate' | 'Severe' | string;
  percentage: number;
  observation: string;
}

export interface PlantCareGuide {
  watering: string;
  sunlight: string;
  soil: string;
  humidity?: string;
  nutrition: string;
}

export interface NamedPlantAnalysisResult {
  savedToAccount?: boolean;
  persistenceMessage?: string;
  isPlantImage: boolean;
  validationStatus: string;
  validationMessage: string;
  userPlantName: string;
  scientificName?: string;
  cropType?: string;
  growingLocation?: string;
  healthAssessment: 'Healthy-looking' | 'Possible Symptoms / Damage Observed' | 'Uncertain / Inconclusive' | string;
  healthScorePercentage: number;
  observedSymptoms: ObservedSymptom[];
  hasSymptoms: boolean;
  diseaseModelAvailable: boolean;
  possibleDisease?: string | null;
  diseaseConfidence?: number | null;
  diseaseDiagnosisNotice: string;
  careGuide: PlantCareGuide;
  recommendations: Recommendation[];
  generalManagementTips: string[];
  disclaimer: string;
  analysisTimestamp: string;
  imageUrl?: string;
  hindiName?: string;
  imageType?: string;
  detectedSubject?: string;
  visibleCondition?: string;
  ripenessStatus?: string;
  spoilageStatus?: string;
  visualSummary?: string;
  visualObservations?: string[];
  possibleIssues?: Array<{ name?: string; evidence?: string; likelihood?: string }>;
  precautions?: string[];
  analysisSource?: string;
}

export interface SupportedPlantItem {
  id: string;
  name: string;
  scientificName: string;
  category: string;
  diseaseModelAvailable: boolean;
  supportedDiseasesCount: number;
}


// ----------------- Better Nutrition Types -----------------

export type Gender = 'male' | 'female';
export type ActivityLevel = 'sedentary' | 'light' | 'moderate' | 'active' | 'very_active';
export type NutritionGoal = 'weight_loss' | 'maintenance' | 'weight_gain' | 'healthy_eating';
export type FoodPreference = 'vegetarian' | 'non_vegetarian' | 'vegan' | 'eggetarian' | 'pescatarian' | 'jain';
export type CuisineType = 'indian' | 'south_indian' | 'andhra' | 'tamil' | 'north_indian' | 'continental' | 'mediterranean' | 'asian' | 'general';

export interface NutritionProfileInput {
  age: number;
  gender: Gender;
  heightCm: number;
  weightKg: number;
  goalWeightKg?: number;
  activityLevel: ActivityLevel;
  goal: NutritionGoal;
  foodPreference: FoodPreference;
  mealsPerDay?: number;
  targetTimelineWeeks?: number;
  allergies: string[];
  customAllergies?: string;
  intolerances?: string[];
  dislikedFoods?: string;
  dietaryRestrictions: string[];
  preferredCuisine: CuisineType;
  budgetTier?: 'budget_friendly' | 'moderate' | 'premium';
  cookingTimePref?: 'quick_easy' | 'moderate' | 'elaborate';
  variationSeed?: number;
  generateNewWeek?: boolean;
  weekNumber?: number;
  weekStartDate?: string;
}

export interface NutritionCalculationResult {
  bmi: number;
  bmiCategory: 'Underweight' | 'Normal weight' | 'Overweight' | 'Obesity' | string;
  bmr: number;
  tdee: number;
  goalAdjustmentCalories?: number;
  goal?: string;
  targetCalories: number;
  targetProteinGrams: number;
  targetCarbsGrams: number;
  targetFatGrams: number;
  targetFibreGrams?: number;
  mealsPerDay?: number;
  mealCalorieTargets?: Record<string, number>;
  formulaUsed: string;
  safetyWarnings?: string[];
  incompatibleNotices?: string[];
  disclaimer: string;
}

export interface Ingredient {
  name: string;
  quantityGrams: number;
  measure: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fibre?: number;
  allergens: string[];
}

export interface FoodItem {
  dishId?: string;
  name: string;
  portion: string;
  calories: number;
  proteinGrams: number;
  carbsGrams: number;
  fatGrams: number;
  fibreGrams?: number;
  category: string;
  isVegetarian: boolean;
  isVegan?: boolean;
  allergens: string[];
  ingredients?: Ingredient[];
  preparationInstructions?: string;
  goalFitReason?: string;
  cuisine?: string;
}

export interface Meal {
  mealType: string;
  timeSuggestion: string;
  items: FoodItem[];
  totalCalories: number;
  totalProtein: number;
  totalCarbs?: number;
  totalFat?: number;
  totalFibre?: number;
}

export interface DailyDietPlan {
  dayNumber: number;
  dayName: string;
  meals: Meal[];
  dailyTargetCalories?: number;
  dailyTotalCalories: number;
  calorieDifference?: number;
  calorieDifferencePercent?: number;
  isWithinTolerance?: boolean;
  dailyTotalProtein: number;
  dailyTotalCarbs: number;
  dailyTotalFat: number;
  dailyTotalFibre?: number;
  hydrationTip: string;
  macroReconciliation?: {
    proteinCalories: number;
    carbsCalories: number;
    fatCalories: number;
    macroSumCalories: number;
    atwaterCalculatedKcal?: number;
    formula?: string;
    note?: string;
    differenceFromTotal?: number;
    reconciliationNotes?: string;
  };
}

export interface FoodRecommendationItem {
  group: string;
  items: string[];
  rationale: string;
}

export interface FoodAvoidanceItem {
  item: string;
  reason: string;
  category: string;
}

export interface FoodSubstitutionItem {
  original: string;
  substitute: string;
  benefit: string;
}

export interface NutritionalGuidance {
  foodsToEat: FoodRecommendationItem[];
  foodsToAvoid: FoodAvoidanceItem[];
  foodsToLimit: FoodRecommendationItem[];
  safeSubstitutions: FoodSubstitutionItem[];
  timingAndPortionTips: string[];
}

export interface WeeklyDietPlanResponse {
  savedToAccount?: boolean;
  persistenceMessage?: string;
  id?: string;
  weekNumber?: number;
  weekStartDate?: string;
  selectedDishIds?: string[];
  profileSummary: {
    age?: number;
    gender?: Gender;
    heightCm?: number;
    weightKg?: number;
    goalWeightKg?: number;
    activityLevel?: ActivityLevel;
    bmi: number;
    bmiCategory: string;
    bmr?: number;
    tdee?: number;
    goalAdjustmentCalories?: number;
    targetCalories: number;
    targetProtein: number;
    targetCarbs?: number;
    targetFat?: number;
    targetFibre?: number;
    goal: NutritionGoal;
    foodPreference: FoodPreference;
    mealsPerDay?: number;
    allergies: string[];
    customAllergies?: string;
    intolerances?: string[];
    dislikedFoods?: string;
    dietaryRestrictions?: string[];
    preferredCuisine?: CuisineType;
    budgetTier?: 'budget_friendly' | 'moderate' | 'premium';
    cookingTimePref?: 'quick_easy' | 'moderate' | 'elaborate';
  };
  variationSeed?: number;
  days: DailyDietPlan[];
  guidance?: NutritionalGuidance;
  generatedAt: string;
  nutritionalNotes: string[];
  safetyWarnings?: string[];
  disclaimer: string;
}

export interface SavedWeeklyPlanSummary {
  id: string;
  weekNumber: number;
  weekStartDate?: string;
  targetCalories?: number;
  totalCaloriesAvg?: number;
  totalProteinAvg?: number;
  createdAt: string;
}

// ----------------- Assistant Types -----------------

export interface EvidenceSource {
  title: string;
  organization: string;
  year: string;
  url: string;
  category?: string;
}

export interface AssistantEngineStatus {
  provider: string;
  model: string;
  is_live_llm: boolean;
  mode: string;
  badge: string;
}

export interface SessionSummary {
  sessionId: string;
  lastMessage: string;
  messageCount: number;
  updatedAt: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  savedToAccount?: boolean;
  persistenceMessage?: string;
  category?: 'crop_care' | 'soil' | 'disease' | 'nutrition' | 'irrigation' | 'economics' | 'general' | 'clarification';
  evidenceSources?: EvidenceSource[];
  suggestedQuestions?: string[];
  calculatorData?: any;
  modelProvider?: string;
  relatedAction?: {
    label: string;
    route: string;
  };
}

// ----------------- Indian Plant Explorer & Health Analyzer Types -----------------

export interface PlantSummaryItem {
  id: string;
  plantId?: string;
  scientificName: string;
  commonName: string;
  hindiName?: string;
  teluguName?: string;
  tamilName?: string;
  family: string;
  category: string;
  statusInIndia: string;
  soilPreferences?: string;
  verificationStatus: string;
  rank?: number;
  confidence?: number;
  confidencePercentage?: number;
  leafCharacteristics?: Record<string, string>;
}

export interface PlantSpeciesRecord {
  id: string;
  scientificName: string;
  commonName: string;
  hindiName?: string;
  teluguName?: string;
  tamilName?: string;
  otherRegionalNames: Record<string, string>;
  synonyms: string[];
  family: string;
  genus: string;
  species: string;
  category: string;
  statusInIndia: string;
  indianStates: string[];
  leafCharacteristics: {
    shape?: string;
    arrangement?: string;
    margin?: string;
    venation?: string;
    color?: string;
  };
  stemCharacteristics: string;
  flowerCharacteristics: string;
  fruitCharacteristics: string;
  growthHabit: string;
  habitatAndClimate: string;
  sunlightRequirements: string;
  waterRequirements: string;
  soilPreferences: string;
  growingSeason: string;
  propagationMethods: string[];
  uses: string[];
  safetyNotes: string;
  isToxic: boolean;
  commonPestsAndDiseases: Array<{
    name: string;
    type?: string;
    symptoms?: string;
    management?: string;
  }>;
  preventionGuidance: string[];
  imageReferences: Array<{
    imageUrl?: string;
    localPath?: string;
    organ?: string;
    license?: string;
    author?: string;
  }>;
  sources: Array<{
    title: string;
    url: string;
    publisher: string;
  }>;
  verificationStatus: string;
  lastCheckedDate: string;
}

export interface PlantSearchResponse {
  total: number;
  page: number;
  limit: number;
  totalPages: number;
  items: PlantSummaryItem[];
}

export interface PlantCategoryCount {
  category: string;
  count: number;
}

export interface PlantAutocompleteItem {
  id: string;
  scientificName: string;
  commonName: string;
  hindiName?: string;
  teluguName?: string;
  tamilName?: string;
  category: string;
  family: string;
  highlight: string;
  matchSource: string;
  statusInIndia?: string;
}

export interface PlantIdentificationResult {
  savedToAccount?: boolean;
  persistenceMessage?: string;
  success: boolean;
  mode: 'automatic' | 'name_assisted' | 'ollama_vision_screening';
  isAgricultural: boolean;
  detectedOrgan: string;
  organAnalysis?: {
    organ: string;
    confidence: number;
    evidence: string;
  };
  organHonestyNotice?: string;
  isAmbiguous: boolean;
  ambiguityMessage?: string;
  inDistribution?: boolean;
  directorySearchQuery?: string;
  topCandidate?: PlantSummaryItem;
  candidates: PlantSummaryItem[];
  suggestedDirectoryMatches?: PlantSummaryItem[];
  normalizedEntropy?: number;
  visualEvidence: string[];
  nameAssistedAnalysis?: {
    status: string;
    isConsistent?: boolean | null;
    explanation: string;
  };
  targetedPlant?: PlantSpeciesRecord;
  healthAssessment?: {
    healthStatus: string;
    healthScorePercentage: number;
    chlorosisPercentage: number;
    necrosisPercentage: number;
    mildewPercentage: number;
    symptoms: string[];
  };
  recommendations?: Array<{
    title: string;
    description: string;
    type: string;
  }>;
  analysisTimestamp: string;
  visualCondition?: string;
  ripenessStatus?: string;
  spoilageStatus?: string;
  visualSummary?: string;
  possibleIssues?: Array<{ name?: string; evidence?: string; likelihood?: string }>;
  precautions?: string[];
  analysisSource?: string;
  error?: string;
}

export interface HealthSymptomItem {
  symptom: string;
  severityPercentage: number;
  severityLevel: 'None' | 'Mild' | 'Moderate' | 'Severe' | string;
  description: string;
}

export interface HealthRecommendation {
  title: string;
  description: string;
  type: 'action' | 'organic' | 'chemical' | 'prevention' | 'info' | string;
}

export interface PlantHealthAnalysisResult {
  savedToAccount?: boolean;
  persistenceMessage?: string;
  success: boolean;
  plantName: string;
  healthStatus: string;
  healthScorePercentage: number;
  observedSymptoms: HealthSymptomItem[];
  diseaseModelAvailable: boolean;
  diseaseDiagnosis?: {
    matchedCrop?: string;
    predictedCondition?: string;
    confidence?: number;
    isHealthy?: boolean;
    explanation?: string;
    modelStatus?: string;
  };
  diagnosisNotice: string;
  recommendations: HealthRecommendation[];
  disclaimer: string;
  analysisTimestamp: string;
  error?: string;
  imageType?: string;
  detectedSubject?: string;
  visualCondition?: string;
  ripenessStatus?: string;
  spoilageStatus?: string;
  visualSummary?: string;
  visualObservations?: string[];
  possibleIssues?: Array<{ name?: string; evidence?: string; likelihood?: string }>;
  precautions?: string[];
  analysisSource?: string;
}

