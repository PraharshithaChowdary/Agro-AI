import React from 'react';
import { Link } from 'react-router-dom';
import { Sprout, Layers, ArrowRight, Sparkles, CheckCircle2, ShieldAlert } from 'lucide-react';

export const BetterProduction: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#fbfcf9] py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-10">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-green-100 text-green-900 border border-green-300 text-xs font-bold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5 text-green-600" />
            Better Production Hub
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-agro-950">
            Smart Crop & Soil Diagnostics
          </h1>
          <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
            Select a diagnostic module below to analyze plant specimens or evaluate soil suitability with local computer vision.
          </p>
        </div>

        {/* Two Clean Core Pillars: Plant Analysis & Soil Assessment */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Pillar 1: Plant Analysis & Identification */}
          <div className="bg-white rounded-3xl p-8 border border-gray-200 shadow-card hover:shadow-xl hover:border-emerald-500 transition-all flex flex-col justify-between group">
            <div>
              <div className="w-16 h-16 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center mb-6 group-hover:scale-105 transition-transform shadow-sm">
                <Sprout className="w-8 h-8 text-emerald-700" />
              </div>

              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-bold tracking-wide text-emerald-800 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-emerald-600" />
                  Visual Flora Diagnostics
                </span>
              </div>

              <h2 className="text-2xl font-bold text-agro-950 mb-3">Plant Analysis & Identification</h2>
              <p className="text-xs text-gray-600 leading-relaxed mb-6">
                Upload any plant photograph (leaf, stem, flower, fruit, or whole habit). Identifies Indian species with top-5 candidate matches, assesses foliar health condition, and provides 5 tailored care suggestions.
              </p>

              <div className="space-y-2.5 mb-8 text-xs text-gray-700">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Mode A (Automatic) & Mode B (By Plant Name)</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Supports leaves, stems, flowers, fruits & whole plants</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Telugu, Tamil, & Hindi regional vernacular names</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>5 Actionable care suggestions (water, light, soil, pests, maintenance)</span>
                </div>
              </div>
            </div>

            <Link
              to="/plants"
              className="w-full inline-flex items-center justify-center gap-2 py-3.5 px-4 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm shadow-md transition-colors"
            >
              Launch Plant Analysis
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          {/* Pillar 2: Soil Assessment */}
          <div className="bg-white rounded-3xl p-8 border border-gray-200 shadow-card hover:shadow-xl hover:border-amber-500 transition-all flex flex-col justify-between group">
            <div>
              <div className="w-16 h-16 rounded-2xl bg-amber-100 text-amber-900 flex items-center justify-center mb-6 group-hover:scale-105 transition-transform shadow-sm">
                <Layers className="w-8 h-8 text-amber-800" />
              </div>

              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-bold tracking-wide text-amber-800 bg-amber-50 px-3 py-1 rounded-full border border-amber-200 flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-amber-600" />
                  Pedological Assessment
                </span>
              </div>

              <h2 className="text-2xl font-bold text-agro-950 mb-3">Soil Category Assessment</h2>
              <p className="text-xs text-gray-600 leading-relaxed mb-6">
                Upload authentic soil photographs to classify visual soil types across 6 primary Indian categories (Alluvial, Black, Clay, Laterite, Red, Sandy) and view recommended crop compatibility.
              </p>

              <div className="space-y-2.5 mb-8 text-xs text-gray-700">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-amber-700 shrink-0" />
                  <span>Visual categorization across 6 primary Indian soil types</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-amber-700 shrink-0" />
                  <span>Agronomic crop suitability matrix</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-amber-700 shrink-0" />
                  <span>Structural soil improvement & aeration tips</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-amber-700 shrink-0" />
                  <span>Honest visual guidance (No fabricated N-P-K chemical values)</span>
                </div>
              </div>
            </div>

            <Link
              to="/production/soil"
              className="w-full inline-flex items-center justify-center gap-2 py-3.5 px-4 rounded-xl bg-amber-800 hover:bg-amber-900 text-white font-bold text-sm shadow-md transition-colors"
            >
              Launch Soil Assessment
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* Pipeline Integrity Notice */}
        <div className="max-w-4xl mx-auto bg-agro-900 text-white p-6 rounded-3xl border border-agro-800 flex flex-col sm:flex-row items-center gap-5">
          <div className="w-12 h-12 rounded-2xl bg-green-500/20 text-green-400 flex items-center justify-center shrink-0">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div className="space-y-1 text-xs">
            <h4 className="font-bold text-sm text-green-300">Agricultural Relevance Safety Protocol</h4>
            <p className="text-gray-300 leading-relaxed">
              Every photograph is strictly validated against non-plant and non-agricultural objects (faces, selfies, pets, cars, furniture, screens). Only genuine plant and soil photographs are processed.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
