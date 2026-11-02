import React, { useState, useEffect } from 'react';
import {
  Sprout,
  AlertCircle,
  CheckCircle2,
  AlertTriangle,
  Loader2,
  RefreshCw,
  Droplets,
  Sun,
  Layers,
  Sparkles,
  ShieldCheck,
  HelpCircle,
  Info,
  Bug,
  Activity,
  Search,
} from 'lucide-react';
import { ImageUploader } from '../components/ImageUploader';
import { productionService } from '../services/productionService';
import { NamedPlantAnalysisResult, SupportedPlantItem } from '../types';
import { PersistenceNotice } from '../components/PersistenceNotice';

export const AnalyseMyPlant: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [plantName, setPlantName] = useState<string>('');
  const [cropType, setCropType] = useState<string>('');
  const [growingLocation, setGrowingLocation] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<NamedPlantAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Autocomplete catalogue state
  const [supportedPlants, setSupportedPlants] = useState<SupportedPlantItem[]>([]);
  const [filteredSuggestions, setFilteredSuggestions] = useState<SupportedPlantItem[]>([]);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);

  useEffect(() => {
    // Fetch supported plant catalogue on mount for autocomplete
    productionService.getSupportedPlants().then((data) => {
      setSupportedPlants(data);
    });
  }, []);

  const handlePlantNameChange = (val: string) => {
    setPlantName(val);
    if (val.trim().length > 0) {
      const q = val.toLowerCase();
      const matches = supportedPlants.filter(
        (p) => p.name.toLowerCase().includes(q) || p.scientificName.toLowerCase().includes(q)
      );
      setFilteredSuggestions(matches);
      setShowSuggestions(true);
    } else {
      setFilteredSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const handleSelectSuggestion = (p: SupportedPlantItem) => {
    setPlantName(p.name);
    setCropType(p.category);
    setShowSuggestions(false);
  };

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError('Please select or capture a plant image.');
      return;
    }
    if (!plantName.trim()) {
      setError('Please enter or select the plant name.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await productionService.analyzeNamedPlant(
        selectedImage,
        plantName,
        cropType || undefined,
        growingLocation || undefined
      );
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Plant health analysis could not be completed.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-[#fbfcf9] py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-900 border border-emerald-300 text-xs font-bold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5 text-emerald-700" />
            Better Production — Recommended Mode
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-agro-950">
            Plant Health Analysis by Name
          </h1>
          <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
            Upload your plant photograph, provide the plant name, and specify your growing environment.
            Our engine extracts observable symptoms (yellowing, brown spots, dryness, mildew), assesses health,
            uses available screening models where supported, and delivers general care guidance. Results are not a verified field diagnosis.
          </p>
        </div>

        {/* Input & Upload Card */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-card space-y-6">
          {/* Plant Name & Metadata Inputs */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Plant Name with Autocomplete */}
            <div className="relative md:col-span-1">
              <label className="block text-xs font-bold text-gray-700 mb-1.5 flex items-center gap-1">
                Plant / Crop Name <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={plantName}
                  onChange={(e) => handlePlantNameChange(e.target.value)}
                  onFocus={() => {
                    if (plantName.trim().length > 0) setShowSuggestions(true);
                  }}
                  placeholder="e.g. Tomato, Rose, Tulsi, Monstera"
                  className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 text-xs sm:text-sm text-gray-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 bg-white"
                />
                <Search className="w-4 h-4 absolute right-3 top-3 text-gray-400 pointer-events-none" />
              </div>

              {/* Autocomplete Dropdown */}
              {showSuggestions && filteredSuggestions.length > 0 && (
                <div className="absolute z-20 w-full mt-1 bg-white rounded-xl border border-gray-200 shadow-xl max-h-60 overflow-y-auto">
                  <div className="p-1.5 text-[10px] font-bold text-gray-400 uppercase tracking-wider border-b border-gray-100">
                    Recognized Plants & Models
                  </div>
                  {filteredSuggestions.map((item) => (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => handleSelectSuggestion(item)}
                      className="w-full text-left px-3 py-2 text-xs hover:bg-emerald-50 flex items-center justify-between transition-colors border-b border-gray-50 last:border-0"
                    >
                      <div>
                        <p className="font-bold text-gray-900">{item.name}</p>
                        <p className="text-[10px] text-gray-500 italic">{item.scientificName}</p>
                      </div>
                      <span
                        className={`text-[9px] font-bold px-1.5 py-0.5 rounded-md ${
                          item.diseaseModelAvailable
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-600'
                        }`}
                      >
                        {item.diseaseModelAvailable ? 'Disease Model' : 'Care Guide'}
                      </span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Optional Crop Type */}
            <div>
              <label className="block text-xs font-bold text-gray-700 mb-1.5">
                Crop Category <span className="text-gray-400 font-normal">(Optional)</span>
              </label>
              <select
                value={cropType}
                onChange={(e) => setCropType(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 text-xs sm:text-sm text-gray-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 bg-white"
              >
                <option value="">Select category...</option>
                <option value="Vegetable">Vegetable</option>
                <option value="Fruit">Fruit / Orchard</option>
                <option value="Cereal Grain">Cereal Grain</option>
                <option value="Ornamental / Flower">Ornamental / Flowering</option>
                <option value="Herb / Medicinal">Herb / Medicinal</option>
                <option value="Houseplant / Indoor">Indoor Houseplant</option>
                <option value="Succulent / Cactus">Succulent / Cactus</option>
                <option value="Cash Crop / Fiber">Cash Crop / Fiber</option>
                <option value="Other">Other</option>
              </select>
            </div>

            {/* Optional Growing Location */}
            <div>
              <label className="block text-xs font-bold text-gray-700 mb-1.5">
                Growing Environment <span className="text-gray-400 font-normal">(Optional)</span>
              </label>
              <select
                value={growingLocation}
                onChange={(e) => setGrowingLocation(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 text-xs sm:text-sm text-gray-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 bg-white"
              >
                <option value="">Select location...</option>
                <option value="Indoor Potted">Indoor Potted (Living room, Desk)</option>
                <option value="Outdoor Balcony / Terrace">Outdoor Balcony / Terrace</option>
                <option value="Backyard Garden Bed">Backyard Garden Bed</option>
                <option value="Open Field Farm">Open Field Farm</option>
                <option value="Commercial Greenhouse">Commercial Greenhouse / Polyhouse</option>
                <option value="Hydroponic / Aeroponic">Hydroponic / Soil-less</option>
              </select>
            </div>
          </div>

          {/* Image Uploader */}
          <div className="pt-2">
            <ImageUploader
              selectedImage={selectedImage}
              onImageSelected={(file) => {
                setSelectedImage(file);
                setResult(null);
                setError(null);
              }}
              onClearImage={handleReset}
              label="Select Plant / Leaf Photograph"
              helperText="Upload clear daylight photo focusing on foliage, leaves, or stem spots"
            />
          </div>

          {/* Error Notice */}
          {error && (
            <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-red-800 text-xs flex items-start gap-3 animate-in fade-in">
              <AlertCircle className="w-5 h-5 shrink-0 text-red-600 mt-0.5" />
              <div className="space-y-1">
                <p className="font-bold text-sm">Analysis Advisory</p>
                <p>{error}</p>
              </div>
            </div>
          )}

          {/* Action Button */}
          {selectedImage && !result && (
            <button
              onClick={handleAnalyze}
              disabled={loading || !plantName.trim()}
              className="w-full flex items-center justify-center gap-2 py-3.5 px-6 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm shadow-md transition-all disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-emerald-200" />
                  Extracting Observable Symptoms & Formulating Care Plan...
                </>
              ) : (
                <>
                  <Sprout className="w-4 h-4 text-emerald-200" />
                  Analyse Plant Health for "{plantName.trim() || 'My Plant'}"
                </>
              )}
            </button>
          )}
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
            <PersistenceNotice savedToAccount={result.savedToAccount} message={result.persistenceMessage} />
            {/* Top Banner Card */}
            <div
              className={`rounded-3xl p-6 sm:p-8 border shadow-card ${
                result.healthAssessment === 'Healthy-looking'
                  ? 'bg-gradient-to-br from-emerald-50 via-white to-emerald-50/50 border-emerald-300'
                  : 'bg-gradient-to-br from-amber-50 via-white to-amber-50/50 border-amber-300'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-gray-200/80">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-gray-500">
                      User Plant
                    </span>
                    <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-900 font-bold">
                      {result.scientificName || 'Botanical Specimen'}
                    </span>
                    {result.cropType && (
                      <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-700 font-medium">
                        {result.cropType}
                      </span>
                    )}
                  </div>
                  <h2 className="text-3xl font-extrabold text-agro-950">
                    {result.userPlantName}
                  </h2>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <p className="text-[10px] uppercase font-bold text-gray-400">Health Assessment</p>
                    <p
                      className={`text-lg font-extrabold ${
                        result.healthAssessment === 'Healthy-looking'
                          ? 'text-emerald-700'
                          : 'text-amber-700'
                      }`}
                    >
                      {result.healthAssessment}
                    </p>
                  </div>
                  <div
                    className={`w-12 h-12 rounded-2xl flex items-center justify-center shadow-sm ${
                      result.healthAssessment === 'Healthy-looking'
                        ? 'bg-emerald-100 text-emerald-700'
                        : 'bg-amber-100 text-amber-700'
                    }`}
                  >
                    {result.healthAssessment === 'Healthy-looking' ? (
                      <CheckCircle2 className="w-6 h-6" />
                    ) : (
                      <AlertTriangle className="w-6 h-6" />
                    )}
                  </div>
                </div>
              </div>

              {/* Health Score & Validation Details */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-6">
                {/* Health % Meter */}
                <div className="bg-white/90 p-4 rounded-2xl border border-gray-200 space-y-2">
                  <div className="flex items-center justify-between">
                    <p className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">
                      Visual health assessment
                    </p>
                    <span
                      className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                        result.healthScorePercentage >= 80
                          ? 'bg-emerald-100 text-emerald-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}
                    >
                      {result.analysisSource === 'ollama_vision_screening_unvalidated' ? 'Qualitative only' : (result.healthScorePercentage >= 80 ? 'Vigorous' : 'Needs Care')}
                    </span>
                  </div>
                  <p className="text-2xl font-extrabold text-emerald-700">
                    {result.analysisSource === 'ollama_vision_screening_unvalidated' ? 'Visual estimate' : `${result.healthScorePercentage.toFixed(1)}%`}
                  </p>
                  {result.analysisSource !== 'ollama_vision_screening_unvalidated' && <div className="w-full bg-gray-100 h-2.5 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-emerald-500 to-green-600 rounded-full transition-all"
                      style={{ width: `${Math.min(result.healthScorePercentage, 100)}%` }}
                    ></div>
                  </div>}
                  <p className="text-[10px] text-gray-500">
                    {result.analysisSource === 'ollama_vision_screening_unvalidated' ? 'This result describes visible appearance; it is not a measured health percentage.' : 'Estimate from observable image features; not a laboratory measurement.'}
                  </p>
                </div>

                {/* Validation Status */}
                <div className="bg-white/90 p-4 rounded-2xl border border-gray-200 space-y-2">
                  <p className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">
                    Foliage Verification
                  </p>
                  <div className="flex items-center gap-1.5 pt-1">
                    <ShieldCheck className="w-5 h-5 text-emerald-600" />
                    <span className="text-xs font-bold text-gray-800">
                      {result.validationStatus}
                    </span>
                  </div>
                  <p className="text-[11px] text-gray-600 leading-relaxed pt-1">
                    {result.validationMessage}
                  </p>
                </div>

                {/* Environment & Location */}
                <div className="bg-white/90 p-4 rounded-2xl border border-gray-200 space-y-2">
                  <p className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">
                    Cultivation Context
                  </p>
                  <p className="text-sm font-bold text-gray-900 pt-1">
                    {result.growingLocation || 'Standard Cultivation'}
                  </p>
                  <p className="text-[10px] text-gray-400">
                    Analysis executed at {new Date(result.analysisTimestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            </div>

            {(result.visualSummary || result.visualObservations?.length || result.possibleIssues?.length || result.ripenessStatus || result.spoilageStatus) && (
              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-emerald-200 shadow-soft space-y-4">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-emerald-600" />
                  <h3 className="text-lg font-bold text-agro-950">Image Summary & Visible Condition</h3>
                </div>
                {result.visualSummary && <p className="text-sm leading-relaxed text-gray-700">{result.visualSummary}</p>}
                <div className="flex flex-wrap gap-2">
                  {result.imageType && <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-800">Image type: {result.imageType.replace(/_/g, ' ')}</span>}
                  {result.visibleCondition && <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-800">Visible condition: {result.visibleCondition.replace(/_/g, ' ')}</span>}
                  {result.ripenessStatus && result.ripenessStatus !== 'not_applicable' && <span className="rounded-full bg-orange-50 px-3 py-1 text-xs font-semibold text-orange-800">Ripeness: {result.ripenessStatus.replace(/_/g, ' ')}</span>}
                  {result.spoilageStatus && result.spoilageStatus !== 'not_applicable' && <span className="rounded-full bg-rose-50 px-3 py-1 text-xs font-semibold text-rose-800">Visible spoilage: {result.spoilageStatus.replace(/_/g, ' ')}</span>}
                </div>
                {result.visualObservations?.length ? <div><p className="mb-2 text-xs font-bold uppercase tracking-wide text-gray-500">Visible evidence</p><ul className="list-disc space-y-1 pl-5 text-sm text-gray-700">{result.visualObservations.map((item, idx) => <li key={idx}>{item}</li>)}</ul></div> : null}
                {result.possibleIssues?.length ? <div><p className="mb-2 text-xs font-bold uppercase tracking-wide text-gray-500">Possible issues — not confirmed</p><div className="space-y-2">{result.possibleIssues.map((issue, idx) => <div key={idx} className="rounded-xl border border-amber-200 bg-amber-50/60 p-3"><p className="text-sm font-semibold text-amber-950">{issue.name || 'Possible visible issue'}</p>{issue.evidence && <p className="mt-1 text-sm text-gray-700">Evidence: {issue.evidence}</p>}</div>)}</div></div> : null}
                {result.precautions?.length ? <div><p className="mb-2 text-xs font-bold uppercase tracking-wide text-gray-500">Precautions</p><ul className="list-disc space-y-1 pl-5 text-sm text-gray-700">{result.precautions.map((item, idx) => <li key={idx}>{item}</li>)}</ul></div> : null}
              </div>
            )}

            {/* Observable Symptoms Section */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-agro-950 flex items-center gap-2">
                  <Activity className="w-5 h-5 text-emerald-600" />
                  Observed Visual Symptoms (Image Feature Analysis)
                </h3>
                <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-gray-100 text-gray-700">
                  Separated from Disease Diagnosis
                </span>
              </div>
              <p className="text-xs text-gray-500">
                These are qualitative visual observations from the uploaded image. They are not measured affected-area percentages or a confirmed diagnosis.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                {result.observedSymptoms.map((sym, idx) => (
                  <div
                    key={idx}
                    className={`p-4 rounded-2xl border space-y-2 ${
                      sym.severity === 'Severe'
                        ? 'bg-red-50/70 border-red-200'
                        : sym.severity === 'Moderate'
                        ? 'bg-amber-50/70 border-amber-200'
                        : sym.severity === 'Mild'
                        ? 'bg-yellow-50/60 border-yellow-200'
                        : 'bg-gray-50 border-gray-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-xs text-gray-900">{sym.name}</span>
                      <span
                        className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full ${
                          sym.severity === 'Severe'
                            ? 'bg-red-200 text-red-900'
                            : sym.severity === 'Moderate'
                            ? 'bg-amber-200 text-amber-900'
                            : sym.severity === 'Mild'
                            ? 'bg-yellow-200 text-yellow-900'
                            : 'bg-emerald-100 text-emerald-800'
                        }`}
                      >
                        {sym.severity}{result.analysisSource === 'ollama_vision_screening_unvalidated' ? ' · qualitative' : ` (${sym.percentage}%)`}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 leading-relaxed">{sym.observation}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Disease Model Diagnosis Card (Honest Status Handling) */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-bold text-agro-950 flex items-center gap-2">
                  <Bug className="w-5 h-5 text-emerald-600" />
                  Machine Learning Disease Classifier Status
                </h3>
                <span
                  className={`text-xs font-bold px-3 py-1 rounded-full border ${
                    result.diseaseModelAvailable
                      ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                      : 'bg-gray-100 text-gray-700 border-gray-200'
                  }`}
                >
                  {result.diseaseModelAvailable ? 'Trained Model Active' : (result.analysisSource === 'ollama_vision_screening_unvalidated' ? 'Visual screening only' : 'Model Not Trained For This Species')}
                </span>
              </div>

              {result.diseaseModelAvailable ? (
                <div className="p-4 rounded-2xl bg-emerald-50/50 border border-emerald-200 space-y-2">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-bold text-emerald-950">
                      Possible Disease / Condition: <span className="underline">{result.possibleDisease}</span>
                    </p>
                    {result.diseaseConfidence && (
                      <span className="text-xs font-bold bg-emerald-100 text-emerald-900 px-2 py-0.5 rounded">
                        Confidence: {(result.diseaseConfidence * 100).toFixed(1)}%
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-gray-600 leading-relaxed">
                    {result.diseaseDiagnosisNotice}
                  </p>
                </div>
              ) : (
                <div className="p-4 rounded-2xl bg-gray-50 border border-gray-200 space-y-1">
                  <div className="flex items-center gap-2 text-xs font-bold text-gray-800">
                    <Info className="w-4 h-4 text-gray-500" />
                    Limited Disease Diagnostics Notice
                  </div>
                  <p className="text-xs text-gray-600 leading-relaxed">
                    {result.diseaseDiagnosisNotice}
                  </p>
                </div>
              )}
            </div>

            {/* Plant Care Guide (Watering, Light, Soil, Humidity, Nutrition) */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
              <h3 className="text-lg font-bold text-agro-950 flex items-center gap-2">
                <Sprout className="w-5 h-5 text-emerald-600" />
                Verified Botanical Care Profile for {result.userPlantName}
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
                {/* Watering */}
                <div className="p-4 rounded-2xl bg-blue-50/60 border border-blue-100 space-y-1.5">
                  <div className="flex items-center gap-2 text-xs font-bold text-blue-900">
                    <Droplets className="w-4 h-4 text-blue-600" />
                    Watering Protocol
                  </div>
                  <p className="text-xs text-gray-700 leading-relaxed">{result.careGuide.watering}</p>
                </div>

                {/* Sunlight */}
                <div className="p-4 rounded-2xl bg-amber-50/60 border border-amber-100 space-y-1.5">
                  <div className="flex items-center gap-2 text-xs font-bold text-amber-900">
                    <Sun className="w-4 h-4 text-amber-600" />
                    Sunlight & Exposure
                  </div>
                  <p className="text-xs text-gray-700 leading-relaxed">{result.careGuide.sunlight}</p>
                </div>

                {/* Soil */}
                <div className="p-4 rounded-2xl bg-earth-50/60 border border-earth-200/60 space-y-1.5">
                  <div className="flex items-center gap-2 text-xs font-bold text-earth-900">
                    <Layers className="w-4 h-4 text-earth-700" />
                    Soil & Substrate
                  </div>
                  <p className="text-xs text-gray-700 leading-relaxed">{result.careGuide.soil}</p>
                </div>

                {/* Nutrition */}
                <div className="p-4 rounded-2xl bg-emerald-50/60 border border-emerald-100 space-y-1.5">
                  <div className="flex items-center gap-2 text-xs font-bold text-emerald-900">
                    <Sparkles className="w-4 h-4 text-emerald-600" />
                    Nutrition & Fertilization
                  </div>
                  <p className="text-xs text-gray-700 leading-relaxed">{result.careGuide.nutrition}</p>
                </div>
              </div>
            </div>

            {/* 4 to 5 Tailored Action Recommendations */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-5">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-agro-950">
                    Tailored Care & Symptom Management Actions
                  </h3>
                  <p className="text-xs text-gray-500">
                    Specific agronomic adjustments formulated for {result.userPlantName} based on observed symptoms
                  </p>
                </div>
                <span className="text-xs font-bold text-emerald-800 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                  {result.recommendations.length} Action Items
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.recommendations.map((rec, index) => (
                  <div
                    key={index}
                    className="p-4 rounded-2xl bg-gray-50 border border-gray-200 space-y-2 hover:bg-emerald-50/50 hover:border-emerald-300 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-emerald-900 flex items-center gap-1.5">
                        <span className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center text-[10px] font-bold">
                          {index + 1}
                        </span>
                        {rec.title}
                      </span>
                      <span className="text-[10px] uppercase font-bold text-gray-400 bg-white px-2 py-0.5 rounded border">
                        {rec.type}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 leading-relaxed">{rec.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* General Cultural Management Tips */}
            {result.generalManagementTips && result.generalManagementTips.length > 0 && (
              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
                <h3 className="text-lg font-bold text-agro-950 flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-emerald-600" />
                  Long-term Cultural Practices & Prevention
                </h3>
                <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-gray-700">
                  {result.generalManagementTips.map((tip, idx) => (
                    <li
                      key={idx}
                      className="flex items-start gap-2 bg-agro-50/60 p-3 rounded-xl border border-agro-100"
                    >
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Disclaimer */}
            <div className="p-4 rounded-2xl bg-gray-100 border border-gray-200 text-[11px] text-gray-500 leading-relaxed flex items-start gap-2">
              <HelpCircle className="w-4 h-4 shrink-0 text-gray-400 mt-0.5" />
              <span>{result.disclaimer}</span>
            </div>

            {/* Actions Bar */}
            <div className="flex justify-between items-center pt-2">
              <button
                onClick={handleReset}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-bold transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" /> Analyze Another Plant
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
