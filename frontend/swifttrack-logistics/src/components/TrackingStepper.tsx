import React from 'react';
import { ORDER_STAGES, OrderStatus, getStageIndex } from '@/types';
import { Warehouse, Receipt, Cog, UserCheck, Package, Truck, Navigation, CheckCircle } from 'lucide-react';

interface TrackingStepperProps {
  currentStatus: OrderStatus;
  compact?: boolean;
}

const iconMap: { [key: string]: React.ReactNode } = {
  Warehouse: <Warehouse className="w-4 h-4" strokeWidth={1.5} />,
  Receipt: <Receipt className="w-4 h-4" strokeWidth={1.5} />,
  Cog: <Cog className="w-4 h-4" strokeWidth={1.5} />,
  UserCheck: <UserCheck className="w-4 h-4" strokeWidth={1.5} />,
  Package: <Package className="w-4 h-4" strokeWidth={1.5} />,
  Truck: <Truck className="w-4 h-4" strokeWidth={1.5} />,
  Navigation: <Navigation className="w-4 h-4" strokeWidth={1.5} />,
  CheckCircle: <CheckCircle className="w-4 h-4" strokeWidth={1.5} />,
};

const TrackingStepper: React.FC<TrackingStepperProps> = ({ currentStatus, compact = false }) => {
  const currentIndex = getStageIndex(currentStatus);

  if (compact) {
    return (
      <div className="flex items-center gap-1">
        {ORDER_STAGES.map((stage, index) => {
          const isCompleted = index < currentIndex;
          const isActive = index === currentIndex;
          const isDelivered = currentStatus === 'delivered';

          return (
            <React.Fragment key={stage.status}>
              <div
                className={`w-6 h-6 rounded-full flex items-center justify-center text-xs transition-all ${
                  isDelivered && index <= currentIndex
                    ? 'bg-success text-success-foreground'
                    : isCompleted
                    ? 'bg-success text-success-foreground'
                    : isActive
                    ? 'bg-primary text-primary-foreground animate-pulse-glow'
                    : 'bg-secondary text-muted-foreground'
                }`}
                title={stage.label}
              >
                {index + 1}
              </div>
              {index < ORDER_STAGES.length - 1 && (
                <div
                  className={`w-3 h-0.5 transition-all ${
                    isDelivered || isCompleted ? 'bg-success' : isActive ? 'bg-primary' : 'bg-secondary'
                  }`}
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    );
  }

  return (
    <div className="space-y-0 stagger-children">
      {ORDER_STAGES.map((stage, index) => {
        const isCompleted = index < currentIndex;
        const isActive = index === currentIndex;
        const isDelivered = currentStatus === 'delivered';

        return (
          <div key={stage.status}>
            <div className="tracking-step py-2">
              <div
                className={`tracking-step-circle ${
                  isDelivered && index <= currentIndex
                    ? 'completed'
                    : isCompleted
                    ? 'completed'
                    : isActive
                    ? 'active'
                    : 'pending'
                }`}
              >
                {iconMap[stage.icon]}
              </div>
              <div className="flex-1">
                <p className={`text-sm font-medium ${
                  isCompleted || isActive || isDelivered ? 'text-foreground' : 'text-muted-foreground'
                }`}>
                  {stage.label}
                </p>
                {isActive && !isDelivered && (
                  <p className="text-xs text-primary mt-0.5">In Progress</p>
                )}
                {isDelivered && index === currentIndex && (
                  <p className="text-xs text-success mt-0.5">Completed</p>
                )}
              </div>
              <span className={`text-xs font-medium ${
                isDelivered && index <= currentIndex
                  ? 'text-success'
                  : isCompleted
                  ? 'text-success'
                  : isActive
                  ? 'text-primary'
                  : 'text-muted-foreground'
              }`}>
                {isDelivered && index <= currentIndex
                  ? '✓'
                  : isCompleted
                  ? '✓'
                  : isActive
                  ? '•••'
                  : `Step ${index + 1}`}
              </span>
            </div>
            {index < ORDER_STAGES.length - 1 && (
              <div
                className={`tracking-connector ml-5 ${
                  isDelivered || isCompleted ? 'completed' : isActive ? 'active' : ''
                }`}
              />
            )}
          </div>
        );
      })}
    </div>
  );
};

export default TrackingStepper;
