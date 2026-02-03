import axios, { type AxiosInstance, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios';

/**
 * API Client Configuration for SwiftLogistics Web Portal
 * 
 * This module sets up an Axios instance with:
 * - Base URL from environment variables
 * - Authentication token handling
 * - Request/response interceptors
 * - Error handling
 */

const API_BASE_URL = import.meta.env.VITE_API_GATEWAY_URL || 'http://localhost:3000';

// Create Axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request Interceptor
 * Attaches JWT token to every request if available
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('authToken');
    
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Log request in debug mode
    if (import.meta.env.VITE_DEBUG === 'true') {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.data);
    }
    
    return config;
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
  (response: AxiosResponse) => {
    // Log response in debug mode
    if (import.meta.env.VITE_DEBUG === 'true') {
      console.log(`[API Response] ${response.config.url}`, response.data);
    }
    
    return response;
  },
  (error) => {
    // Handle different error scenarios
    if (error.response) {
      const { status, data } = error.response;
      
      // Unauthorized - redirect to login
      if (status === 401) {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
      
      // Forbidden
      if (status === 403) {
        console.error('[API] Access forbidden:', data.message);
      }
      
      // Server error
      if (status >= 500) {
        console.error('[API] Server error:', data.message);
      }
      
      // Log error in debug mode
      if (import.meta.env.VITE_DEBUG === 'true') {
        console.error(`[API Error] ${error.config?.url}`, {
          status,
          message: data.message || data.error,
          data,
        });
      }
    } else if (error.request) {
      // Request made but no response received
      console.error('[API] No response received:', error.message);
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
    
    refreshToken: () => 
      apiClient.post('/api/auth/refresh'),
  },

  // Orders
  orders: {
    getAll: (params?: { status?: string; page?: number; limit?: number }) => 
      apiClient.get('/api/orders', { params }),
    
    getById: (id: string) => 
      apiClient.get(`/api/orders/${id}`),
    
    create: (orderData: any) => 
      apiClient.post('/api/orders', orderData),
    
    update: (id: string, orderData: any) => 
      apiClient.patch(`/api/orders/${id}`, orderData),
    
    track: (trackingNumber: string) => 
      apiClient.get(`/api/orders/track/${trackingNumber}`),
  },

  // Billing
  billing: {
    getInvoices: (params?: { page?: number; limit?: number }) => 
      apiClient.get('/api/billing/invoices', { params }),
    
    getInvoiceById: (id: string) => 
      apiClient.get(`/api/billing/invoices/${id}`),
    
    downloadInvoice: (id: string) => 
      apiClient.get(`/api/billing/invoices/${id}/download`, {
        responseType: 'blob',
      }),
  },

  // Contracts
  contracts: {
    getAll: () => 
      apiClient.get('/api/contracts'),
    
    getById: (id: string) => 
      apiClient.get(`/api/contracts/${id}`),
  },

  // Packages (WMS integration)
  packages: {
    getById: (id: string) => 
      apiClient.get(`/api/packages/${id}`),
    
    track: (trackingNumber: string) => 
      apiClient.get(`/api/packages/track/${trackingNumber}`),
  },
};

export default apiClient;
