import React from 'react';
import { User } from '../types';
import { LogOut } from 'lucide-react';
import { Link } from 'react-router-dom';

interface ProfileProps {
  user: User;
  onLogout: () => void;
}

export const Profile: React.FC<ProfileProps> = ({ user, onLogout }) => {
  return (
    <div className="min-h-screen bg-[#fbfcf9] py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="bg-white rounded-3xl p-8 border border-gray-200 shadow-card space-y-6">
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
              <p className="text-sm font-bold text-gray-900">Local Auth Repository</p>
            </div>
          </div>

          <div className="pt-4 border-t border-gray-100 flex justify-between items-center">
            <Link
              to="/dashboard"
              className="text-xs font-bold text-green-700 hover:text-green-800"
            >
              ← Return to Dashboard
            </Link>

            <button
              onClick={onLogout}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-red-50 text-red-700 hover:bg-red-100 font-bold text-xs transition-colors"
            >
              <LogOut className="w-3.5 h-3.5" /> Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
