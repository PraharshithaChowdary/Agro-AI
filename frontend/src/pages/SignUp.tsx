import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sprout, Lock, Mail, User as UserIcon, ArrowRight, AlertCircle, Loader2, CheckCircle2 } from 'lucide-react';
import { authService } from '../services/authService';
import { User, UserRole } from '../types';

interface SignUpProps {
  onLoginSuccess: (user: User) => void;
}

export const SignUp: React.FC<SignUpProps> = ({ onLoginSuccess }) => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<UserRole>('farmer');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (role === 'admin') {
      setError('Public registration for Admin role is strictly restricted.');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    setLoading(true);
    try {
      const res = await authService.register(fullName, email, password, role);
      onLoginSuccess(res.user);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 agro-mesh-bg">
      <div className="max-w-lg w-full space-y-6 bg-white p-8 sm:p-10 rounded-3xl border border-gray-200 shadow-card">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-agro-900 text-green-400 mx-auto flex items-center justify-center shadow-md">
            <Sprout className="w-6 h-6" />
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-agro-950">Create AGRO AI Account</h2>
          <p className="text-xs text-gray-500">Join the smart agriculture and personalized nutrition ecosystem</p>
        </div>

        {error && (
          <div className="flex items-start gap-2.5 p-3.5 bg-red-50 border border-red-200 rounded-xl text-red-700 text-xs animate-in fade-in">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-1.5">
              Full Name
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                <UserIcon className="w-4 h-4" />
              </div>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="e.g. Maya Sharma"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm text-gray-900 placeholder-gray-400 transition-all outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-1.5">
              Email Address
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                <Mail className="w-4 h-4" />
              </div>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm text-gray-900 placeholder-gray-400 transition-all outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-1.5">
              Password
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                <Lock className="w-4 h-4" />
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="At least 6 characters"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm text-gray-900 placeholder-gray-400 transition-all outline-none"
              />
            </div>
          </div>

          {/* User Role Selection */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
              Select Your Primary Role
            </label>
            <div className="grid grid-cols-3 gap-2.5">
              <button
                type="button"
                onClick={() => setRole('farmer')}
                className={`p-3 rounded-xl border text-left flex flex-col justify-between transition-all ${
                  role === 'farmer'
                    ? 'border-green-600 bg-green-50/90 ring-2 ring-green-600 shadow-sm'
                    : 'border-gray-200 hover:border-gray-300 bg-gray-50/50'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-lg">🌱</span>
                  {role === 'farmer' && <CheckCircle2 className="w-4 h-4 text-green-600" />}
                </div>
                <div>
                  <p className="text-xs font-bold text-gray-900">Farmer</p>
                  <p className="text-[10px] text-gray-500">Crops & Soil</p>
                </div>
              </button>

              <button
                type="button"
                onClick={() => setRole('buyer')}
                className={`p-3 rounded-xl border text-left flex flex-col justify-between transition-all ${
                  role === 'buyer'
                    ? 'border-amber-600 bg-amber-50/90 ring-2 ring-amber-600 shadow-sm'
                    : 'border-gray-200 hover:border-gray-300 bg-gray-50/50'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-lg">🌾</span>
                  {role === 'buyer' && <CheckCircle2 className="w-4 h-4 text-amber-600" />}
                </div>
                <div>
                  <p className="text-xs font-bold text-gray-900">Buyer / Trader</p>
                  <p className="text-[10px] text-gray-500">Produce Sourcing</p>
                </div>
              </button>

              <button
                type="button"
                onClick={() => setRole('general')}
                className={`p-3 rounded-xl border text-left flex flex-col justify-between transition-all ${
                  role === 'general'
                    ? 'border-emerald-600 bg-emerald-50/90 ring-2 ring-emerald-600 shadow-sm'
                    : 'border-gray-200 hover:border-gray-300 bg-gray-50/50'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-lg">🥗</span>
                  {role === 'general' && <CheckCircle2 className="w-4 h-4 text-emerald-600" />}
                </div>
                <div>
                  <p className="text-xs font-bold text-gray-900">General User</p>
                  <p className="text-[10px] text-gray-500">Nutrition & Diet</p>
                </div>
              </button>
            </div>
            <p className="text-[11px] text-gray-400 mt-1.5 italic">
              * Note: Administrator accounts cannot be created via public signup.
            </p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-agro-900 hover:bg-agro-800 text-white font-bold text-sm shadow-md transition-all disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-green-400" />
                Creating Account...
              </>
            ) : (
              <>
                Complete Registration
                <ArrowRight className="w-4 h-4 text-green-400" />
              </>
            )}
          </button>
        </form>

        {/* Sign in link */}
        <div className="text-center text-xs text-gray-600">
          Already have an account?{' '}
          <Link to="/signin" className="text-green-700 font-bold hover:underline">
            Sign In Here
          </Link>
        </div>
      </div>
    </div>
  );
};
