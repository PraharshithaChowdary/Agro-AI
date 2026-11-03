import axios from 'axios';

/**
 * AGRO AI Mobile API Client
 * Connects directly to the shared FastAPI backend running on the host machine.
 */
export const getMobileApiBaseUrl = (): string => {
  // 1. Check custom URL if saved by user
  const savedUrl = localStorage.getItem('agro_api_url');
  if (savedUrl) return savedUrl;

  // 2. Check environment variable
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }

  // 3. Default to host LAN IP (fallback to 10.0.2.2 for Android emulator)
  return 'http://192.168.1.29:8000/api';
};

export const setMobileBackendUrl = (url: string) => {
  localStorage.setItem('agro_api_url', url.trim());
};

export const apiClient = axios.create({
  baseURL: getMobileApiBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000,
});

// Request interceptor to attach JWT token and ensure latest baseURL
apiClient.interceptors.request.use(
  (config) => {
    config.baseURL = getMobileApiBaseUrl();
    const token = localStorage.getItem('agro_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle unauthenticated responses
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('agro_token');
      localStorage.removeItem('agro_user');
    }
    return Promise.reject(error);
  }
);
