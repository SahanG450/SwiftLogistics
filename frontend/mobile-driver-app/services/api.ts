import axios, { AxiosInstance } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

/**
 * API Client Configuration for SwiftLogistics Mobile Driver App
 * 
 * This module sets up an Axios instance with:
 * - Base URL from environment variables
 * - Authentication token handling with AsyncStorage
 * - Request/response interceptors
 * - Error handling for mobile environment
 */

// Use environment variable or fallback
const API_BASE_URL = process.env.API_GATEWAY_URL || 'http://10.0.2.2:3000';

console.log('[API] Base URL:', API_BASE_URL);

// Create Axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000, // Longer timeout for mobile networks
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request Interceptor
 * Attaches JWT token to every request if available
 */
apiClient.interceptors.request.use(
  async (config) => {
    try {
      const token = await AsyncStorage.getItem('authToken');
      
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      
      // Log request in debug mode
      if (process.env.DEBUG === 'true') {
        console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
      }
      
      return config;
    } catch (error) {
      console.error('[API] Error in request interceptor:', error);
      return config;
    }
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

/**
 * Response Interceptor
 * Handles responses and errors globally
 */
apiClient.interceptors.response.use(
  (response) => {
    // Log response in debug mode
    if (process.env.DEBUG === 'true') {
      console.log(`[API Response] ${response.config.url}`, response.status);
    }
    
    return response;
  },
  async (error) => {
    // Handle different error scenarios
    if (error.response) {
      const { status, data } = error.response;
      
      // Unauthorized - clear storage and redirect to login
      if (status === 401) {
        await AsyncStorage.multiRemove(['authToken', 'user']);
        // Navigation will be handled by AuthContext
      }
      
      // Log error in debug mode
      if (process.env.DEBUG === 'true') {
        console.error(`[API Error] ${error.config?.url}`, {
          status,
          message: data.message || data.error,
        });
      }
    } else if (error.request) {
      // Request made but no response received (network error)
      console.error('[API] Network Error - No response received');
    } else {
      // Error setting up request
      console.error('[API] Request setup error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

/**
 * API Service Methods
 */

export const api = {
  // Auth
  auth: {
    login: (email: string, password: string) => 
      apiClient.post('/api/auth/login', { email, password }),
    
    logout: () => 
      apiClient.post('/api/auth/logout'),
  },

  // Driver Manifest
  manifest: {
    getDriverManifest: (driverId: string, date?: string) => 
      apiClient.get(`/api/manifests/driver/${driverId}`, { 
        params: { date } 
      }),
    
    getById: (manifestId: string) => 
      apiClient.get(`/api/manifests/${manifestId}`),
    
    startManifest: (manifestId: string) => 
      apiClient.post(`/api/manifests/${manifestId}/start`, {
        timestamp: new Date().toISOString(),
      }),
    
    completeManifest: (manifestId: string) => 
      apiClient.post(`/api/manifests/${manifestId}/complete`, {
        timestamp: new Date().toISOString(),
      }),
  },

  // Deliveries
  deliveries: {
    getById: (orderId: string) => 
      apiClient.get(`/api/orders/${orderId}`),
    
    markDelivered: (orderId: string, data: {
      timestamp: string;
      location: { lat: number; lng: number };
      proofPhoto?: string;
      signature?: string;
      notes?: string;
    }) => 
      apiClient.post(`/api/orders/${orderId}/mark-delivered`, data),
    
    markFailed: (orderId: string, data: {
      timestamp: string;
      location: { lat: number; lng: number };
      reason: string;
      notes?: string;
    }) => 
      apiClient.post(`/api/orders/${orderId}/mark-failed`, data),
    
    uploadProof: (orderId: string, photoData: string) => 
      apiClient.post(`/api/orders/${orderId}/upload-proof`, {
        photo: photoData,
      }),
  },

  // Driver Stats
  driver: {
    getStats: (driverId: string, period?: 'today' | 'week' | 'month') => 
      apiClient.get(`/api/driver/${driverId}/stats`, {
        params: { period },
      }),
    
    getProfile: (driverId: string) => 
      apiClient.get(`/api/driver/${driverId}/profile`),
    
    updateLocation: (driverId: string, location: { lat: number; lng: number }) => 
      apiClient.post(`/api/driver/${driverId}/location`, {
        location,
        timestamp: new Date().toISOString(),
      }),
  },
};

export default apiClient;
