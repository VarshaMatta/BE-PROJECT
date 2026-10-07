import React, { useState, useRef, useEffect } from 'react';
import { Bell, Store, LogOut, ChevronDown, CheckCircle2, AlertTriangle, Sparkles, X } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useShop } from '../../context/ShopContext';
import { useNavigate } from 'react-router-dom';

export const Header = () => {
  const { user, logout } = useAuth();
  const { shops, activeShop, selectShop } = useShop();
  const [showNotifications, setShowNotifications] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();

  // Close notifications popover on click outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowNotifications(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const sampleNotifications = [
    {
      id: 1,
      title: 'CSV Data Validated',
      desc: '12,310 sales records successfully ingested for FreshMart.',
      time: '10m ago',
      icon: CheckCircle2,
      color: 'text-emerald-400 bg-emerald-500/10'
    },
    {
      id: 2,
      title: 'Pricing Rules Updated',
      desc: 'Valid range ₹57.80 - ₹68.00 set for Amul Milk 1L.',
      time: '1h ago',
      icon: Sparkles,
      color: 'text-purple-400 bg-purple-500/10'
    },
    {
      id: 3,
      title: 'Data Sufficiency Alert',
      desc: 'New Chips needs historical sales data (Cold Start).',
      time: '3h ago',
      icon: AlertTriangle,
      color: 'text-amber-400 bg-amber-500/10'
    },
  ];

  return (
    <header className="h-16 bg-[#0F1424]/90 backdrop-blur border-b border-slate-800/80 px-8 flex items-center justify-between sticky top-0 z-30">
      {/* Active Shop Selector Dropdown */}
      <div className="flex items-center gap-3">
        <div className="relative inline-block text-left">
          <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-sm text-slate-200">
            <Store className="w-4 h-4 text-purple-400" />
            <select
              value={activeShop ? activeShop.shop_id : ''}
              onChange={(e) => {
                const s = shops.find(item => item.shop_id === parseInt(e.target.value));
                if (s) selectShop(s);
              }}
              className="bg-transparent border-none text-slate-200 text-sm font-semibold focus:outline-none cursor-pointer pr-2"
            >
              {shops.map((s) => (
                <option key={s.shop_id} value={s.shop_id} className="bg-slate-900 text-slate-200">
                  {s.shop_name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Right controls: Notifications, User Profile, Logout */}
      <div className="flex items-center gap-4">
        {/* Notifications Popover Trigger */}
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 transition relative"
            title="Notifications"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-purple-500 animate-pulse"></span>
          </button>

          {/* Notifications Dropdown Panel */}
          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 bg-[#121726] border border-slate-800 rounded-2xl shadow-2xl p-4 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">Notifications</h3>
                <button
                  onClick={() => setShowNotifications(false)}
                  className="text-slate-500 hover:text-slate-300"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <div className="space-y-3">
                {sampleNotifications.map((n) => {
                  const Icon = n.icon;
                  return (
                    <div key={n.id} className="flex gap-3 p-2.5 rounded-xl bg-[#181E30] border border-slate-800/80 hover:border-slate-700 transition">
                      <div className={`w-8 h-8 rounded-lg ${n.color} flex items-center justify-center flex-shrink-0`}>
                        <Icon className="w-4 h-4" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <p className="text-xs font-semibold text-white truncate">{n.title}</p>
                          <span className="text-[10px] text-slate-500">{n.time}</span>
                        </div>
                        <p className="text-[11px] text-slate-400 mt-0.5 leading-tight">{n.desc}</p>
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="pt-3 mt-3 border-t border-slate-800 text-center">
                <button
                  onClick={() => {
                    setShowNotifications(false);
                    navigate('/dashboard');
                  }}
                  className="text-[11px] text-purple-400 hover:text-purple-300 font-semibold"
                >
                  View All Alerts
                </button>
              </div>
            </div>
          )}
        </div>

        {/* User Profile Info */}
        <div className="flex items-center gap-3 pl-2 border-l border-slate-800">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-purple-500 to-indigo-500 flex items-center justify-center font-bold text-white text-xs shadow">
            {user ? user.name.charAt(0).toUpperCase() : 'A'}
          </div>
          <div className="text-left hidden sm:block">
            <p className="text-xs font-semibold text-slate-200 leading-tight">{user ? user.name : 'Alex Kumar'}</p>
            <p className="text-[10px] text-slate-400">{user ? user.email : 'owner@pricewise.io'}</p>
          </div>
        </div>

        {/* Logout Button */}
        <button
          onClick={() => {
            logout();
            navigate('/login');
          }}
          title="Sign Out"
          className="p-2 rounded-xl text-slate-400 hover:text-rose-400 hover:bg-slate-900 transition"
        >
          <LogOut className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
};
