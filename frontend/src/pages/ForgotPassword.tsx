import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Sprout, Mail, ArrowLeft, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { authService } from '../services/authService';

export const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    setLoading(true);

    try {
      const res = await authService.resetPassword(email);
      setMessage(res.message);
    } catch (err: any) {
      setError(err.message || 'Failed to send reset link.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 agro-mesh-bg">
      <div className="max-w-md w-full space-y-6 bg-white p-8 sm:p-10 rounded-3xl border border-gray-200 shadow-card">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-agro-900 text-green-400 mx-auto flex items-center justify-center shadow-md">
            <Sprout className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-extrabold text-agro-950">Password Recovery</h2>
          <p className="text-xs text-gray-500">
            Enter your registered email and we'll send password recovery guidance.
          </p>
        </div>

        {message && (
          <div className="flex items-start gap-2.5 p-3.5 bg-green-50 border border-green-200 rounded-xl text-green-800 text-xs">
            <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5 text-green-600" />
            <span>{message}</span>
          </div>
        )}

        {error && (
          <div className="flex items-start gap-2.5 p-3.5 bg-red-50 border border-red-200 rounded-xl text-red-700 text-xs">
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

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-agro-900 hover:bg-agro-800 text-white font-bold text-sm shadow-md transition-all disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-green-400" />
                Sending Recovery Email...
              </>
            ) : (
              'Send Recovery Link'
            )}
          </button>
        </form>

        <div className="text-center">
          <Link
            to="/signin"
            className="inline-flex items-center gap-1.5 text-xs text-gray-600 hover:text-agro-950 font-semibold"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Sign In
          </Link>
        </div>
      </div>
    </div>
  );
};
