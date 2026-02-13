import React from 'react';
import { Order, Priority, getStageIndex } from '@/types';
import { MapPin, Clock, Package, AlertTriangle, ChevronRight } from 'lucide-react';
import TrackingStepper from './TrackingStepper';

interface OrderCardProps {
  order: Order;
  onClick?: () => void;
  showTracking?: boolean;
}

const priorityConfig: Record<Priority, { class: string; label: string }> = {
  urgent: { class: 'badge-priority-urgent', label: 'Urgent' },
  high: { class: 'badge-priority-high', label: 'High Priority' },
  normal: { class: 'badge-priority-normal', label: 'Normal' },
};

const OrderCard: React.FC<OrderCardProps> = ({ order, onClick, showTracking = false }) => {
  const totalWeight = order.items.reduce((sum, item) => sum + item.weight * item.quantity, 0);
  const totalItems = order.items.reduce((sum, item) => sum + item.quantity, 0);
  const stageProgress = ((getStageIndex(order.status) + 1) / 8) * 100;

  return (
    <div
      onClick={onClick}
      className={`glass-card p-5 transition-all ${
        onClick ? 'cursor-pointer hover:scale-[1.02] active:scale-[0.98]' : ''
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-lg font-semibold text-foreground">{order.orderNumber}</span>
            <span className={priorityConfig[order.priority].class}>
              {priorityConfig[order.priority].label}
            </span>
          </div>
          <p className="text-sm text-muted-foreground">{order.clientName}</p>
        </div>
        {onClick && (
          <ChevronRight className="w-5 h-5 text-muted-foreground" strokeWidth={1.5} />
        )}
      </div>

      {/* Delivery Address */}
      <div className="flex items-start gap-3 mb-4 p-3 rounded-xl bg-secondary/30">
        <MapPin className="w-5 h-5 text-primary mt-0.5 shrink-0" strokeWidth={1.5} />
        <div className="text-sm">
          <p className="text-foreground">{order.deliveryAddress.street}</p>
          <p className="text-muted-foreground">
            {order.deliveryAddress.city}, {order.deliveryAddress.state} {order.deliveryAddress.zipCode}
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        <div className="text-center p-2 rounded-lg bg-secondary/30">
          <Package className="w-4 h-4 text-muted-foreground mx-auto mb-1" strokeWidth={1.5} />
          <p className="text-xs text-muted-foreground">Items</p>
          <p className="text-sm font-semibold text-foreground">{totalItems}</p>
        </div>
        <div className="text-center p-2 rounded-lg bg-secondary/30">
          <AlertTriangle className="w-4 h-4 text-muted-foreground mx-auto mb-1" strokeWidth={1.5} />
          <p className="text-xs text-muted-foreground">Weight</p>
          <p className="text-sm font-semibold text-foreground">{totalWeight.toFixed(1)} kg</p>
        </div>
        <div className="text-center p-2 rounded-lg bg-secondary/30">
          <Clock className="w-4 h-4 text-muted-foreground mx-auto mb-1" strokeWidth={1.5} />
          <p className="text-xs text-muted-foreground">ETA</p>
          <p className="text-sm font-semibold text-foreground">
            {order.estimatedDelivery
              ? new Date(order.estimatedDelivery).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
              : 'TBD'}
          </p>
        </div>
      </div>

      {/* Progress Bar or Tracking */}
      {showTracking ? (
        <TrackingStepper currentStatus={order.status} />
      ) : (
        <div>
          <div className="flex items-center justify-between text-xs mb-2">
            <span className="text-muted-foreground">Progress</span>
            <span className="text-primary font-medium">{Math.round(stageProgress)}%</span>
          </div>
          <div className="h-2 rounded-full bg-secondary/50 overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{
                width: `${stageProgress}%`,
                background: order.status === 'delivered'
                  ? 'linear-gradient(90deg, hsl(142, 60%, 50%), hsl(142, 60%, 40%))'
                  : 'linear-gradient(90deg, hsl(211, 100%, 50%), hsl(211, 100%, 60%))',
              }}
            />
          </div>
          <div className="mt-2">
            <TrackingStepper currentStatus={order.status} compact />
          </div>
        </div>
      )}

      {/* Special Instructions */}
      {order.specialInstructions && (
        <div className="mt-4 p-3 rounded-xl bg-warning/10 border border-warning/20">
          <p className="text-xs font-medium text-warning mb-1">Special Instructions</p>
          <p className="text-sm text-foreground">{order.specialInstructions}</p>
        </div>
      )}
    </div>
  );
};

export default OrderCard;
