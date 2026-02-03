import AsyncStorage from '@react-native-async-storage/async-storage';
import { api } from './api';

/**
 * Authentication Service for Mobile Driver App
 * Handles user authentication, token management, and session persistence
 */

export interface Driver {
  id: string;
  email: string;
  name: string;
  phone: string;
  vehicleId?: string;
  licenseNumber?: string;
}

export interface LoginResponse {
  token: string;
  user: Driver;
}

/**
 * Login driver with email and password
 */
export const login = async (email: string, password: string): Promise<LoginResponse> => {
  try {
    const response = await api.auth.login(email, password);
    const { token, user } = response.data;
    
    // Store token and user in AsyncStorage
    await AsyncStorage.multiSet([
      ['authToken', token],
      ['user', JSON.stringify(user)],
    ]);
    
    console.log('[Auth] Login successful:', user.email);
    return { token, user };
  } catch (error: any) {
    console.error('[Auth] Login failed:', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Login failed. Please check your credentials.');
  }
};

/**
 * Logout driver and clear session
 */
export const logout = async (): Promise<void> => {
  try {
    await api.auth.logout();
  } catch (error) {
    console.error('[Auth] Logout API call failed:', error);
  } finally {
    // Always clear async storage
    await AsyncStorage.multiRemove(['authToken', 'user']);
    console.log('[Auth] Logout successful');
  }
};

/**
 * Get current driver from AsyncStorage
 */
export const getCurrentDriver = async (): Promise<Driver | null> => {
  try {
    const userStr = await AsyncStorage.getItem('user');
    if (!userStr) return null;
    
    return JSON.parse(userStr);
  } catch (error) {
    console.error('[Auth] Failed to get current driver:', error);
    return null;
  }
};

/**
 * Check if driver is authenticated
 */
export const isAuthenticated = async (): Promise<boolean> => {
  try {
    const token = await AsyncStorage.getItem('authToken');
    const user = await AsyncStorage.getItem('user');
    return !!(token && user);
  } catch (error) {
    console.error('[Auth] Failed to check authentication:', error);
    return false;
  }
};

/**
 * Get auth token
 */
export const getAuthToken = async (): Promise<string | null> => {
  try {
    return await AsyncStorage.getItem('authToken');
  } catch (error) {
    console.error('[Auth] Failed to get auth token:', error);
    return null;
  }
};

/**
 * Update driver profile in storage
 */
export const updateDriverProfile = async (driver: Driver): Promise<void> => {
  try {
    await AsyncStorage.setItem('user', JSON.stringify(driver));
    console.log('[Auth] Driver profile updated');
  } catch (error) {
    console.error('[Auth] Failed to update driver profile:', error);
    throw error;
  }
};

export const authService = {
  login,
  logout,
  getCurrentDriver,
  isAuthenticated,
  getAuthToken,
  updateDriverProfile,
};

export default authService;
