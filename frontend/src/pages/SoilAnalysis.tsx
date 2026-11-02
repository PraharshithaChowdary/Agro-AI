import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Layers,
  AlertCircle,
  CheckCircle2,
  Loader2,
  RefreshCw,
  Info,
  Sprout,
  FlaskConical,
  ArrowRight,
  Leaf,
} from 'lucide-react';
import { ImageUploader } from '../components/ImageUploader';
import { PersistenceNotice } from '../components/PersistenceNotice';
import { productionService } from '../services/productionService';
import { SoilAnalysisResult } from '../types';

export const SoilAnalysis: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SoilAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await productionService.analyzeSoil(selectedImage);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Soil analysis could not be completed.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setResult(null);
    setError(null);
  };

  const isCropLeafError = error && (
    error.toLowerCase().includes('crop / plant leaf') ||
    error.toLowerCase().includes('crop analysis') ||
    error.toLowerCase().includes('plant leaf')
  );

  return (
    <div className="min-h-screen bg-[#fbfcf9] py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-bold tracking-wide">
            <Layers className="w-3.5 h-3.5 text-amber-700" />
            Soil Diagnostics & Crop Suitability
          </div>
          <h1 className="text-3xl font-extrabold text-agro-950">Visual Soil Assessment</h1>
          <p className="text-xs sm:text-sm text-gray-600">
            Upload genuine soil surface photographs to classify soil category (Alluvial, Black/Regur, Red, Laterite, Heavy Clay, Sandy Loam), identify crop suitability, and receive organic structural guidance.
          </p>
        </div>

        {/* Upload Card */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-card">
          <div className="space-y-6">
            <ImageUploader
              selectedImage={selectedImage}
              onImageSelected={(file) => {
                setSelectedImage(file);
                setResult(null);
                setError(null);
              }}
              onClearImage={handleReset}
              label="Select Soil Sample Photograph"
              helperText="Upload topsoil, earth, or ground photo in clear natural lighting (JPG, PNG, WebP)"
            />

            {/* Error / Cross-Module Notice */}
            {error && (
              <div className={`p-5 rounded-2xl border text-xs animate-in fade-in space-y-3 ${
                isCropLeafError ? 'bg-green-50 border-green-300 text-green-950' : 'bg-red-50 border-red-200 text-red-800'
              }`}>
                <div className="flex items-start gap-3">
                  {isCropLeafError ? (
                    <Leaf className="w-5 h-5 shrink-0 text-green-700 mt-0.5" />
                  ) : (
                    <AlertCircle className="w-5 h-5 shrink-0 text-red-600 mt-0.5" />
                  )}
                  <div className="space-y-1 flex-1">
                    <p className="font-bold text-sm">
                      {isCropLeafError ? 'Plant Foliage Detected!' : 'Soil Assessment Notice'}
                    </p>
                    <p className="leading-relaxed">{error}</p>
                  </div>
                </div>

                {isCropLeafError && (
                  <div className="pt-2 border-t border-green-200 flex items-center justify-between">
                    <span className="text-[11px] text-green-800 font-medium">
                      Would you like to diagnose this leaf in the Crop Disease Analysis module?
                    </span>
                    <Link
                      to="/production/crop"
                      className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-green-700 hover:bg-green-800 text-white font-bold text-xs shadow-sm transition-colors"
                    >
                      Switch to Crop Analysis
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                )}
              </div>
            )}

            {selectedImage && !result && (
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full flex items-center justify-center gap-2 py-3.5 px-6 rounded-xl bg-earth-700 hover:bg-earth-800 text-white font-bold text-sm shadow-md transition-all disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-amber-300" />
                    Validating Soil Sample & Evaluating Texture/Category...
                  </>
                ) : (
                  <>
                    <Layers className="w-4 h-4 text-amber-300" />
                    Run Visual Soil Assessment
                  </>
                )}
              </button>
            )}
          </div>
        </div>

        {/* Results */}
        {result && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
            <PersistenceNotice savedToAccount={result.savedToAccount} message={result.persistenceMessage} />
            {/* Top Category Banner */}
            <div className="bg-gradient-to-br from-amber-50 via-white to-earth-50 rounded-3xl p-6 sm:p-8 border border-amber-300 shadow-card">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-gray-200/80">
                <div className="space-y-1">
                  <span className="text-xs font-bold uppercase tracking-wider text-amber-800 bg-amber-100/70 px-2.5 py-0.5 rounded-full">
                    Visual Classification
                  </span>
                  <h2 className="text-3xl font-extrabold text-agro-950">
                    {result.predictedSoilCategory}
                  </h2>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <p className="text-[10px] uppercase font-bold text-gray-400">Assessment basis</p>
                    <p className="text-lg font-extrabold text-earth-800">{result.predictedSoilCategory.toLowerCase().includes('uncertain') ? 'Needs clearer sample' : 'Visual candidate'}</p>
                  </div>
                  <div className="w-12 h-12 rounded-2xl bg-amber-100 text-amber-800 flex items-center justify-center shadow-sm">
                    <Layers className="w-6 h-6" />
                  </div>
                </div>
              </div>

              <p className="pt-4 text-[11px] text-gray-500">Based on visible surface features only • {new Date(result.analysisTimestamp).toLocaleTimeString()}</p>
            </div>

            {(result.report || result.summary) && (
              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-amber-200 shadow-soft space-y-3">
                <h3 className="text-lg font-bold text-agro-950">Soil Assessment Report</h3>
                {result.report ? (
                  <div className="space-y-4 text-sm leading-relaxed text-gray-700">
                    <div><p className="text-[11px] font-bold uppercase tracking-wide text-gray-500">Visible finding</p><p>{result.report.visualFinding}</p></div>
                    <div><p className="text-[11px] font-bold uppercase tracking-wide text-gray-500">Category interpretation</p><p>{result.report.categoryInterpretation}</p></div>
                    <div><p className="text-[11px] font-bold uppercase tracking-wide text-gray-500">Next steps</p><p>{result.report.nextSteps}</p></div>
                    {result.pHRange && !result.pHRange.toLowerCase().includes('cannot be determined') && <p className="border-t border-gray-100 pt-3 text-xs text-gray-600"><strong>Typical pH reference:</strong> {result.pHRange}</p>}
                  </div>
                ) : <p className="text-sm leading-relaxed text-gray-700">{result.summary}</p>}
                <p className="text-xs leading-relaxed text-gray-500">Visual categorization is preliminary. Soil pH, nutrient levels, salinity and fertilizer needs require a representative laboratory soil test.</p>
              </div>
            )}

            {/* Visual Observations */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
              <h3 className="text-lg font-bold text-agro-950 flex items-center gap-2">
                <Info className="w-5 h-5 text-amber-700" />
                Physical Characteristics & Visual Observations
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-gray-700">
                {result.visualObservations.map((obs, idx) => (
                  <div key={idx} className="flex items-start gap-2 bg-gray-50 p-3 rounded-xl border border-gray-200">
                    <CheckCircle2 className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                    <span>{obs}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Suitable Crops */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
              <h3 className="text-lg font-bold text-agro-950 flex items-center gap-2">
                <Sprout className="w-5 h-5 text-green-700" />
                Agronomically Suitable Crops
              </h3>
              <p className="text-xs text-gray-500">
                Crops documented to thrive in {result.predictedSoilCategory.toLowerCase()} conditions:
              </p>
              <div className="flex flex-wrap gap-2 pt-1">
                {result.suitableCrops.length ? result.suitableCrops.map((crop, idx) => (
                  <span
                    key={idx}
                    className="px-3.5 py-1.5 rounded-xl bg-green-50 text-green-900 border border-green-200 text-xs font-bold"
                  >
                    🌾 {crop}
                  </span>
                )) : <p className="text-xs text-gray-600">Confirm the soil group with a soil test before using crop-suitability guidance.</p>}
              </div>
            </div>

            {/* Structural Soil Improvement & Fertilizer Guidance */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
                <h3 className="text-base font-bold text-agro-950">
                  Soil Structure & Organic Improvement
                </h3>
                <ul className="space-y-2 text-xs text-gray-700">
                  {result.soilImprovementGuidance.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-600 mt-1.5 shrink-0"></span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
                <h3 className="text-base font-bold text-agro-950">
                  Fertilizer & Amendment Considerations
                </h3>
                <ul className="space-y-2 text-xs text-gray-700">
                  {result.fertilizerGuidance.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-green-600 mt-1.5 shrink-0"></span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Mandatory Chemical / Laboratory Testing Disclaimer */}
            <div className="bg-amber-50 rounded-3xl p-6 border border-amber-200 flex items-start gap-4">
              <FlaskConical className="w-6 h-6 text-amber-700 shrink-0 mt-0.5" />
              <div className="space-y-1 text-xs text-amber-900">
                <p className="font-bold">Laboratory Soil Testing Disclaimer</p>
                <p className="leading-relaxed">
                  {result.limitationsDisclaimer ||
                    'Visual soil assessment identifies texture, color, and macro characteristics. Exact chemical properties such as precise pH, available Nitrogen (N), Phosphorus (P), and Potassium (K) cannot be fabricated from photographs alone. Please consult an accredited soil testing laboratory before applying concentrated synthetic chemicals.'}
                </p>
              </div>
            </div>

            {/* Actions Bar */}
            <div className="flex justify-between items-center pt-2">
              <button
                onClick={handleReset}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-bold transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" /> Assess Another Soil Sample
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
