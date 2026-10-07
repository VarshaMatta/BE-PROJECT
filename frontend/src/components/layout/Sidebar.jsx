import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  TrendingUp, 
  LayoutDashboard, 
  Store, 
  UploadCloud, 
  Package, 
  Sparkles, 
  History, 
  Settings 
} from 'lucide-react';

export const Sidebar = () => {
  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Shops', path: '/shops', icon: Store },
    { label: 'Data Upload', path: '/upload', icon: UploadCloud },
    { label: 'Products', path: '/products', icon: Package },
    { label: 'Recommendations', path: '/recommendations', icon: Sparkles },
    { label: 'History', path: '/history', icon: History },
    { label: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-[#0F1424] border-r border-slate-800/80 flex flex-col justify-between min-h-screen select-none">
      <div>
        {/* Brand Logo Header */}
        <div className="h-16 flex items-center gap-3 px-6 border-b border-slate-800/60">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-600/30">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-white tracking-tight leading-none">PriceWise</h1>
            <p className="text-[10px] text-purple-400 font-medium tracking-wide">AI Pricing System</p>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-4 space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-600/25'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`
                }
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Footer info */}
      <div className="p-4 border-t border-slate-800/60 text-xs text-slate-500">
        <p className="font-semibold text-slate-400">PriceWise v1.0</p>
        <p>Constraint-Aware System</p>
      </div>
    </aside>
  );
};
