/**
 * TypeScript Type Definitions for SwiftLogistics Web Portal
 */

// User Types
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'client' | 'admin' | 'driver';
  company?: string;
  phone?: string;
}

// Order Types
export interface Address {
  street: string;
  city: string;
  province: string;
  postalCode: string;
  country: string;
  coordinates?: {
    lat: number;
    lng: number;
  };
}

export interface PackageDetails {
  weight: number;
  dimensions: {
    length: number;
    width: number;
    height: number;
  };
  value?: number;
  description?: string;
  fragile?: boolean;
  requiresSignature?: boolean;
}

export type OrderStatus = 
  | 'PENDING'
  | 'CONFIRMED'
  | 'RECEIVED'
  | 'INSPECTED'
  | 'STORED'
  | 'LOADED'
  | 'IN_TRANSIT'
  | 'OUT_FOR_DELIVERY'
  | 'DELIVERED'
  | 'FAILED'
  | 'CANCELLED';

export type OrderPriority = 'STANDARD' | 'URGENT' | 'SAME_DAY';

export interface Order {
  id: string;
  orderNumber: string;
  clientId: string;
  trackingNumber?: string;
  status: OrderStatus;
  priority: OrderPriority;
  
  pickupAddress: Address;
  pickupContact: {
    name: string;
    phone: string;
    email?: string;
  };
  pickupDate: string;
  
  deliveryAddress: Address;
  deliveryContact: {
    name: string;
    phone: string;
    email?: string;
  };
  deliveryDate?: string;
  estimatedDeliveryDate?: string;
  
  packageDetails: PackageDetails;
  
  specialInstructions?: string;
  
  manifestId?: string;
  driverId?: string;
  
  createdAt: string;
  updatedAt: string;
}

// Billing Types
export type PaymentStatus = 'PENDING' | 'PAID' | 'OVERDUE' | 'CANCELLED';

export interface Invoice {
  id: string;
  invoiceNumber: string;
  clientId: string;
  orderId: string;
  
  amount: number;
  currency: string;
  
  status: PaymentStatus;
  
  items: {
    description: string;
    quantity: number;
    unitPrice: number;
    amount: number;
  }[];
  
  subtotal: number;
  tax: number;
  total: number;
  
  dueDate: string;
  paidDate?: string;
  
  createdAt: string;
  updatedAt: string;
}

// Contract Types
export type ContractStatus = 'ACTIVE' | 'EXPIRED' | 'PENDING' | 'CANCELLED';

export interface Contract {
  id: string;
  contractNumber: string;
  clientId: string;
  
  status: ContractStatus;
  
  startDate: string;
  endDate: string;
  
  services: string[];
  pricing: {
    baseRate: number;
    perKgRate: number;
    urgentSurcharge: number;
  };
  
  sla: {
    standardDelivery: string;
    urgentDelivery: string;
    sameDayDelivery: string;
  };
  
  createdAt: string;
  updatedAt: string;
}

// Package/Tracking Types
export interface TrackingEvent {
  timestamp: string;
  status: OrderStatus;
  location: string;
  description: string;
  performedBy?: string;
}

export interface PackageTracking {
  trackingNumber: string;
  currentStatus: OrderStatus;
  currentLocation: string;
  
  events: TrackingEvent[];
  
  estimatedDelivery?: string;
  
  packageDetails: PackageDetails;
  
  origin: Address;
  destination: Address;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Form Types
export interface NewOrderForm {
  pickupAddress: Address;
  pickupContact: {
    name: string;
    phone: string;
    email?: string;
  };
  pickupDate: string;
  
  deliveryAddress: Address;
  deliveryContact: {
    name: string;
    phone: string;
    email?: string;
  };
  
  packageDetails: PackageDetails;
  priority: OrderPriority;
  specialInstructions?: string;
}

// Auth Types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}
