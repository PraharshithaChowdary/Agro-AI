import React from 'react';
import { Link } from 'react-router-dom';
import {
  Sprout,
  HeartPulse,
  BotMessageSquare,
  ShieldCheck,
  CheckCircle2,
  ArrowRight,
  Sparkles,
  Cpu,
  Layers,
  Activity,
  Zap,
} from 'lucide-react';

export const Welcome: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen bg-[#fbfcf9]">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-28 agro-mesh-bg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            {/* Pill Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-green-100/90 text-agro-900 border border-green-300 shadow-sm text-xs font-bold uppercase tracking-wider animate-in fade-in">
              <Sparkles className="w-3.5 h-3.5 text-green-600" />
              Next-Gen AgriTech & Wellness Intelligence
            </div>

            {/* Main Headline */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-agro-950 tracking-tight leading-[1.15]">
              Smart Agriculture. <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-emerald-500">
                Healthy Lives.
              </span>{' '}
              Better Future.
            </h1>

            {/* Subheading */}
            <p className="text-lg sm:text-xl text-gray-600 leading-relaxed font-normal">
              Empowering farmers with local AI crop disease & soil diagnostics, guiding individuals with
              scientific 7-day personalized nutrition plans, and delivering instantaneous offline agricultural answers.
            </p>

            {/* CTAs */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link
                to="/signup"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-xl bg-agro-900 hover:bg-agro-800 text-white font-bold text-base shadow-lg shadow-green-950/20 transition-all hover:scale-[1.02]"
              >
                Launch AGRO AI Platform
                <ArrowRight className="w-5 h-5 text-green-400" />
              </Link>
              <Link
                to="/signin"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-white hover:bg-gray-50 text-gray-800 font-semibold text-base border border-gray-300 shadow-sm transition-all"
              >
                Existing User Sign In
              </Link>
            </div>

            {/* Trust Badges */}
            <div className="pt-6 flex flex-wrap items-center justify-center gap-6 text-xs text-gray-600 font-semibold">
              <div className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-green-600" />
                Zero Paid API Keys Required
              </div>
              <div className="flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-green-600" />
                Local ML Inference
              </div>
              <div className="flex items-center gap-1.5">
                <Cpu className="w-4 h-4 text-green-600" />
                Evidence-Based Diet Planner
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* THREE CORE PILLARS SECTION */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16 space-y-3">
            <h2 className="text-xs font-bold uppercase tracking-widest text-green-700">Three Dedicated Pillars</h2>
            <p className="text-3xl sm:text-4xl font-extrabold text-agro-950">
              Complete Agricultural & Nutritional Ecosystem
            </p>
            <p className="text-sm text-gray-500">
              Engineered with zero fluff. Only three robust, production-grade features built for real utility.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Pillar 1: Better Production */}
            <div className="relative group rounded-3xl p-8 bg-[#fafcf9] border border-green-200/80 hover:border-green-500 shadow-soft hover:shadow-card transition-all duration-300 flex flex-col">
              <div className="w-14 h-14 rounded-2xl bg-green-100 text-green-800 flex items-center justify-center mb-6 shadow-sm group-hover:scale-110 transition-transform">
                <Sprout className="w-7 h-7 text-green-700" />
              </div>

              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-bold tracking-wide text-green-800 bg-green-50 px-3 py-1 rounded-full border border-green-200 flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-green-600" />
                  Visual Diagnostics
                </span>
              </div>

              <h3 className="text-2xl font-bold text-agro-950 mb-3">Better Production</h3>
              <p className="text-sm text-gray-600 leading-relaxed mb-6">
                Automated plant health inspection, leaf & stem condition diagnosis, and visual soil classification powered by local lightweight CNN models with intelligent agricultural relevance verification.
              </p>

              <ul className="space-y-2.5 text-xs text-gray-700 font-medium mb-8 mt-auto">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-green-600 shrink-0" />
                  Plant health & foliar symptom extraction (leaves, stems, flowers)
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-green-600 shrink-0" />
                  Visual soil classification & crop suitability
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-green-600 shrink-0" />
                  Automatic non-agricultural image rejection
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-green-600 shrink-0" />
                  Crisp, actionable agronomic recommendations
                </li>
              </ul>

              <Link
                to="/plants"
                className="w-full inline-flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-green-700 hover:bg-green-800 text-white font-bold text-sm shadow-md transition-colors"
              >
                Launch Plant / Soil Analysis
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {/* Pillar 2: Better Nutrition */}
            <div className="relative group rounded-3xl p-8 bg-[#fafcf9] border border-emerald-200/80 hover:border-emerald-500 shadow-soft hover:shadow-card transition-all duration-300 flex flex-col">
              <div className="w-14 h-14 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center mb-6 shadow-sm group-hover:scale-110 transition-transform">
                <HeartPulse className="w-7 h-7 text-emerald-700" />
              </div>

              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-bold tracking-wide text-emerald-800 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-emerald-600" />
                  Diet Planning
                </span>
              </div>

              <h3 className="text-2xl font-bold text-agro-950 mb-3">Better Nutrition</h3>
              <p className="text-sm text-gray-600 leading-relaxed mb-6">
                Personalized BMR & TDEE metabolic calculation and complete 7-day meal planning built from a structured nutritional food database respecting allergies and cuisine preferences.
              </p>

              <ul className="space-y-2.5 text-xs text-gray-700 font-medium mb-8 mt-auto">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  Harris-Benedict / Mifflin-St Jeor BMR formulas
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  Full 7-day schedule (5 meals per day)
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  Accurate per-meal calorie & protein breakdown
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  Strict allergy exclusion & diet preference match
                </li>
              </ul>

              <Link
                to="/nutrition"
                className="w-full inline-flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm shadow-md transition-colors"
              >
                Generate 7-Day Diet Plan
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {/* Pillar 3: AGRO AI Assistant */}
            <div className="relative group rounded-3xl p-8 bg-[#fafcf9] border border-indigo-200/80 hover:border-indigo-500 shadow-soft hover:shadow-card transition-all duration-300 flex flex-col">
              <div className="w-14 h-14 rounded-2xl bg-indigo-100 text-indigo-800 flex items-center justify-center mb-6 shadow-sm group-hover:scale-110 transition-transform">
                <BotMessageSquare className="w-7 h-7 text-indigo-700" />
              </div>

              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-bold tracking-wide text-indigo-800 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-200 flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-indigo-600" />
                  Offline Assistant
                </span>
              </div>

              <h3 className="text-2xl font-bold text-agro-950 mb-3">AGRO AI Assistant</h3>
              <p className="text-sm text-gray-600 leading-relaxed mb-6">
                Agriculture-focused assistant for crop care, soil health, farming practices, and nutrition. Answers depend on the configured backend and available knowledge sources.
              </p>

              <ul className="space-y-2.5 text-xs text-gray-700 font-medium mb-8 mt-auto">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-indigo-600 shrink-0" />
                  Instant answers on crop diseases & remedies
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-indigo-600 shrink-0" />
                  Soil management & fertilizer recommendations
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-indigo-600 shrink-0" />
                  Nutrition and calorie counting counseling
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-indigo-600 shrink-0" />
                  Account-scoped history when signed in
                </li>
              </ul>

              <Link
                to="/assistant"
                className="w-full inline-flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-indigo-700 hover:bg-indigo-800 text-white font-bold text-sm shadow-md transition-colors"
              >
                Chat with Assistant
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ARCHITECTURE HIGHLIGHTS */}
      <section className="py-16 bg-[#f4f7f2] border-y border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 text-center">
            <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-2">
              <Zap className="w-6 h-6 text-green-600 mx-auto" />
              <p className="text-2xl font-extrabold text-agro-950">Local-first</p>
              <p className="text-xs text-gray-500">Runtime depends on the selected model and configured services</p>
            </div>
            <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-2">
              <Activity className="w-6 h-6 text-emerald-600 mx-auto" />
              <p className="text-2xl font-extrabold text-agro-950">MobileNetV2</p>
              <p className="text-xs text-gray-500">Lightweight CNN transfer learning for edge & local inference</p>
            </div>
            <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-2">
              <Layers className="w-6 h-6 text-amber-600 mx-auto" />
              <p className="text-2xl font-extrabold text-agro-950">5 Meal / Day</p>
              <p className="text-xs text-gray-500">Structured macro balance for all 7 days of the week</p>
            </div>
            <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-2">
              <ShieldCheck className="w-6 h-6 text-indigo-600 mx-auto" />
              <p className="text-2xl font-extrabold text-agro-950">Relevance Filter</p>
              <p className="text-xs text-gray-500">Rejects non-farming photos before diagnosis</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
