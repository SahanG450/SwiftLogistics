import React from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ReactNode;
  trend?: {
    value: number;
    positive: boolean;
  };
  variant?: 'default' | 'primary' | 'success' | 'warning';
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  variant = 'default',
}) => {
  const variantStyles = {
    default: 'from-card to-secondary/30',
    primary: 'from-primary/20 to-primary/5',
    success: 'from-success/20 to-success/5',
    warning: 'from-warning/20 to-warning/5',
  };

  const iconStyles = {
    default: 'text-muted-foreground',
    primary: 'text-primary',
    success: 'text-success',
    warning: 'text-warning',
  };

  return (
    <div className="stat-card relative overflow-hidden">
      <div className={`absolute inset-0 bg-gradient-to-br ${variantStyles[variant]} opacity-50`} />
      <div className="relative">
        <div className="flex items-start justify-between mb-3">
          <div className={`p-2.5 rounded-xl bg-secondary/50 ${iconStyles[variant]}`}>
            {icon}
          </div>
          {trend && (
            <span className={`text-xs font-medium px-2 py-1 rounded-full ${
              trend.positive
                ? 'bg-success/20 text-success'
                : 'bg-destructive/20 text-destructive'
            }`}>
              {trend.positive ? '+' : ''}{trend.value}%
            </span>
          )}
        </div>
        <p className="text-sm text-muted-foreground mb-1">{title}</p>
        <p className="text-2xl font-bold text-foreground">{value}</p>
        {subtitle && (
          <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>
        )}
      </div>
    </div>
  );
};

export default StatCard;
