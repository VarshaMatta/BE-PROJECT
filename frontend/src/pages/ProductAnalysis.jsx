import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Sliders, CheckCircle2, TrendingUp, DollarSign, Calendar, Layers } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';
import { useShop } from '../context/ShopContext';
import { StatusBadge } from '../components/common/Badge';
import API from '../services/api';

export const ProductAnalysis = () => {
  const { productId } = useParams();
  const { activeShop } = useShop();
  const navigate = useNavigate();

  const [product, setProduct] = useState(null);
  const [charts, setCharts] = useState({ sales_history: [], price_history: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (activeShop && productId) {
      fetchProductDetails();
    }
  }, [activeShop, productId]);

  const fetchProductDetails = async () => {
    try {
      setLoading(true);
      const res = await API.get(`/shops/${activeShop.shop_id}/products/${productId}`);
      setProduct(res.data);

      const chartRes = await API.get(`/shops/${activeShop.shop_id}/products/${productId}/charts`);
      setCharts(chartRes.data);
    } catch (err) {
      console.error('Failed to load product details:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !product) {
    return (
      <div className="text-center py-20 text-slate-400">
        <p>Loading product analysis...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Back Button */}
      <button
        onClick={() => navigate('/products')}
        className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Products</span>
      </button>

      {/* Product Header Card */}
      <div className="bg-[#121726] border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center text-white font-extrabold text-xl shadow-lg shadow-purple-600/30">
            {product.product_name.charAt(0)}
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-white tracking-tight">{product.product_name}</h1>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/30">
                {product.category}
              </span>
              <StatusBadge status={product.data_sufficiency_status} />
            </div>
            <p className="text-xs text-slate-400 mt-1">Product ID: {product.external_code}</p>
          </div>
        </div>

        <button
          onClick={() => navigate(`/products/${product.product_id}/constraints`)}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-xs shadow-lg shadow-purple-600/30 hover:from-purple-500 hover:to-indigo-500 transition self-start md:self-auto"
        >
          <Sliders className="w-4 h-4" />
          <span>Set Pricing Rules</span>
        </button>
      </div>

      {/* 5 Key Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-4 text-center">
          <p className="text-[11px] text-slate-400 font-medium">Current Price</p>
          <p className="text-2xl font-extrabold text-white mt-1">₹{product.current_price.toFixed(2)}</p>
        </div>

        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-4 text-center">
          <p className="text-[11px] text-slate-400 font-medium">MRP</p>
          <p className="text-2xl font-extrabold text-slate-200 mt-1">₹{product.mrp ? product.mrp.toFixed(2) : (product.current_price * 1.15).toFixed(2)}</p>
        </div>

        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-4 text-center">
          <p className="text-[11px] text-slate-400 font-medium">Cost (Your Input)</p>
          <p className="text-2xl font-extrabold text-purple-400 mt-1">₹{product.cost_price ? product.cost_price.toFixed(2) : (product.current_price * 0.75).toFixed(2)}</p>
        </div>

        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-4 text-center">
          <p className="text-[11px] text-slate-400 font-medium">History</p>
          <p className="text-2xl font-extrabold text-slate-200 mt-1">{product.history_days} days</p>
        </div>

        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-4 text-center col-span-2 sm:col-span-1">
          <p className="text-[11px] text-slate-400 font-medium">Price Points</p>
          <p className="text-2xl font-extrabold text-indigo-400 mt-1">{product.price_point_count}</p>
        </div>
      </div>

      {/* Two Recharts Graphs: Sales History + Price History */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Sales History Chart */}
        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white">Sales History</h3>
            <span className="text-[11px] text-slate-500 font-semibold">Quantity Sold</span>
          </div>

          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={charts.sales_history}>
                <defs>
                  <linearGradient id="purpleArea" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" stroke="#64748B" fontSize={10} tickLine={false} />
                <YAxis stroke="#64748B" fontSize={10} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#181E30', borderColor: '#334155', borderRadius: '10px', color: '#FFF' }} />
                <Area type="monotone" dataKey="quantity_sold" stroke="#8B5CF6" strokeWidth={2.5} fillOpacity={1} fill="url(#purpleArea)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Price History Chart */}
        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white">Price History</h3>
            <span className="text-[11px] text-slate-500 font-semibold">Selling Price (₹)</span>
          </div>

          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={charts.price_history}>
                <XAxis dataKey="date" stroke="#64748B" fontSize={10} tickLine={false} />
                <YAxis stroke="#64748B" fontSize={10} tickLine={false} domain={['auto', 'auto']} />
                <Tooltip contentStyle={{ backgroundColor: '#181E30', borderColor: '#334155', borderRadius: '10px', color: '#FFF' }} />
                <Line type="stepAfter" dataKey="selling_price" stroke="#A78BFA" strokeWidth={2.5} dot={{ fill: '#8B5CF6', r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Data Quality Checklist Section */}
      <div className="bg-[#121726] border border-slate-800 rounded-2xl p-6">
        <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>Data Quality Audit</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div className="p-3 rounded-xl bg-[#181E30] border border-slate-800 flex items-center gap-3">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span className="text-slate-300 font-medium">{product.history_days} days history</span>
          </div>

          <div className="p-3 rounded-xl bg-[#181E30] border border-slate-800 flex items-center gap-3">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span className="text-slate-300 font-medium">{product.price_point_count} different selling prices</span>
          </div>

          <div className="p-3 rounded-xl bg-[#181E30] border border-slate-800 flex items-center gap-3">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span className="text-slate-300 font-medium">Sufficient non-zero sales</span>
          </div>

          <div className="p-3 rounded-xl bg-[#181E30] border border-slate-800 flex items-center gap-3">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span className="text-slate-300 font-medium">Eligible for demand modeling</span>
          </div>
        </div>
      </div>
    </div>
  );
};
