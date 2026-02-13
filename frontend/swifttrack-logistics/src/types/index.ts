// User Types
export type UserRole = 'client' | 'driver';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  phone?: string;
  address?: string;
  membership_level?: 'gold' | 'silver' | 'platinum';
}

// Order Types
export type OrderStatus = 
  | 'checking_warehouse'
  | 'cms_billing'
  | 'ros_processing'
  | 'driver_assigned'
  | 'ready_for_pickup'
  | 'pickup'
  | 'shipping'
  | 'delivered';

export type Priority = 'urgent' | 'high' | 'normal';

export interface DeliveryAddress {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
  instructions?: string;
}

export interface OrderItem {
  id: string;
  name: string;
  quantity: number;
  weight: number; // in kg
  price: number;
}

export interface Order {
  id: string;
  orderNumber: string;
  clientId: string;
  clientName: string;
  deliveryAddress: DeliveryAddress;
  items: OrderItem[];
  priority: Priority;
  specialInstructions?: string;
  status: OrderStatus;
  assignedDriverId?: string;
  createdAt: Date;
  updatedAt: Date;
  estimatedDelivery?: Date;
  deliveredAt?: Date;
  failureReason?: string;
  failureNotes?: string;
  podSignature?: string;
  podPhoto?: string;
}

// Billing Types
export interface BillingItem {
  orderId: string;
  orderNumber: string;
  baseFee: number;
  weightFee: number;
  totalWeight: number;
  total: number;
  date: Date;
}

export interface MonthlyBilling {
  month: string;
  year: number;
  items: BillingItem[];
  totalAmount: number;
}

// Status Stage Mapping
export const ORDER_STAGES: { status: OrderStatus; label: string; icon: string }[] = [
  { status: 'checking_warehouse', label: 'Checking Warehouse', icon: 'Warehouse' },
  { status: 'cms_billing', label: 'CMS Billing', icon: 'Receipt' },
  { status: 'ros_processing', label: 'ROS Processing', icon: 'Cog' },
  { status: 'driver_assigned', label: 'Driver Assigned', icon: 'UserCheck' },
  { status: 'ready_for_pickup', label: 'Ready for Pickup', icon: 'Package' },
  { status: 'pickup', label: 'Pickup', icon: 'Truck' },
  { status: 'shipping', label: 'Shipping', icon: 'Navigation' },
  { status: 'delivered', label: 'Delivered', icon: 'CheckCircle' },
];

export const getStageIndex = (status: OrderStatus): number => {
  return ORDER_STAGES.findIndex(s => s.status === status);
};
