import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Server, Wifi, CheckCircle2, AlertCircle, Loader2, X, RefreshCw } from 'lucide-react';
import { getMobileApiBaseUrl, setMobileBackendUrl } from '../services/api';

interface ServerConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSaved?: (newUrl: string) => void;
}

export const formatServerUrl = (input: string): string => {
  let val = input.trim();
  if (!val) {
    return 'http://192.168.1.29:8000/api';
  }

  // Remove trailing slashes
  val = val.replace(/\/+$/, '');

  // Add http:// if scheme missing
  if (!/^https?:\/\//i.test(val)) {
    val = 'http://' + val;
  }

  // Parse URL to verify structure
  try {
    const parsed = new URL(val);
    // If no port specified and host looks like IP, default port 8000
    if (!parsed.port && !parsed.hostname.includes('.com') && !parsed.hostname.includes('.org')) {
      parsed.port = '8000';
    }
    // Ensure path ends with /api
    let pathname = parsed.pathname.replace(/\/+$/, '');
    if (!pathname.endsWith('/api')) {
      if (pathname === '' || pathname === '/') {
        pathname = '/api';
      } else {
        pathname = pathname + '/api';
      }
    }
    return `${parsed.protocol}//${parsed.hostname}${parsed.port ? ':' + parsed.port : ''}${pathname}`;
  } catch {
    if (!val.endsWith('/api')) {
      val += '/api';
    }
    return val;
  }
};

export const ServerConfigModal: React.FC<ServerConfigModalProps> = ({ isOpen, onClose, onSaved }) => {
  const [urlInput, setUrlInput] = useState('');
  const [testing, setTesting] = useState(false);
  const [testStatus, setTestStatus] = useState<{
    success: boolean;
    message: string;
    responseTime?: number;
  } | null>(null);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setUrlInput(getMobileApiBaseUrl());
      setTestStatus(null);
      setSavedSuccess(false);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleTestConnection = async () => {
    const formatted = formatServerUrl(urlInput);
    setTesting(true);
    setTestStatus(null);
    const startTime = Date.now();

    try {
      // Test the /health endpoint directly
      const healthEndpoint = formatted.endsWith('/api')
        ? `${formatted}/health`
        : `${formatted.replace(/\/+$/, '')}/api/health`;

      const response = await axios.get(healthEndpoint, { timeout: 6000 });
      const duration = Date.now() - startTime;

      if (response.status === 200 && response.data?.status === 'healthy') {
        setTestStatus({
          success: true,
          message: `Connected successfully! AGRO AI backend is online and responding.`,
          responseTime: duration,
        });
      } else {
        setTestStatus({
          success: true,
          message: `Server responded with status ${response.status}.`,
          responseTime: duration,
        });
      }
    } catch (err: any) {
      const duration = Date.now() - startTime;
      let errMsg = 'Could not reach server.';
      if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
        errMsg = 'Connection timed out. Check that your laptop and mobile device are on the same Wi-Fi network.';
      } else if (err.response?.status) {
        errMsg = `Server returned HTTP status ${err.response.status}.`;
      } else if (err.message) {
        errMsg = `Connection error: ${err.message}`;
      }
      setTestStatus({
        success: false,
        message: `${errMsg} Ensure FastAPI is running on host port 8000.`,
        responseTime: duration,
      });
    } finally {
      setTesting(false);
    }
  };

  const handleSave = () => {
    const formatted = formatServerUrl(urlInput);
    setMobileBackendUrl(formatted);
    window.dispatchEvent(new CustomEvent('agro_server_changed', { detail: formatted }));
    setSavedSuccess(true);
    if (onSaved) onSaved(formatted);
    setTimeout(() => {
      onClose();
    }, 600);
  };

  const handlePreset = (presetUrl: string) => {
    setUrlInput(presetUrl);
    setTestStatus(null);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-7 shadow-2xl border border-gray-200 space-y-5">
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-gray-100">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-agro-900 text-green-400 flex items-center justify-center shadow-sm">
              <Server className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-extrabold text-gray-900 text-base">Server Configuration</h3>
              <p className="text-[11px] text-gray-500 font-medium">Laptop Backend Connection Settings</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Input */}
        <div className="space-y-2">
          <label className="block text-xs font-bold uppercase tracking-wider text-gray-700">
            Backend API Base URL
          </label>
          <div className="relative">
            <input
              type="text"
              value={urlInput}
              onChange={(e) => {
                setUrlInput(e.target.value);
                setTestStatus(null);
                setSavedSuccess(false);
              }}
              placeholder="http://192.168.1.29:8000/api"
              className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-green-500 text-xs font-mono text-gray-900 placeholder-gray-400 outline-none transition-all"
            />
          </div>
          <p className="text-[11px] text-gray-500">
            Enter your laptop's Wi-Fi IPv4 address (e.g. <span className="font-mono text-green-700 font-bold">192.168.1.29</span> or <span className="font-mono text-green-700 font-bold">http://192.168.1.29:8000/api</span>).
          </p>
        </div>

        {/* Presets */}
        <div className="space-y-1.5">
          <span className="text-[10px] font-bold uppercase tracking-wider text-gray-400">Quick Presets:</span>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => handlePreset('http://192.168.1.29:8000/api')}
              className="px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-gray-100 hover:bg-green-50 hover:text-green-800 text-gray-700 border border-gray-200 transition-colors flex items-center gap-1"
            >
              <Wifi className="w-3 h-3 text-green-600" /> Laptop Wi-Fi (192.168.1.29)
            </button>
            <button
              type="button"
              onClick={() => handlePreset('http://10.0.2.2:8000/api')}
              className="px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-gray-100 hover:bg-gray-200 text-gray-700 border border-gray-200 transition-colors"
            >
              Android Emulator (10.0.2.2)
            </button>
          </div>
        </div>

        {/* Test Result Message */}
        {testStatus && (
          <div
            className={`p-3 rounded-xl border text-xs flex items-start gap-2.5 animate-in fade-in ${
              testStatus.success
                ? 'bg-green-50 border-green-200 text-green-800'
                : 'bg-red-50 border-red-200 text-red-700'
            }`}
          >
            {testStatus.success ? (
              <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5 text-green-600" />
            ) : (
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-red-600" />
            )}
            <div>
              <p className="font-bold">{testStatus.message}</p>
              {testStatus.responseTime !== undefined && (
                <p className="text-[10px] opacity-80 mt-0.5">Response time: {testStatus.responseTime}ms</p>
              )}
            </div>
          </div>
        )}

        {savedSuccess && (
          <div className="p-2.5 bg-green-100 text-green-800 rounded-xl text-xs font-bold text-center flex items-center justify-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-green-700" /> Server URL updated successfully!
          </div>
        )}

        {/* Actions */}
        <div className="pt-2 flex items-center justify-between gap-3 border-t border-gray-100">
          <button
            type="button"
            disabled={testing}
            onClick={handleTestConnection}
            className="flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl border border-gray-300 hover:bg-gray-50 text-gray-700 text-xs font-bold transition-all disabled:opacity-50"
          >
            {testing ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin text-green-600" />
                Testing...
              </>
            ) : (
              <>
                <RefreshCw className="w-3.5 h-3.5 text-gray-500" />
                Test Connection
              </>
            )}
          </button>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-3.5 py-2.5 rounded-xl text-xs font-semibold text-gray-600 hover:bg-gray-100 transition-colors"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleSave}
              className="px-4 py-2.5 rounded-xl bg-agro-900 hover:bg-agro-800 text-white text-xs font-bold shadow-md transition-all"
            >
              Save & Apply
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

