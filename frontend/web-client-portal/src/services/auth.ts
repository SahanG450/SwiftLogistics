import { api } from './api';

/**
 * Authentication Service
 * Handles user authentication, token management, and session persistence
 */

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'client' | 'admin';
}

export interface LoginResponse {
  token: string;
  user: User;
}

/**
 * Login user with email and password
 */
export const login = async (email: string, password: string): Promise<LoginResponse> => {
  try {
    const response = await api.auth.login(email, password);
    const { token, user } = response.data;
    
    // Store token and user in localStorage
    localStorage.setItem('authToken', token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return { token, user };
  } catch (error: any) {
    console.error('[Auth] Login failed:', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Login failed. Please check your credentials.');
  }
};

/**
 * Logout user and clear session
 */
export const logout = async (): Promise<void> => {
  try {
    await api.auth.logout();
  } catch (error) {
    console.error('[Auth] Logout failed:', error);
  } finally {
    // Always clear local storage
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  }
};

/**
 * Get current user from localStorage
 */
export const getCurrentUser = (): User | null => {
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  
  try {
    return JSON.parse(userStr);
  } catch (error) {
    console.error('[Auth] Failed to parse user data:', error);
    return null;
  }
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('authToken');
  const user = localStorage.getItem('user');
  return !!(token && user);
};

/**
 * Get auth token
 */
export const getAuthToken = (): string | null => {
  return localStorage.getItem('authToken');
};

/**
 * Refresh authentication token
 */
export const refreshAuthToken = async (): Promise<string> => {
  try {
    const response = await api.auth.refreshToken();
    const { token } = response.data;
    
    localStorage.setItem('authToken', token);
    return token;
  } catch (error: any) {
    console.error('[Auth] Token refresh failed:', error);
    throw new Error('Session expired. Please login again.');
  }
};

export const authService = {
  login,
  logout,
  getCurrentUser,
  isAuthenticated,
  getAuthToken,
  refreshAuthToken,
};

export default authService;
