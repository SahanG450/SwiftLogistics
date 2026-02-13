import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { User, Order, OrderStatus } from '@/types';

interface AppContextType {
  user: User | null;
  orders: Order[];
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  register: (userData: Partial<User>) => Promise<boolean>;
  updateOrderStatus: (orderId: string, status: OrderStatus, podData?: { signature?: string; photo?: string }) => void;
  addOrder: (order: Omit<Order, 'id' | 'createdAt' | 'updatedAt'>) => void;
  showConfetti: boolean;
  setShowConfetti: (show: boolean) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

// Mock initial data
const mockOrders: Order[] = [
  {
    id: '1',
    orderNumber: 'SW-2024-001',
    clientId: 'client-1',
    clientName: 'John Doe',
    deliveryAddress: {
      street: '123 Main Street',
      city: 'San Francisco',
      state: 'CA',
      zipCode: '94102',
      country: 'USA',
      instructions: 'Leave at front door',
    },
    items: [
      { id: 'item-1', name: 'Electronics Package', quantity: 2, weight: 3.5, price: 299.99 },
      { id: 'item-2', name: 'Documents', quantity: 1, weight: 0.5, price: 49.99 },
    ],
    priority: 'high',
    specialInstructions: 'Handle with care - fragile contents',
    status: 'ready_for_pickup',
    assignedDriverId: 'driver-1',
    createdAt: new Date('2024-01-15'),
    updatedAt: new Date('2024-01-15'),
    estimatedDelivery: new Date('2024-01-17'),
  },
  {
    id: '2',
    orderNumber: 'SW-2024-002',
    clientId: 'client-1',
    clientName: 'John Doe',
    deliveryAddress: {
      street: '456 Oak Avenue',
      city: 'Los Angeles',
      state: 'CA',
      zipCode: '90001',
      country: 'USA',
    },
    items: [
      { id: 'item-3', name: 'Medical Supplies', quantity: 5, weight: 8.0, price: 599.99 },
    ],
    priority: 'urgent',
    status: 'shipping',
    assignedDriverId: 'driver-1',
    createdAt: new Date('2024-01-14'),
    updatedAt: new Date('2024-01-15'),
    estimatedDelivery: new Date('2024-01-16'),
  },
  {
    id: '3',
    orderNumber: 'SW-2024-003',
    clientId: 'client-1',
    clientName: 'John Doe',
    deliveryAddress: {
      street: '789 Pine Road',
      city: 'Seattle',
      state: 'WA',
      zipCode: '98101',
      country: 'USA',
    },
    items: [
      { id: 'item-4', name: 'Office Equipment', quantity: 1, weight: 15.0, price: 1299.99 },
    ],
    priority: 'normal',
    status: 'delivered',
    assignedDriverId: 'driver-1',
    createdAt: new Date('2024-01-10'),
    updatedAt: new Date('2024-01-13'),
    deliveredAt: new Date('2024-01-13'),
  },
  {
    id: '4',
    orderNumber: 'SW-2024-004',
    clientId: 'client-1',
    clientName: 'John Doe',
    deliveryAddress: {
      street: '321 Elm Street',
      city: 'Portland',
      state: 'OR',
      zipCode: '97201',
      country: 'USA',
    },
    items: [
      { id: 'item-5', name: 'Retail Goods', quantity: 10, weight: 5.0, price: 199.99 },
    ],
    priority: 'normal',
    status: 'cms_billing',
    createdAt: new Date('2024-01-16'),
    updatedAt: new Date('2024-01-16'),
  },
];

const mockUsers: { email: string; password: string; user: User }[] = [
  {
    email: 'client@swifttrack.com',
    password: 'client123',
    user: {
      id: 'client-1',
      email: 'client@swifttrack.com',
      name: 'John Doe',
      role: 'client',
      phone: '+1 (555) 123-4567',
      address: '123 Business Park, San Francisco, CA',
      membership_level: 'platinum',
    },
  },
  {
    email: 'driver@swifttrack.com',
    password: 'driver123',
    user: {
      id: 'driver-1',
      email: 'driver@swifttrack.com',
      name: 'Mike Johnson',
      role: 'driver',
      phone: '+1 (555) 987-6543',
    },
  },
];

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [orders, setOrders] = useState<Order[]>(mockOrders);
  const [showConfetti, setShowConfetti] = useState(false);

  const login = useCallback(async (email: string, password: string): Promise<boolean> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const foundUser = mockUsers.find(
      u => u.email.toLowerCase() === email.toLowerCase() && u.password === password
    );
    
    if (foundUser) {
      setUser(foundUser.user);
      return true;
    }
    return false;
  }, []);

  const logout = useCallback(() => {
    setUser(null);
  }, []);

  const register = useCallback(async (userData: Partial<User>): Promise<boolean> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const newUser: User = {
      id: `client-${Date.now()}`,
      email: userData.email || '',
      name: userData.name || '',
      role: 'client',
      phone: userData.phone,
      address: userData.address,
      membership_level: userData.membership_level || 'silver',
    };
    
    setUser(newUser);
    return true;
  }, []);

  const updateOrderStatus = useCallback((
    orderId: string, 
    status: OrderStatus,
    podData?: { signature?: string; photo?: string }
  ) => {
    setOrders(prevOrders => 
      prevOrders.map(order => {
        if (order.id === orderId) {
          const updatedOrder = {
            ...order,
            status,
            updatedAt: new Date(),
            ...(status === 'delivered' && { deliveredAt: new Date() }),
            ...(podData?.signature && { podSignature: podData.signature }),
            ...(podData?.photo && { podPhoto: podData.photo }),
          };
          
          // Trigger confetti for delivered status
          if (status === 'delivered') {
            setShowConfetti(true);
            setTimeout(() => setShowConfetti(false), 3000);
          }
          
          return updatedOrder;
        }
        return order;
      })
    );
  }, []);

  const addOrder = useCallback((orderData: Omit<Order, 'id' | 'createdAt' | 'updatedAt'>) => {
    const newOrder: Order = {
      ...orderData,
      id: `order-${Date.now()}`,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    setOrders(prevOrders => [newOrder, ...prevOrders]);
  }, []);

  return (
    <AppContext.Provider value={{
      user,
      orders,
      login,
      logout,
      register,
      updateOrderStatus,
      addOrder,
      showConfetti,
      setShowConfetti,
    }}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
