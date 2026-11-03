import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { User } from '../types';
import { LogOut, Server, ArrowLeft, RefreshCw } from 'lucide-react';
import { getMobileApiBaseUrl } from '../services/api';
import { ServerConfigModal } from '../components/ServerConfigModal';

interface ProfileProps {
  user: User;
  onLogout: () => void;
}

export const Profile: React.FC<ProfileProps> = ({ user, onLogout }) => {
  const navigate = useNavigate();
  const [showServerModal, setShowServerModal] = useState(false);
  const [serverUrl, setServerUrl] = useState(getMobileApiBaseUrl());

  useEffect(() => {
    const handleUrlUpdate = () => {
      setServerUrl(getMobileApiBaseUrl());
    };
    window.addEventListener('agro_server_changed', handleUrlUpdate);
    return () => window.removeEventListener('agro_server_changed', handleUrlUpdate);
  }, []);

  const handleSignOut = () => {
    onLogout();
    navigate('/signin', { replace: true });
  };

  return (
    <div className="min-h-screen bg-[#fbfcf9] py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="bg-white rounded-3xl p-8 border border-gray-200 shadow-card space-y-6">
          {/* User Header */}
          <div className="flex items-center gap-4 pb-6 border-b border-gray-100">
            <div className="w-16 h-16 rounded-2xl bg-agro-900 text-green-400 flex items-center justify-center text-2xl font-bold uppercase shadow-md">
              {(user?.fullName || user?.email || 'U').charAt(0)}
            </div>
            <div>
              <h1 className="text-2xl font-extrabold text-agro-950">{user?.fullName || user?.email || 'User'}</h1>
              <p className="text-xs text-gray-500 font-medium">{user?.email}</p>
              <span className="inline-block mt-1 px-2.5 py-0.5 rounded-full bg-green-100 text-green-800 text-[11px] font-bold uppercase">
                {user?.role || 'farmer'} Account
              </span>
            </div>
          </div>

          {/* Details Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="p-4 rounded-2xl bg-gray-50 border border-gray-200 space-y-1">
              <span className="text-gray-400 font-bold uppercase">Full Name</span>
              <p className="text-sm font-bold text-gray-900">{user?.fullName || 'Not specified'}</p>
            </div>

            <div className="p-4 rounded-2xl bg-gray-50 border border-gray-200 space-y-1">
              <span className="text-gray-400 font-bold uppercase">Email Address</span>
              <p className="text-sm font-bold text-gray-900">{user.email}</p>
            </div>

            <div className="p-4 rounded-2xl bg-gray-50 border border-gray-200 space-y-1">
              <span className="text-gray-400 font-bold uppercase">Account Role</span>
              <p className="text-sm font-bold text-gray-900 capitalize">{user.role}</p>
            </div>

            <div className="p-4 rounded-2xl bg-gray-50 border border-gray-200 space-y-1">
              <span className="text-gray-400 font-bold uppercase">Security & Storage</span>
              <p className="text-sm font-bold text-gray-900">SQLite Database (agro_ai.db)</p>
            </div>
          </div>

          {/* Mobile Server Configuration Card */}
          <div className="p-4 rounded-2xl bg-gradient-to-r from-emerald-50/70 to-green-50/50 border border-emerald-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-agro-900 text-green-400 flex items-center justify-center shrink-0 shadow-sm">
                <Server className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs font-bold text-agro-950">Backend Server IP</p>
                <p className="text-[11px] font-mono text-gray-600 truncate max-w-xs">{serverUrl}</p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setShowServerModal(true)}
              className="inline-flex items-center justify-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-emerald-300 text-emerald-800 hover:bg-emerald-50 text-xs font-bold transition-all shadow-sm"
            >
              <RefreshCw className="w-3.5 h-3.5 text-emerald-600" /> Configure Server IP
            </button>
          </div>

          {/* Bottom Actions */}
          <div className="pt-4 border-t border-gray-100 flex justify-between items-center">
            <Link
              to="/dashboard"
              className="inline-flex items-center gap-1.5 text-xs font-bold text-green-700 hover:text-green-800"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Return to Dashboard
            </Link>

            <button
              onClick={handleSignOut}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-red-50 text-red-700 hover:bg-red-100 font-bold text-xs transition-colors"
            >
              <LogOut className="w-3.5 h-3.5" /> Sign Out
            </button>
          </div>
        </div>
      </div>

      <ServerConfigModal
        isOpen={showServerModal}
        onClose={() => setShowServerModal(false)}
        onSaved={(newUrl) => setServerUrl(newUrl)}
      />
    </div>
  );
};
