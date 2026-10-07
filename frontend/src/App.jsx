import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ShopProvider } from './context/ShopContext';
import { DashboardLayout } from './components/layout/DashboardLayout';

import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Shops } from './pages/Shops';
import { Dashboard } from './pages/Dashboard';
import { DataUpload } from './pages/DataUpload';
import { ColumnMapping } from './pages/ColumnMapping';
import { ValidationResult } from './pages/ValidationResult';
import { ProductsList } from './pages/ProductsList';
import { ProductAnalysis } from './pages/ProductAnalysis';
import { SetConstraints } from './pages/SetConstraints';
import { Recommendations } from './pages/Recommendations';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-screen bg-[#0B0E17] flex items-center justify-center text-slate-400">
        <p>Loading PriceWise...</p>
      </div>
    );
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return <DashboardLayout>{children}</DashboardLayout>;
};

const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (user) {
    return <Navigate to="/dashboard" replace />;
  }
  return children;
};

export default function App() {
  return (
    <Router>
      <AuthProvider>
        <ShopProvider>
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
            <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />

            {/* Protected Routes */}
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/shops" element={<ProtectedRoute><Shops /></ProtectedRoute>} />
            <Route path="/upload" element={<ProtectedRoute><DataUpload /></ProtectedRoute>} />
            <Route path="/upload/mapping" element={<ProtectedRoute><ColumnMapping /></ProtectedRoute>} />
            <Route path="/upload/validation" element={<ProtectedRoute><ValidationResult /></ProtectedRoute>} />
            <Route path="/products" element={<ProtectedRoute><ProductsList /></ProtectedRoute>} />
            <Route path="/products/:productId" element={<ProtectedRoute><ProductAnalysis /></ProtectedRoute>} />
            <Route path="/products/:productId/constraints" element={<ProtectedRoute><SetConstraints /></ProtectedRoute>} />
            <Route path="/recommendations" element={<ProtectedRoute><Recommendations /></ProtectedRoute>} />

            {/* History & Settings placeholder routes */}
            <Route path="/history" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/settings" element={<ProtectedRoute><Shops /></ProtectedRoute>} />

            {/* Default Catch-all */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </ShopProvider>
      </AuthProvider>
    </Router>
  );
}
