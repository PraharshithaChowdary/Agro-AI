import React from 'react';
import { Sprout, ShieldCheck, Heart, Leaf } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-agro-950 text-gray-300 border-t border-agro-900 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Col */}
          <div className="md:col-span-2 space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-agro-800 flex items-center justify-center text-green-400">
                <Sprout className="w-5 h-5" />
              </div>
              <span className="text-xl font-bold text-white tracking-tight">AGRO <span className="text-green-400">AI</span></span>
            </div>
            <p className="text-sm text-agro-200/80 font-medium">
              Smart Agriculture. Healthy Lives. Better Future.
            </p>
            <p className="text-xs text-gray-400 max-w-md leading-relaxed">
              Empowering farmers, buyers, and consumers with local AI-driven crop & soil diagnostics, scientifically validated personalized nutrition planning, and instant agricultural knowledge.
            </p>
          </div>

          {/* Three Pillars */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-green-400 mb-3">Core Capabilities</h4>
            <ul className="space-y-2 text-xs text-gray-300">
              <li>
                <Link to="/production/crop" className="hover:text-white transition-colors flex items-center gap-1.5">
                  <Leaf className="w-3.5 h-3.5 text-green-400" />
                  Better Production — Crop
                </Link>
              </li>
              <li>
                <Link to="/production/soil" className="hover:text-white transition-colors flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                  Better Production — Soil
                </Link>
              </li>
              <li>
                <Link to="/nutrition" className="hover:text-white transition-colors flex items-center gap-1.5">
                  <Heart className="w-3.5 h-3.5 text-emerald-400" />
                  Better Nutrition — 7-Day Plan
                </Link>
              </li>
              <li>
                <Link to="/assistant" className="hover:text-white transition-colors flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
                  AGRO AI Assistant
                </Link>
              </li>
            </ul>
          </div>

          {/* Compliance & Notice */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-green-400 mb-3">Integrity & Safety</h4>
            <div className="bg-agro-900/60 p-3 rounded-xl border border-agro-800/80 space-y-2">
              <div className="flex items-center gap-1.5 text-xs text-green-300 font-semibold">
                <ShieldCheck className="w-4 h-4 text-green-400" />
                Local & Private
              </div>
              <p className="text-[11px] text-gray-300 leading-normal">
                Visual assessments are recommendations. For precise chemical diagnosis, verify via accredited soil labs. Nutrition plans provide general wellness guidance.
              </p>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-agro-900/80 flex flex-col sm:flex-row items-center justify-between text-xs text-gray-500 gap-4">
          <p>© {new Date().getFullYear()} AGRO AI. All rights reserved.</p>
          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1 text-green-400 bg-agro-900/80 px-2.5 py-1 rounded-full text-[11px]">
              <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"></span>
              Zero External Paid AI APIs
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
