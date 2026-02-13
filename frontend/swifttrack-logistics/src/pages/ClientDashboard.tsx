import React, { useState, useMemo } from 'react';
import { useApp } from '@/context/AppContext';
import { useNavigate } from 'react-router-dom';
import { 
  Package, 
  DollarSign, 
  AlertCircle, 
  Plus, 
  LogOut, 
  User,
  Truck,
  FileText,
  Filter
} from 'lucide-react';
import StatCard from '@/components/StatCard';
import OrderCard from '@/components/OrderCard';
import Confetti from '@/components/Confetti';

const ClientDashboard: React.FC = () => {
  const { user, orders, logout, showConfetti } = useApp();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'orders' | 'billing' | 'exceptions'>('orders');
  const [selectedOrder, setSelectedOrder] = useState<string | null>(null);

  const clientOrders = useMemo(() => 
    orders.filter(o => o.clientId === user?.id),
    [orders, user]
  );

  const activeOrders = clientOrders.filter(o => o.status !== 'delivered');
  const failedOrders = clientOrders.filter(o => o.failureReason);
  
  const totalSpent = useMemo(() => {
    return clientOrders.reduce((sum, order) => {
      const totalWeight = order.items.reduce((w, item) => w + item.weight * item.quantity, 0);
      return sum + 500 + (totalWeight * 100);
    }, 0);
  }, [clientOrders]);

  const billingItems = useMemo(() => {
    return clientOrders.map(order => {
      const totalWeight = order.items.reduce((w, item) => w + item.weight * item.quantity, 0);
      const baseFee = 500;
      const weightFee = totalWeight * 100;
      return {
        orderId: order.id,
        orderNumber: order.orderNumber,
        baseFee,
        weightFee,
        totalWeight,
        total: baseFee + weightFee,
        date: order.createdAt,
        status: order.status,
      };
    });
  }, [clientOrders]);

  const currentOrder = selectedOrder ? clientOrders.find(o => o.id === selectedOrder) : null;

  const tabs = [
    { id: 'orders', label: 'Orders', icon: Package, count: activeOrders.length },
    { id: 'billing', label: 'Billing', icon: FileText, count: billingItems.length },
    { id: 'exceptions', label: 'Exceptions', icon: AlertCircle, count: failedOrders.length },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Confetti show={showConfetti} />
      
      {/* Header */}
      <header className="sticky top-0 z-40 backdrop-blur-xl bg-background/80 border-b border-border">
        <div className="container max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                <Truck className="w-5 h-5 text-primary-foreground" strokeWidth={1.5} />
              </div>
              <div>
                <h1 className="text-lg font-bold text-foreground">SwiftTrack</h1>
                <p className="text-xs text-muted-foreground">Client Portal</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-3 py-2 rounded-xl bg-secondary/50">
                <User className="w-4 h-4 text-muted-foreground" strokeWidth={1.5} />
                <span className="text-sm text-foreground">{user?.name}</span>
                {user?.membership_level && (
                  <span className="px-2 py-0.5 text-xs rounded-full bg-primary/20 text-primary font-medium capitalize">
                    {user.membership_level}
                  </span>
                )}
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

      <main className="container max-w-6xl mx-auto px-4 py-6">
        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6 stagger-children">
          <StatCard
            title="Active Orders"
            value={activeOrders.length}
            subtitle={`${clientOrders.filter(o => o.status === 'delivered').length} delivered`}
            icon={<Package className="w-5 h-5" strokeWidth={1.5} />}
            variant="primary"
          />
          <StatCard
            title="Total Spent"
            value={`$${totalSpent.toLocaleString()}`}
            subtitle="This month"
            icon={<DollarSign className="w-5 h-5" strokeWidth={1.5} />}
            variant="success"
            trend={{ value: 12, positive: true }}
          />
          <StatCard
            title="Failed Attempts"
            value={failedOrders.length}
            subtitle="Requires attention"
            icon={<AlertCircle className="w-5 h-5" strokeWidth={1.5} />}
            variant={failedOrders.length > 0 ? 'warning' : 'default'}
          />
        </div>

        {/* New Order Button */}
        <button
          onClick={() => navigate('/new-order')}
          className="btn-primary w-full sm:w-auto mb-6"
        >
          <Plus className="w-5 h-5" strokeWidth={1.5} />
          Create New Order
        </button>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => { setActiveTab(tab.id as typeof activeTab); setSelectedOrder(null); }}
              className={`flex items-center gap-2 px-4 py-3 rounded-xl font-medium text-sm whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? 'bg-primary text-primary-foreground shadow-glow-primary'
                  : 'bg-secondary/50 text-muted-foreground hover:text-foreground'
              }`}
            >
              <tab.icon className="w-4 h-4" strokeWidth={1.5} />
              {tab.label}
              {tab.count > 0 && (
                <span className={`px-2 py-0.5 text-xs rounded-full ${
                  activeTab === tab.id
                    ? 'bg-primary-foreground/20'
                    : 'bg-muted'
                }`}>
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Order List */}
          <div className="space-y-4">
            {activeTab === 'orders' && (
              <>
                {clientOrders.length === 0 ? (
                  <div className="glass-card p-8 text-center">
                    <Package className="w-12 h-12 text-muted-foreground mx-auto mb-4" strokeWidth={1} />
                    <p className="text-muted-foreground">No orders yet</p>
                    <button
                      onClick={() => navigate('/new-order')}
                      className="btn-primary mt-4"
                    >
                      Create First Order
                    </button>
                  </div>
                ) : (
                  clientOrders.map((order) => (
                    <OrderCard
                      key={order.id}
                      order={order}
                      onClick={() => setSelectedOrder(order.id)}
                    />
                  ))
                )}
              </>
            )}

            {activeTab === 'billing' && (
              <div className="glass-card overflow-hidden">
                <div className="p-4 border-b border-border">
                  <h3 className="font-semibold text-foreground">Monthly Invoice</h3>
                  <p className="text-sm text-muted-foreground">Formula: Base Fee $500 + (Weight × $100)</p>
                </div>
                <div className="divide-y divide-border">
                  {billingItems.map((item) => (
                    <div key={item.orderId} className="p-4 hover:bg-secondary/20 transition-colors">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium text-foreground">{item.orderNumber}</span>
                        <span className="text-lg font-bold text-primary">${item.total.toLocaleString()}</span>
                      </div>
                      <div className="flex items-center justify-between text-sm text-muted-foreground">
                        <span>Base: ${item.baseFee} + Weight ({item.totalWeight.toFixed(1)}kg): ${item.weightFee}</span>
                        <span>{new Date(item.date).toLocaleDateString()}</span>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="p-4 border-t border-border bg-primary/10">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-foreground">Total</span>
                    <span className="text-xl font-bold text-primary">
                      ${billingItems.reduce((sum, item) => sum + item.total, 0).toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'exceptions' && (
              <>
                {failedOrders.length === 0 ? (
                  <div className="glass-card p-8 text-center">
                    <AlertCircle className="w-12 h-12 text-success mx-auto mb-4" strokeWidth={1} />
                    <p className="text-success font-medium">No failed deliveries!</p>
                    <p className="text-sm text-muted-foreground mt-1">All orders are on track</p>
                  </div>
                ) : (
                  failedOrders.map((order) => (
                    <div key={order.id} className="glass-card p-5 border-l-4 border-destructive">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <span className="font-semibold text-foreground">{order.orderNumber}</span>
                          <p className="text-sm text-muted-foreground">{order.clientName}</p>
                        </div>
                        <span className="badge-priority-urgent">Failed</span>
                      </div>
                      <div className="p-3 rounded-xl bg-destructive/10 border border-destructive/20">
                        <p className="text-sm font-medium text-destructive mb-1">Failure Reason</p>
                        <p className="text-sm text-foreground">{order.failureReason}</p>
                        {order.failureNotes && (
                          <p className="text-xs text-muted-foreground mt-2">{order.failureNotes}</p>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </>
            )}
          </div>

          {/* Order Details Panel */}
          <div className="hidden lg:block">
            {currentOrder ? (
              <div className="glass-card p-6 sticky top-24 animate-fade-in">
                <h3 className="text-xl font-bold text-foreground mb-6">Order Details</h3>
                <OrderCard order={currentOrder} showTracking />
              </div>
            ) : (
              <div className="glass-card p-8 text-center sticky top-24">
                <Filter className="w-12 h-12 text-muted-foreground mx-auto mb-4" strokeWidth={1} />
                <p className="text-muted-foreground">Select an order to view details</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default ClientDashboard;
