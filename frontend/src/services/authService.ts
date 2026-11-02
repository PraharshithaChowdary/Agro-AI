import { apiClient } from './api';
import { User, AuthResponse, UserRole } from '../types';

export interface IAuthRepository {
  login(email: string, password: string): Promise<AuthResponse>;
  register(fullName: string, email: string, password: string, role: UserRole): Promise<AuthResponse>;
  getCurrentUser(): Promise<User | null>;
  logout(): Promise<void>;
  resetPassword(email: string): Promise<{ success: boolean; message: string }>;
}

class BackendAuthRepository implements IAuthRepository {
  async login(email: string, password: string): Promise<AuthResponse> {
    try {
      const res = await apiClient.post<AuthResponse>('/auth/login', { email, password });
      if (res.data.token) {
        localStorage.setItem('agro_token', res.data.token);
        localStorage.setItem('agro_user', JSON.stringify(res.data.user));
      }
      return res.data;
    } catch (err: any) {
      // If backend is running and responds with error, propagate exact message
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      throw new Error(err.message || 'Login failed');
    }
  }

  async register(fullName: string, email: string, password: string, role: UserRole): Promise<AuthResponse> {
    if (role === 'admin') {
      throw new Error('Public registration for Admin role is not permitted.');
    }
    try {
      const res = await apiClient.post<AuthResponse>('/auth/signup', {
        fullName,
        email,
        password,
        role,
      });
      if (res.data.token) {
        localStorage.setItem('agro_token', res.data.token);
        localStorage.setItem('agro_user', JSON.stringify(res.data.user));
      }
      return res.data;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      throw new Error(err.message || 'Registration failed');
    }
  }

  async getCurrentUser(): Promise<User | null> {
    const cached = localStorage.getItem('agro_user');
    const token = localStorage.getItem('agro_token');
    if (!token || !cached) return null;

    try {
      const res = await apiClient.get<{ user: User }>('/auth/me');
      localStorage.setItem('agro_user', JSON.stringify(res.data.user));
      return res.data.user;
    } catch (err: any) {
      // A rejected/expired token is authoritative: do not revive a stale cached user.
      // Only permit cached identity for a temporary network outage.
      if (err.response?.status) {
        localStorage.removeItem('agro_token');
        localStorage.removeItem('agro_user');
        return null;
      }
      try {
        return JSON.parse(cached);
      } catch {
        return null;
      }
    }
  }

  async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/logout');
    } catch {
      // ignore
    } finally {
      localStorage.removeItem('agro_token');
      localStorage.removeItem('agro_user');
    }
  }

  async resetPassword(email: string): Promise<{ success: boolean; message: string }> {
    try {
      const res = await apiClient.post<{ message: string }>('/auth/forgot-password', { email });
      return { success: true, message: res.data.message || 'Reset instructions sent to your email.' };
    } catch (err: any) {
      return {
        success: true,
        message: `If an account exists for ${email}, password reset instructions have been generated.`,
      };
    }
  }
}

export const authService = new BackendAuthRepository();
