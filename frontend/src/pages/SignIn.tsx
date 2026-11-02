import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sprout, Lock, Mail, ArrowRight, AlertCircle, Loader2 } from 'lucide-react';
import { authService } from '../services/authService';
import { User } from '../types';

interface SignInProps {
  onLoginSuccess: (user: User) => void;
}

export const SignIn: React.FC<SignInProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await authService.login(email, password);
      onLoginSuccess(res.user);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Invalid credentials. Please check and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 agro-mesh-bg">
      <div className="max-w-md w-full space-y-6 bg-white p-8 sm:p-10 rounded-3xl border border-gray-200 shadow-card">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-agro-900 text-green-400 mx-auto flex items-center justify-center shadow-md">
            <Sprout className="w-6 h-6" />
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-agro-950">Welcome Back</h2>
          <p className="text-xs text-gray-500">Sign in to your AGRO AI dashboard</p>
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
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-bold uppercase tracking-wider text-gray-700">Password</label>
              <Link to="/forgot-password" className="text-xs text-green-700 hover:text-green-800 font-semibold">
                Forgot password?
              </Link>
            </div>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                <Lock className="w-4 h-4" />
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm text-gray-900 placeholder-gray-400 transition-all outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-agro-900 hover:bg-agro-800 text-white font-bold text-sm shadow-md transition-all disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-green-400" />
                Signing In...
              </>
            ) : (
              <>
                Sign In to AGRO AI
                <ArrowRight className="w-4 h-4 text-green-400" />
              </>
            )}
          </button>
        </form>

        {/* Sign up prompt */}
        <div className="pt-2 border-t border-gray-100 text-center text-xs text-gray-600">
          Don't have an account?{' '}
          <Link to="/signup" className="text-green-700 font-bold hover:underline">
            Create Free Account
          </Link>
        </div>
      </div>
    </div>
  );
};
