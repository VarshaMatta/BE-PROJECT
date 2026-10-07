import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Package, FileText, ShieldCheck, ArrowUpRight, UploadCloud } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';
import { useAuth } from '../context/AuthContext';
import { useShop } from '../context/ShopContext';
import { StatusBadge } from '../components/common/Badge';
import API from '../services/api';

export const Dashboard = () => {
  const { user } = useAuth();
  const { activeShop } = useShop();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (activeShop) {
      fetchDashboardData();
    }
  }, [activeShop]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const res = await API.get(`/shops/${activeShop.shop_id}/analytics/overview`);
      setData(res.data);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!activeShop) {
    return (
      <div className="text-center py-20 bg-[#121726] rounded-2xl border border-slate-800 p-8">
        <UploadCloud className="w-16 h-16 text-purple-400 mx-auto mb-4 animate-bounce" />
        <h2 className="text-xl font-bold text-white mb-2">No Shop Selected</h2>
        <p className="text-sm text-slate-400 mb-6">Please select or create a shop to view its dashboard.</p>
        <button
          onClick={() => navigate('/shops')}
          className="px-6 py-2.5 rounded-xl bg-purple-600 text-white font-semibold text-sm hover:bg-purple-500"
        >
          Go to Shops
        </button>
      </div>
    );
  }

  const chartData = data?.sales_overview_chart || [];
  const isEmptyData = !data || (data.products_count === 0 && data.sales_records_count === 0);

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Top Greeting Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            Good Morning, {user?.name.split(' ')[0] || 'Alex'} <span className="text-xl">👋</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">Here's what's happening at <span className="font-semibold text-purple-400">{activeShop.shop_name}</span>.</p>
        </div>
        <button
          onClick={() => navigate('/upload')}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-xs shadow-lg shadow-purple-600/30 hover:from-purple-500 hover:to-indigo-500 transition"
        >
          <UploadCloud className="w-4 h-4" />
          <span>Upload Sales CSV</span>
        </button>
      </div>

      {/* Top 3 KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Products Card */}
        <div className="bg-[#121726] border border-slate-800/80 rounded-2xl p-6 flex items-center justify-between shadow-lg">
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Products</p>
            <h3 className="text-3xl font-extrabold text-white mt-2">{data?.products_count || 0}</h3>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
            <Package className="w-6 h-6" />
          </div>
        </div>

        {/* Sales Records Card */}
        <div className="bg-[#121726] border border-slate-800/80 rounded-2xl p-6 flex items-center justify-between shadow-lg">
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Sales Records</p>
            <h3 className="text-3xl font-extrabold text-white mt-2">{(data?.sales_records_count || 0).toLocaleString()}</h3>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
            <FileText className="w-6 h-6" />
          </div>
        </div>

        {/* Data Quality Card */}
        <div className="bg-[#121726] border border-slate-800/80 rounded-2xl p-6 flex items-center justify-between shadow-lg">
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Data Quality</p>
            <h3 className="text-3xl font-extrabold text-white mt-2">{data?.data_quality_pct || 0}%</h3>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
            <ShieldCheck className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Main Content Grid: Chart + Products Needing Attention */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Sales Overview Chart */}
        <div className="lg:col-span-2 bg-[#121726] border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-base font-bold text-white">Sales Overview</h2>
              <p className="text-xs text-slate-400">Historical transaction trends</p>
            </div>
            <select className="bg-[#181E30] border border-slate-700 text-xs text-slate-300 rounded-lg px-3 py-1.5 focus:outline-none">
              <option>Last 6 Months</option>
              <option>Last 12 Months</option>
            </select>
          </div>

          {chartData.length > 0 ? (
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="purpleGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0.0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="month" stroke="#64748B" fontSize={11} tickLine={false} />
                  <YAxis stroke="#64748B" fontSize={11} tickLine={false} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#181E30', borderColor: '#334155', borderRadius: '12px', color: '#FFF' }}
                  />
                  <Area type="monotone" dataKey="sales" stroke="#8B5CF6" strokeWidth={3} fillOpacity={1} fill="url(#purpleGradient)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-64 flex flex-col items-center justify-center text-center text-slate-500 bg-[#181E30]/50 rounded-xl border border-dashed border-slate-800">
              <UploadCloud className="w-10 h-10 mb-2 text-slate-600" />
              <p className="text-xs font-semibold text-slate-400">No Historical Sales Data Uploaded</p>
              <p className="text-[11px] text-slate-500 mt-1 max-w-xs">Upload your shop's sales transaction CSV to render charts and ML recommendations.</p>
              <button
                onClick={() => navigate('/upload')}
                className="mt-4 px-4 py-2 rounded-xl bg-purple-600/20 text-purple-400 border border-purple-500/30 text-xs font-semibold hover:bg-purple-600/30"
              >
                Upload CSV
              </button>
            </div>
          )}
        </div>

        {/* Right Col: Products Needing Attention */}
        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-bold text-white">Products Needing Attention</h2>
              <button onClick={() => navigate('/products')} className="text-xs text-purple-400 hover:text-purple-300 font-semibold flex items-center gap-1">
                View All <ArrowUpRight className="w-3 h-3" />
              </button>
            </div>

            <div className="space-y-3">
              {data?.products_needing_attention && data.products_needing_attention.length > 0 ? (
                data.products_needing_attention.map((p) => (
                  <div
                    key={p.product_id}
                    onClick={() => navigate(`/products/${p.product_id}`)}
                    className="p-3.5 rounded-xl bg-[#181E30] border border-slate-800/80 hover:border-slate-700 transition cursor-pointer flex items-center justify-between"
                  >
                    <div>
                      <h4 className="text-xs font-bold text-white">{p.product_name}</h4>
                      <p className="text-[10px] text-slate-400">{p.category} • {p.days_ago}</p>
                    </div>
                    <StatusBadge status={p.status} />
                  </div>
                ))
              ) : (
                <div className="p-6 text-center text-xs text-slate-500 bg-[#181E30]/40 rounded-xl border border-slate-800/60">
                  <p>All products are sufficiently populated!</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
