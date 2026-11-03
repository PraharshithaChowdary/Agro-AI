import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Sprout,
  AlertCircle,
  CheckCircle2,
  Loader2,
  RefreshCw,
  ShieldCheck,
  Leaf,
  Bug,
  FileText,
  Layers,
  ArrowRight,
} from 'lucide-react';
import { ImageUploader } from '../components/ImageUploader';
import { productionService } from '../services/productionService';
import { CropAnalysisResult } from '../types';
import { PersistenceNotice } from '../components/PersistenceNotice';

export const CropAnalysis: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CropAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await productionService.analyzeCrop(selectedImage);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Image analysis could not be completed.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setResult(null);
    setError(null);
  };

  const isSoilError = error && (error.toLowerCase().includes('soil sample') || error.toLowerCase().includes('soil analysis'));

  return (
    <div className="min-h-screen bg-[#fbfcf9] py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-green-100 text-green-800 text-xs font-bold tracking-wide">
            <Leaf className="w-3.5 h-3.5 text-green-600" />
            Foliar & Crop Diagnostics
          </div>
          <h1 className="text-3xl font-extrabold text-agro-950">Crop & Plant Foliage Analysis</h1>
          <p className="text-xs sm:text-sm text-gray-600">
            Upload a clear crop or plant photo to get visible findings, a practical assessment, and suggested next steps. Confirm suspected disease with a local agricultural adviser before treatment.
          </p>
        </div>

        {/* Upload & Action Card */}
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
              label="Select Crop / Plant Leaf Photograph"
              helperText="Upload a clear daylight crop / leaf photo. Results are preliminary screening, not a confirmed diagnosis."
            />

            {/* Error / Cross-Module Notice */}
            {error && (
              <div className={`p-5 rounded-2xl border text-xs animate-in fade-in space-y-3 ${
                isSoilError ? 'bg-amber-50 border-amber-300 text-amber-950' : 'bg-red-50 border-red-200 text-red-800'
              }`}>
                <div className="flex items-start gap-3">
                  {isSoilError ? (
                    <Layers className="w-5 h-5 shrink-0 text-amber-700 mt-0.5" />
                  ) : (
                    <AlertCircle className="w-5 h-5 shrink-0 text-red-600 mt-0.5" />
                  )}
                  <div className="space-y-1 flex-1">
                    <p className="font-bold text-sm">
                      {isSoilError ? 'Soil Sample Detected!' : 'Analysis Notice'}
                    </p>
                    <p className="leading-relaxed">{error}</p>
                  </div>
                </div>

                {isSoilError && (
                  <div className="pt-2 border-t border-amber-200 flex items-center justify-between">
                    <span className="text-[11px] text-amber-800 font-medium">
                      Would you like to analyze this image in the Soil Assessment module?
                    </span>
                    <Link
                      to="/production/soil"
                      className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-earth-700 hover:bg-earth-800 text-white font-bold text-xs shadow-sm transition-colors"
                    >
                      Switch to Soil Analysis
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
                className="w-full flex items-center justify-center gap-2 py-3.5 px-6 rounded-xl bg-green-700 hover:bg-green-800 text-white font-bold text-sm shadow-md transition-all disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-green-300" />
                    Analyzing image and preparing report...
                  </>
                ) : (
                  <>
                    <Sprout className="w-4 h-4 text-green-300" />
                    Analyze Crop Image
                  </>
                )}
              </button>
            )}
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
            <PersistenceNotice savedToAccount={result.savedToAccount} message={result.persistenceMessage} />
            {/* Top Result Banner */}
            <div
              className={`rounded-3xl p-6 sm:p-8 border shadow-card ${
                result.isHealthy
                  ? 'bg-gradient-to-br from-green-50 via-white to-green-50/50 border-green-300'
                  : 'bg-gradient-to-br from-amber-50 via-white to-amber-50/50 border-amber-300'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-gray-200/80">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-gray-500">
                      Identified Specimen
                    </span>
                    <span className="text-xs px-2.5 py-0.5 rounded-full bg-agro-100 text-agro-900 font-bold">
                      {result.scientificName || 'Botanical Specimen'}
                    </span>
                  </div>
                  <h2 className="text-3xl font-extrabold text-agro-950">
                    {result.predictedCrop}
                  </h2>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <p className="text-[10px] uppercase font-bold text-gray-400">Visual Assessment</p>
                    <p
                      className={`text-lg font-extrabold ${
                        result.isHealthy ? 'text-green-700' : 'text-amber-700'
                      }`}
                    >
                      {result.predictedCondition}
                    </p>
                  </div>
                  <div
                    className={`w-12 h-12 rounded-2xl flex items-center justify-center shadow-sm ${
                      result.isHealthy ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
                    }`}
                  >
                    {result.isHealthy ? (
                      <CheckCircle2 className="w-6 h-6" />
                    ) : (
                      <Bug className="w-6 h-6" />
                    )}
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-6">
                <div className="bg-white/90 p-4 rounded-2xl border border-gray-200 space-y-2">
                  <p className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">Visual condition</p>
                  <p className="text-lg font-extrabold text-agro-950">{result.predictedCondition}</p>
                  <p className="text-xs text-gray-500">Assessment from the visible image findings.</p>
                </div>
                <div className="bg-white/90 p-4 rounded-2xl border border-gray-200 space-y-2">
                  <p className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">Visible evidence</p>
                  <p className="text-sm font-semibold text-gray-800">
                    {result.visibleObservations?.[0] || result.possibleIssues?.[0]?.evidence || result.summary || 'See the full image report below.'}
                  </p>
                  {result.possibleIssues?.[0]?.name && <p className="text-xs text-amber-800">Possible issue: {result.possibleIssues[0].name}</p>}
                </div>
                <div className="bg-white/90 p-4 rounded-2xl border border-gray-200 space-y-2">
                  <p className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">Suggested next step</p>
                  <p className="text-sm font-semibold text-gray-800">{result.recommendations[0]?.title || 'Review the report'}</p>
                  <p className="text-xs text-gray-500">{result.recommendations[0]?.description || 'Use a clear close-up for more specific guidance.'}</p>
                </div>
              </div>
            </div>

            {/* Explanation Card */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-3">
              <h3 className="text-lg font-bold text-agro-950 flex items-center gap-2">
                <FileText className="w-5 h-5 text-green-600" />
                Agronomic Assessment & Foliar Overview
              </h3>
              <p className="text-xs sm:text-sm text-gray-700 leading-relaxed whitespace-pre-line">
                {result.explanation || result.summary}
              </p>
            </div>

            {(result.summary || result.visibleObservations?.length || result.possibleIssues?.length || result.precautions?.length || result.ripenessStatus || result.spoilageStatus) && (
              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-emerald-200 shadow-soft space-y-4">
                <h3 className="text-lg font-bold text-agro-950">Image Summary & Visible Condition</h3>
                {result.summary && <p className="text-sm leading-relaxed text-gray-700">{result.summary}</p>}
                <div className="flex flex-wrap gap-2">
                  {result.imageType && <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-800">Type: {result.imageType.replace(/_/g, ' ')}</span>}
                  {result.visibleCondition && <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-800">Condition: {result.visibleCondition.replace(/_/g, ' ')}</span>}
                  {result.ripenessStatus && result.ripenessStatus !== 'not_applicable' && <span className="rounded-full bg-orange-50 px-3 py-1 text-xs font-semibold text-orange-800">Ripeness: {result.ripenessStatus.replace(/_/g, ' ')}</span>}
                  {result.spoilageStatus && result.spoilageStatus !== 'not_applicable' && <span className="rounded-full bg-rose-50 px-3 py-1 text-xs font-semibold text-rose-800">Visible spoilage: {result.spoilageStatus.replace(/_/g, ' ')}</span>}
                </div>
                {result.visibleObservations?.length ? <div><p className="mb-2 text-xs font-bold uppercase tracking-wide text-gray-500">Visible evidence</p><ul className="list-disc space-y-1 pl-5 text-sm text-gray-700">{result.visibleObservations.map((item, idx) => <li key={idx}>{item}</li>)}</ul></div> : null}
                {result.possibleIssues?.length ? <div><p className="mb-2 text-xs font-bold uppercase tracking-wide text-gray-500">Possible issues — not confirmed</p><div className="space-y-2">{result.possibleIssues.map((issue, idx) => <div key={idx} className="rounded-xl border border-amber-200 bg-amber-50/60 p-3"><p className="text-sm font-semibold text-amber-950">{issue.name || 'Possible visible issue'}</p>{issue.evidence && <p className="mt-1 text-sm text-gray-700">Evidence: {issue.evidence}</p>}</div>)}</div></div> : null}
                {result.precautions?.length ? <div><p className="mb-2 text-xs font-bold uppercase tracking-wide text-gray-500">Precautions</p><ul className="list-disc space-y-1 pl-5 text-sm text-gray-700">{result.precautions.map((item, idx) => <li key={idx}>{item}</li>)}</ul></div> : null}
                {result.limitationsDisclaimer && <p className="border-t border-gray-100 pt-3 text-xs leading-relaxed text-gray-500">{result.limitationsDisclaimer}</p>}
              </div>
            )}

            {/* Targeted Recommendations */}
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-5">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-agro-950">
                    Suggested Next Steps
                  </h3>
                  <p className="text-xs text-gray-500">
                    {`Low-risk guidance for ${result.predictedCrop}, based on the visible image findings`}
                  </p>
                </div>
                <span className="text-xs font-bold text-green-700 bg-green-50 px-3 py-1 rounded-full border border-green-200">
                  {result.recommendations.length} Action Items
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.recommendations.map((rec, index) => (
                  <div
                    key={index}
                    className="p-4 rounded-2xl bg-gray-50 border border-gray-200 space-y-2 hover:bg-green-50/50 hover:border-green-300 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-green-800 flex items-center gap-1.5">
                        <span className="w-5 h-5 rounded-full bg-green-100 text-green-800 flex items-center justify-center text-[10px] font-bold">
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

            {/* Prevention & Basic Care Suggestions */}
            {result.preventionTips && result.preventionTips.length > 0 && (
              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-soft space-y-4">
                <h3 className="text-lg font-bold text-agro-950 flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-green-600" />
                  Long-term Prevention & Cultural Practices
                </h3>
                <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-gray-700">
                  {result.preventionTips.map((tip, idx) => (
                    <li key={idx} className="flex items-start gap-2 bg-agro-50/60 p-3 rounded-xl border border-agro-100">
                      <CheckCircle2 className="w-4 h-4 text-green-600 shrink-0 mt-0.5" />
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Actions Bar */}
            <div className="flex justify-between items-center pt-2">
              <button
                onClick={handleReset}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-bold transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" /> Analyze Another Plant Image
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
