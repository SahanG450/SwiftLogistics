import React from 'react';
import { Navigate } from 'react-router-dom';
import { useApp } from '@/context/AppContext';
import ClientDashboard from './ClientDashboard';
import DriverDashboard from './DriverDashboard';

const Dashboard: React.FC = () => {
  const { user } = useApp();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.role === 'driver') {
    return <DriverDashboard />;
  }

  return <ClientDashboard />;
};

export default Dashboard;
