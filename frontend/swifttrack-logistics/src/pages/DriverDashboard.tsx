import React, { useState, useMemo } from 'react';
import { useApp } from '@/context/AppContext';
import { useNavigate } from 'react-router-dom';
import { 
  Truck, 
  LogOut, 
  User,
  MapPin,
  Navigation,
  Package,
  CheckCircle,
  Camera,
  FileSignature,
  ChevronRight,
  Clock,
  AlertTriangle
} from 'lucide-react';
import { Order, OrderStatus, getStageIndex } from '@/types';
import Confetti from '@/components/Confetti';
import SignatureCanvas from '@/components/SignatureCanvas';

const DriverDashboard: React.FC = () => {
  const { user, orders, logout, updateOrderStatus, showConfetti } = useApp();
  const navigate = useNavigate();
  const [selectedOrder, setSelectedOrder] = useState<string | null>(null);
  const [showSignature, setShowSignature] = useState(false);
  const [podData, setPodData] = useState<{ signature?: string; photo?: string }>({});

  // Get orders assigned to this driver that are ready for driver actions (stages 5-8)
  const driverOrders = useMemo(() => 
    orders.filter(o => 
      o.assignedDriverId === user?.id && 
      getStageIndex(o.status) >= 4 && // Ready for Pickup and beyond
      o.status !== 'delivered'
    ).sort((a, b) => {
      // Sort by priority: urgent > high > normal
      const priorityOrder = { urgent: 0, high: 1, normal: 2 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }),
    [orders, user]
  );

  const completedToday = useMemo(() => 
    orders.filter(o => 
      o.assignedDriverId === user?.id && 
      o.status === 'delivered' &&
      o.deliveredAt &&
      new Date(o.deliveredAt).toDateString() === new Date().toDateString()
    ).length,
    [orders, user]
  );

  const currentOrder = selectedOrder ? orders.find(o => o.id === selectedOrder) : null;

  const getNextStatus = (currentStatus: OrderStatus): OrderStatus | null => {
    const statusFlow: { [key in OrderStatus]?: OrderStatus } = {
      ready_for_pickup: 'pickup',
      pickup: 'shipping',
      shipping: 'delivered',
    };
    return statusFlow[currentStatus] || null;
  };

  const handleStatusUpdate = (orderId: string, newStatus: OrderStatus) => {
    if (newStatus === 'delivered') {
      // Show signature canvas first
      setShowSignature(true);
    } else {
      updateOrderStatus(orderId, newStatus);
    }
  };

  const handleSignatureSave = (signature: string) => {
    if (currentOrder) {
      setPodData(prev => ({ ...prev, signature }));
      setShowSignature(false);
      updateOrderStatus(currentOrder.id, 'delivered', { signature });
      setSelectedOrder(null);
    }
  };

  const handlePhotoUpload = () => {
    // Simulate photo capture
    const mockPhotoUrl = 'data:image/png;base64,mock-photo-data';
    setPodData(prev => ({ ...prev, photo: mockPhotoUrl }));
    // In a real app, this would open the camera
    alert('Photo captured! (Simulated)');
  };

  const statusConfig: { [key in OrderStatus]?: { label: string; color: string; icon: React.ReactNode } } = {
    ready_for_pickup: { 
      label: 'Ready for Pickup', 
      color: 'bg-warning/20 text-warning border-warning/30',
      icon: <Package className="w-4 h-4" strokeWidth={1.5} />
    },
    pickup: { 
      label: 'Picked Up', 
      color: 'bg-primary/20 text-primary border-primary/30',
      icon: <Truck className="w-4 h-4" strokeWidth={1.5} />
    },
    shipping: { 
      label: 'In Transit', 
      color: 'bg-accent/20 text-accent border-accent/30',
      icon: <Navigation className="w-4 h-4" strokeWidth={1.5} />
    },
    delivered: { 
      label: 'Delivered', 
      color: 'bg-success/20 text-success border-success/30',
      icon: <CheckCircle className="w-4 h-4" strokeWidth={1.5} />
    },
  };

  return (
    <div className="min-h-screen bg-background">
      <Confetti show={showConfetti} />
      {showSignature && (
        <SignatureCanvas
          onSave={handleSignatureSave}
          onCancel={() => setShowSignature(false)}
        />
      )}
      
      {/* Header */}
      <header className="sticky top-0 z-40 backdrop-blur-xl bg-background/80 border-b border-border">
        <div className="container max-w-2xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-success to-primary flex items-center justify-center">
                <Truck className="w-5 h-5 text-primary-foreground" strokeWidth={1.5} />
              </div>
              <div>
                <h1 className="text-lg font-bold text-foreground">SwiftTrack</h1>
                <p className="text-xs text-muted-foreground">Driver App</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-3 py-2 rounded-xl bg-secondary/50">
                <User className="w-4 h-4 text-muted-foreground" strokeWidth={1.5} />
                <span className="text-sm text-foreground">{user?.name}</span>
              </div>
              <button
                onClick={() => { logout(); navigate('/login'); }}
                className="p-2.5 rounded-xl hover:bg-secondary/50 text-muted-foreground hover:text-foreground transition-colors"
              >
                <LogOut className="w-5 h-5" strokeWidth={1.5} />
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="container max-w-2xl mx-auto px-4 py-6">
        {/* Stats Bar */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="glass-card p-4 text-center">
            <p className="text-2xl font-bold text-foreground">{driverOrders.length}</p>
            <p className="text-sm text-muted-foreground">Active Deliveries</p>
          </div>
          <div className="glass-card p-4 text-center">
            <p className="text-2xl font-bold text-success">{completedToday}</p>
            <p className="text-sm text-muted-foreground">Completed Today</p>
          </div>
        </div>

        {/* Manifest List */}
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-foreground mb-4">Delivery Manifest</h2>
          
          {driverOrders.length === 0 ? (
            <div className="glass-card p-8 text-center">
              <CheckCircle className="w-12 h-12 text-success mx-auto mb-4" strokeWidth={1} />
              <p className="text-success font-medium">All caught up!</p>
              <p className="text-sm text-muted-foreground mt-1">No pending deliveries</p>
            </div>
          ) : (
            <div className="space-y-4 stagger-children">
              {driverOrders.map((order) => {
                const status = statusConfig[order.status];
                const isSelected = selectedOrder === order.id;
                
                return (
                  <div
                    key={order.id}
                    className={`glass-card p-4 transition-all cursor-pointer ${
                      isSelected ? 'ring-2 ring-primary' : ''
                    }`}
                    onClick={() => setSelectedOrder(isSelected ? null : order.id)}
                  >
                    {/* Header */}
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-foreground">{order.orderNumber}</span>
                        {order.priority === 'urgent' && (
                          <span className="badge-priority-urgent flex items-center gap-1">
                            <AlertTriangle className="w-3 h-3" strokeWidth={2} />
                            Urgent
                          </span>
                        )}
                        {order.priority === 'high' && (
                          <span className="badge-priority-high">High</span>
                        )}
                      </div>
                      <ChevronRight className={`w-5 h-5 text-muted-foreground transition-transform ${
                        isSelected ? 'rotate-90' : ''
                      }`} strokeWidth={1.5} />
                    </div>

                    {/* Address */}
                    <div className="flex items-start gap-2 mb-3">
                      <MapPin className="w-4 h-4 text-primary mt-0.5 shrink-0" strokeWidth={1.5} />
                      <div className="text-sm">
                        <p className="text-foreground">{order.deliveryAddress.street}</p>
                        <p className="text-muted-foreground">
                          {order.deliveryAddress.city}, {order.deliveryAddress.state}
                        </p>
                      </div>
                    </div>

                    {/* Status Badge */}
                    <div className="flex items-center justify-between">
                      {status && (
                        <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium border ${status.color}`}>
                          {status.icon}
                          {status.label}
                        </span>
                      )}
                      <div className="flex items-center gap-1 text-sm text-muted-foreground">
                        <Clock className="w-4 h-4" strokeWidth={1.5} />
                        {order.estimatedDelivery 
                          ? new Date(order.estimatedDelivery).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
                          : 'TBD'}
                      </div>
                    </div>

                    {/* Expanded Content */}
                    {isSelected && (
                      <div className="mt-4 pt-4 border-t border-border animate-fade-in">
                        {/* Items */}
                        <div className="mb-4">
                          <p className="text-xs font-medium text-muted-foreground mb-2">ITEMS</p>
                          {order.items.map((item) => (
                            <div key={item.id} className="flex items-center justify-between text-sm py-1">
                              <span className="text-foreground">{item.name}</span>
                              <span className="text-muted-foreground">×{item.quantity} ({item.weight}kg)</span>
                            </div>
                          ))}
                        </div>

                        {/* Special Instructions */}
                        {order.specialInstructions && (
                          <div className="mb-4 p-3 rounded-lg bg-warning/10 border border-warning/20">
                            <p className="text-xs font-medium text-warning mb-1">Special Instructions</p>
                            <p className="text-sm text-foreground">{order.specialInstructions}</p>
                          </div>
                        )}

                        {/* Delivery Instructions */}
                        {order.deliveryAddress.instructions && (
                          <div className="mb-4 p-3 rounded-lg bg-secondary/30">
                            <p className="text-xs font-medium text-muted-foreground mb-1">Delivery Instructions</p>
                            <p className="text-sm text-foreground">{order.deliveryAddress.instructions}</p>
                          </div>
                        )}

                        {/* Status Controller */}
                        <div className="space-y-3">
                          <p className="text-xs font-medium text-muted-foreground">UPDATE STATUS</p>
                          
                          {/* POD Actions for shipping -> delivered */}
                          {order.status === 'shipping' && (
                            <div className="grid grid-cols-2 gap-3 mb-3">
                              <button
                                onClick={(e) => { e.stopPropagation(); handlePhotoUpload(); }}
                                className="btn-secondary !min-h-[44px]"
                              >
                                <Camera className="w-4 h-4" strokeWidth={1.5} />
                                Photo
                              </button>
                              <button
                                onClick={(e) => { e.stopPropagation(); setShowSignature(true); }}
                                className="btn-secondary !min-h-[44px]"
                              >
                                <FileSignature className="w-4 h-4" strokeWidth={1.5} />
                                Signature
                              </button>
                            </div>
                          )}

                          {/* Status Update Buttons */}
                          <div className="grid grid-cols-1 gap-2">
                            {order.status === 'ready_for_pickup' && (
                              <button
                                onClick={(e) => { e.stopPropagation(); handleStatusUpdate(order.id, 'pickup'); }}
                                className="btn-primary w-full"
                              >
                                <Truck className="w-4 h-4" strokeWidth={1.5} />
                                Mark as Picked Up
                              </button>
                            )}
                            {order.status === 'pickup' && (
                              <button
                                onClick={(e) => { e.stopPropagation(); handleStatusUpdate(order.id, 'shipping'); }}
                                className="btn-primary w-full"
                              >
                                <Navigation className="w-4 h-4" strokeWidth={1.5} />
                                Start Shipping
                              </button>
                            )}
                            {order.status === 'shipping' && (
                              <button
                                onClick={(e) => { e.stopPropagation(); handleStatusUpdate(order.id, 'delivered'); }}
                                className="btn-success w-full"
                              >
                                <CheckCircle className="w-4 h-4" strokeWidth={1.5} />
                                Mark as Delivered
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Completed Deliveries Preview */}
        {completedToday > 0 && (
          <div className="glass-card p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-success/20">
                  <CheckCircle className="w-5 h-5 text-success" strokeWidth={1.5} />
                </div>
                <div>
                  <p className="font-medium text-foreground">{completedToday} Deliveries Completed</p>
                  <p className="text-sm text-muted-foreground">Great work today!</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default DriverDashboard;
