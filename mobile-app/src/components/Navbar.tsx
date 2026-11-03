import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
  Sprout,
  HeartPulse,
  BotMessageSquare,
  LayoutDashboard,
  LogOut,
  Menu,
  X,
  ChevronDown,
  Sparkles,
  Server,
} from 'lucide-react';
import { User } from '../types';
import { getMobileApiBaseUrl } from '../services/api';
import { ServerConfigModal } from './ServerConfigModal';

interface NavbarProps {
  user: User | null;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ user, onLogout }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [productionDropdown, setProductionDropdown] = useState(false);
  const [showServerModal, setShowServerModal] = useState(false);
  const [serverUrl, setServerUrl] = useState(getMobileApiBaseUrl());
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const handleUrlUpdate = () => {
      setServerUrl(getMobileApiBaseUrl());
    };
    window.addEventListener('agro_server_changed', handleUrlUpdate);
    return () => window.removeEventListener('agro_server_changed', handleUrlUpdate);
  }, []);

  const isActive = (path: string) => location.pathname === path || location.pathname.startsWith(path + '/');

  return (
    <>
      <nav className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            {/* Logo & Tagline */}
            <div className="flex items-center">
              <Link to={user ? "/dashboard" : "/"} className="flex items-center gap-2.5 group">
                <div className="w-10 h-10 rounded-xl bg-agro-900 flex items-center justify-center text-agro-400 group-hover:bg-agro-800 transition-all shadow-md">
                  <Sprout className="w-6 h-6 text-green-400" />
                </div>
                <div className="flex flex-col">
                  <div className="flex items-center gap-1.5">
                    <span className="font-extrabold text-xl tracking-tight text-agro-950">AGRO</span>
                    <span className="font-extrabold text-xl tracking-tight text-green-600">AI</span>
                  </div>
                  <span className="text-[10px] text-gray-700 font-medium tracking-wide hidden sm:inline-block">
                    Smart Agriculture. Healthy Lives.
                  </span>
                </div>
              </Link>
            </div>

            {/* Desktop Navigation */}
            {user ? (
              <div className="hidden md:flex items-center gap-1 lg:gap-2">
                <Link
                  to="/dashboard"
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold transition-all ${
                    isActive('/dashboard')
                      ? 'text-agro-900 bg-agro-100 font-bold'
                      : 'text-gray-700 hover:text-agro-900 hover:bg-gray-100'
                  }`}
                >
                  <LayoutDashboard className="w-4 h-4 text-agro-700" />
                  Dashboard
                </Link>

                <Link
                  to="/plants"
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold transition-all ${
                    isActive('/plants')
                      ? 'text-agro-900 bg-agro-100 font-bold'
                      : 'text-gray-700 hover:text-agro-900 hover:bg-gray-100'
                  }`}
                >
                  <Sparkles className="w-4 h-4 text-emerald-600" />
                  Plant Analysis
                </Link>

                {/* Better Production Dropdown */}
                <div className="relative" onMouseLeave={() => setProductionDropdown(false)}>
                  <button
                    onClick={() => setProductionDropdown(!productionDropdown)}
                    onMouseEnter={() => setProductionDropdown(true)}
                    className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold transition-all ${
                      isActive('/production')
                        ? 'text-agro-900 bg-agro-100 font-bold'
                        : 'text-gray-700 hover:text-agro-900 hover:bg-gray-100'
                    }`}
                  >
                    <Sprout className="w-4 h-4 text-green-600" />
                    Better Production
                    <ChevronDown className="w-3.5 h-3.5 text-gray-500" />
                  </button>

                  {productionDropdown && (
                    <div
                      onMouseEnter={() => setProductionDropdown(true)}
                      className="absolute left-0 mt-1 w-72 rounded-xl bg-white shadow-xl border border-gray-100 py-2 z-50 animate-in fade-in slide-in-from-top-2"
                    >
                      <Link
                        to="/plants"
                        onClick={() => setProductionDropdown(false)}
                        className="flex flex-col px-4 py-2.5 hover:bg-emerald-50 text-sm text-gray-800 border-b border-gray-100"
                      >
                        <span className="font-bold text-emerald-950 flex items-center gap-1.5">
                          <span className="w-2 h-2 rounded-full bg-emerald-600"></span>
                          Plant Analysis & Identification
                        </span>
                        <span className="text-xs text-gray-500 mt-0.5">Photo identification, health status & 5 care suggestions</span>
                      </Link>
                      <Link
                        to="/production/soil"
                        onClick={() => setProductionDropdown(false)}
                        className="flex flex-col px-4 py-2.5 hover:bg-amber-50 text-sm text-gray-800"
                      >
                        <span className="font-bold text-agro-950 flex items-center gap-1.5">
                          <span className="w-2 h-2 rounded-full bg-amber-600"></span>
                          Soil Assessment
                        </span>
                        <span className="text-xs text-gray-500 mt-0.5">Visual category & crop suitability</span>
                      </Link>
                    </div>
                  )}
                </div>

                {/* Better Nutrition */}
                <Link
                  to="/nutrition"
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold transition-all ${
                    isActive('/nutrition')
                      ? 'text-agro-900 bg-agro-100 font-bold'
                      : 'text-gray-700 hover:text-agro-900 hover:bg-gray-100'
                  }`}
                >
                  <HeartPulse className="w-4 h-4 text-emerald-600" />
                  Better Nutrition
                </Link>

                {/* AGRO AI Assistant */}
                <Link
                  to="/assistant"
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold transition-all ${
                    isActive('/assistant')
                      ? 'text-agro-900 bg-agro-100 font-bold'
                      : 'text-gray-700 hover:text-agro-900 hover:bg-gray-100'
                  }`}
                >
                  <BotMessageSquare className="w-4 h-4 text-indigo-600" />
                  AGRO AI Assistant
                </Link>
              </div>
            ) : (
              <div className="hidden md:flex items-center gap-4">
                <Link
                  to="/signin"
                  className="text-sm font-semibold text-gray-700 hover:text-agro-900 px-3 py-2 rounded-lg"
                >
                  Sign In
                </Link>
                <Link
                  to="/signup"
                  className="text-sm font-semibold bg-agro-800 hover:bg-agro-900 text-white px-4 py-2 rounded-lg shadow-sm transition-all"
                >
                  Get Started
                </Link>
              </div>
            )}

            {/* Desktop Server IP & User Profile */}
            <div className="hidden md:flex items-center gap-3">
              <button
                type="button"
                onClick={() => setShowServerModal(true)}
                title={`Configured Backend: ${serverUrl}`}
                className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold text-gray-600 hover:text-green-800 hover:bg-green-50 border border-gray-200 transition-all"
              >
                <Server className="w-3.5 h-3.5 text-green-600" />
                <span>Server IP</span>
              </button>

              {user && (
                <>
                  <Link
                    to="/profile"
                    className="flex items-center gap-2 py-1 px-2.5 rounded-full bg-gray-50 hover:bg-gray-100 border border-gray-200 transition-colors"
                  >
                    <div className="w-7 h-7 rounded-full bg-agro-700 text-white flex items-center justify-center text-xs font-bold uppercase">
                      {(user.fullName || user.email || 'U').charAt(0)}
                    </div>
                    <div className="flex flex-col text-left">
                      <span className="text-xs font-bold text-gray-800 leading-none">
                        {(user.fullName || user.email || 'User').split(' ')[0]}
                      </span>
                      <span className="text-[10px] uppercase font-semibold tracking-wider text-agro-700 leading-tight">
                        {user.role || 'farmer'}
                      </span>
                    </div>
                  </Link>

                  <button
                    onClick={() => {
                      onLogout();
                      navigate('/signin');
                    }}
                    title="Sign Out"
                    className="p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50 transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                  </button>
                </>
              )}
            </div>

            {/* Mobile Header Icons: Server Config & Hamburger */}
            <div className="flex items-center md:hidden gap-1">
              <button
                type="button"
                onClick={() => setShowServerModal(true)}
                title="Server Configuration"
                className="p-2 rounded-lg text-gray-600 hover:text-green-700 hover:bg-gray-100 transition-colors"
              >
                <Server className="w-5 h-5 text-green-700" />
              </button>
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
              >
                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-200 bg-white px-4 pt-2 pb-6 space-y-2">
            {user ? (
              <>
                <div className="py-2 border-b border-gray-100 flex items-center justify-between">
                  <div>
                    <p className="text-sm font-bold text-gray-800">{user.fullName || user.email || 'User'}</p>
                    <p className="text-xs text-agro-700 capitalize font-medium">{user.role || 'farmer'} Account</p>
                  </div>
                  <Link
                    to="/profile"
                    onClick={() => setMobileMenuOpen(false)}
                    className="text-xs bg-gray-100 text-gray-700 px-2.5 py-1 rounded"
                  >
                    Profile
                  </Link>
                </div>

                <Link
                  to="/dashboard"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  <LayoutDashboard className="w-5 h-5 text-agro-700" />
                  Dashboard
                </Link>

                <Link
                  to="/plants"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-emerald-800 bg-emerald-50/70 hover:bg-emerald-50"
                >
                  <Sparkles className="w-5 h-5 text-emerald-600" />
                  Plant Analysis
                </Link>

                <div className="pl-2 space-y-1">
                  <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider px-2">
                    Better Production
                  </span>
                  <Link
                    to="/plants"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-emerald-800 bg-emerald-50/50 hover:bg-emerald-50"
                  >
                    <Sparkles className="w-4 h-4 text-emerald-600" />
                    Plant Analysis & Identification
                  </Link>
                  <Link
                    to="/production/soil"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
                  >
                    <span className="w-4 h-4 rounded-full bg-amber-600 flex items-center justify-center text-[9px] text-white font-bold">
                      S
                    </span>
                    Soil Assessment
                  </Link>
                </div>

                <Link
                  to="/nutrition"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  <HeartPulse className="w-5 h-5 text-emerald-600" />
                  Better Nutrition
                </Link>

                <Link
                  to="/assistant"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  <BotMessageSquare className="w-5 h-5 text-indigo-600" />
                  AGRO AI Assistant
                </Link>

                {/* Mobile Menu Server Config Button */}
                <button
                  type="button"
                  onClick={() => {
                    setMobileMenuOpen(false);
                    setShowServerModal(true);
                  }}
                  className="w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold text-gray-700 bg-gray-50 hover:bg-gray-100 border border-gray-200 transition-all mt-1"
                >
                  <div className="flex items-center gap-2">
                    <Server className="w-4 h-4 text-green-600" />
                    <span>Server Configuration</span>
                  </div>
                  <span className="text-[10px] font-mono text-gray-500 truncate max-w-[130px]">{serverUrl}</span>
                </button>

                <div className="pt-3 border-t border-gray-100">
                  <button
                    onClick={() => {
                      onLogout();
                      setMobileMenuOpen(false);
                      navigate('/signin');
                    }}
                    className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100"
                  >
                    <LogOut className="w-4 h-4" />
                    Sign Out
                  </button>
                </div>
              </>
            ) : (
              <div className="space-y-2 pt-2">
                <Link
                  to="/signin"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block text-center w-full py-2.5 text-sm font-medium text-gray-700 bg-gray-50 rounded-lg"
                >
                  Sign In
                </Link>
                <Link
                  to="/signup"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block text-center w-full py-2.5 text-sm font-medium text-white bg-agro-800 rounded-lg"
                >
                  Create Account
                </Link>

                {/* Mobile Menu Server Config Button (Public) */}
                <button
                  type="button"
                  onClick={() => {
                    setMobileMenuOpen(false);
                    setShowServerModal(true);
                  }}
                  className="w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold text-gray-700 bg-gray-50 hover:bg-gray-100 border border-gray-200 transition-all mt-2"
                >
                  <div className="flex items-center gap-2">
                    <Server className="w-4 h-4 text-green-600" />
                    <span>Server Configuration</span>
                  </div>
                  <span className="text-[10px] font-mono text-gray-500 truncate max-w-[130px]">{serverUrl}</span>
                </button>
              </div>
            )}
          </div>
        )}
      </nav>

      <ServerConfigModal
        isOpen={showServerModal}
        onClose={() => setShowServerModal(false)}
        onSaved={(newUrl) => setServerUrl(newUrl)}
      />
    </>
  );
};
