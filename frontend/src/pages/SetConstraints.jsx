import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, CheckCircle2, AlertTriangle, Calculator, Sparkles, Check } from 'lucide-react';
import { useShop } from '../context/ShopContext';
import API from '../services/api';

export const SetConstraints = () => {
  const { productId } = useParams();
  const { activeShop } = useShop();
  const navigate = useNavigate();

  const [productName, setProductName] = useState('Product');
  const [costPrice, setCostPrice] = useState(52);
  const [mrp, setMrp] = useState(68);
  const [maxDiscount, setMaxDiscount] = useState(15);
  const [minMargin, setMinMargin] = useState(10);
  const [availableStock, setAvailableStock] = useState(120);

  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (activeShop && productId) {
      loadInitialConstraints();
    }
  }, [activeShop, productId]);

  const loadInitialConstraints = async () => {
    try {
      const prodRes = await API.get(`/shops/${activeShop.shop_id}/products/${productId}`);
      setProductName(prodRes.data.product_name);

      const res = await API.get(`/shops/${activeShop.shop_id}/products/${productId}/constraints`);
      setCostPrice(res.data.cost_price);
      setMrp(res.data.mrp);
      setMaxDiscount(res.data.max_discount_pct);
      setMinMargin(res.data.min_margin_pct);
      setAvailableStock(res.data.available_stock);

      // Initial evaluation
      evaluate({
        cost_price: res.data.cost_price,
        mrp: res.data.mrp,
        max_discount_pct: res.data.max_discount_pct,
        min_margin_pct: res.data.min_margin_pct,
        available_stock: res.data.available_stock
      });
    } catch (err) {
      console.error('Failed to load constraints:', err);
    }
  };

  const evaluate = async (overrideData) => {
    setError('');
    setLoading(true);

    const payload = overrideData || {
      cost_price: parseFloat(costPrice) || 0,
      mrp: parseFloat(mrp) || 0,
      max_discount_pct: parseFloat(maxDiscount) || 0,
      min_margin_pct: parseFloat(minMargin) || 0,
      available_stock: parseInt(availableStock) || 0
    };

    try {
      const res = await API.post(`/shops/${activeShop.shop_id}/products/${productId}/constraints/evaluate`, payload);
      setEvaluation(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Evaluation failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveConstraints = async () => {
    setSaving(true);
    const payload = {
      cost_price: parseFloat(costPrice) || 0,
      mrp: parseFloat(mrp) || 0,
      max_discount_pct: parseFloat(maxDiscount) || 0,
      min_margin_pct: parseFloat(minMargin) || 0,
      available_stock: parseInt(availableStock) || 0
    };

    try {
      const res = await API.post(`/shops/${activeShop.shop_id}/products/${productId}/constraints/save`, payload);
      setEvaluation(res.data.evaluation);
      navigate(`/recommendations?product_id=${productId}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save constraints.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Back Link */}
      <button
        onClick={() => navigate(`/products/${productId}`)}
        className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Product Analysis</span>
      </button>

      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Set Pricing Rules</h1>
        <p className="text-sm text-slate-400 mt-1">Define your business constraints for <span className="text-purple-400 font-semibold">{productName}</span></p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm font-medium">
          {error}
        </div>
      )}

      {/* Main Grid: Left Inputs Form, Right Dynamic Result Card */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Inputs Column */}
        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-6 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Cost Price (₹)</label>
            <input
              type="number"
              step="0.01"
              value={costPrice}
              onChange={(e) => setCostPrice(e.target.value)}
              className="w-full bg-[#181E30] border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">MRP (₹)</label>
            <input
              type="number"
              step="0.01"
              value={mrp}
              onChange={(e) => setMrp(e.target.value)}
              className="w-full bg-[#181E30] border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Maximum Discount (%)</label>
            <input
              type="number"
              step="0.1"
              value={maxDiscount}
              onChange={(e) => setMaxDiscount(e.target.value)}
              className="w-full bg-[#181E30] border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Minimum Margin (%)</label>
            <input
              type="number"
              step="0.1"
              value={minMargin}
              onChange={(e) => setMinMargin(e.target.value)}
              className="w-full bg-[#181E30] border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Available Stock</label>
            <input
              type="number"
              value={availableStock}
              onChange={(e) => setAvailableStock(e.target.value)}
              className="w-full bg-[#181E30] border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
            />
          </div>

          <div className="pt-4 flex gap-3">
            <button
              type="button"
              onClick={() => evaluate()}
              className="flex-1 py-3 px-4 rounded-xl bg-[#181E30] border border-slate-700 text-slate-200 font-semibold text-xs hover:bg-slate-800 transition"
            >
              Calculate Range
            </button>
            <button
              type="button"
              onClick={handleSaveConstraints}
              disabled={saving || (evaluation && !evaluation.is_valid)}
              className="flex-1 py-3 px-4 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-xs shadow-lg shadow-purple-600/30 hover:from-purple-500 hover:to-indigo-500 transition disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save & Recommend →'}
            </button>
          </div>
        </div>

        {/* Right Output Evaluation Card */}
        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            {evaluation?.is_valid ? (
              <div className="space-y-6">
                {/* Header Status Badge */}
                <div className="flex items-center gap-3 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                  <CheckCircle2 className="w-6 h-6 flex-shrink-0" />
                  <div>
                    <h3 className="text-sm font-bold text-emerald-300">VALID PRICE RANGE</h3>
                    <p className="text-xs text-emerald-400/80">Based on your constraints.</p>
                  </div>
                </div>

                {/* Range Numbers & Slider Visualization */}
                <div className="bg-[#181E30] rounded-2xl p-6 border border-slate-800 text-center space-y-4">
                  <div className="flex items-center justify-between text-2xl font-extrabold text-white">
                    <span>₹{evaluation.min_allowed_price.toFixed(2)}</span>
                    <span className="text-slate-600 text-base">─────────</span>
                    <span>₹{evaluation.max_allowed_price.toFixed(2)}</span>
                  </div>

                  {/* Visual Progress Bar */}
                  <div className="relative w-full h-3 rounded-full bg-slate-800 overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-indigo-500 rounded-full"></div>
                  </div>

                  <div className="flex justify-between text-[11px] text-slate-400 font-medium px-1">
                    <span>Min allowed price</span>
                    <span>Max allowed price (MRP)</span>
                  </div>
                </div>

                {/* Checklist items */}
                <div className="space-y-3 pt-2">
                  {evaluation.checks.map((chk, idx) => (
                    <div key={idx} className="flex items-center gap-3 text-xs">
                      <div className={`w-5 h-5 rounded-full ${chk.passed ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'} flex items-center justify-center flex-shrink-0`}>
                        <Check className="w-3.5 h-3.5" />
                      </div>
                      <span className="font-semibold text-slate-200">{chk.label}</span>
                      <span className="text-[11px] text-slate-500 ml-auto">{chk.detail}</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Conflict Status Badge */}
                <div className="flex items-center gap-3 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400">
                  <AlertTriangle className="w-6 h-6 flex-shrink-0" />
                  <div>
                    <h3 className="text-sm font-bold text-rose-300">NO VALID PRICE RANGE</h3>
                    <p className="text-xs text-rose-400/90">Your selected constraints conflict.</p>
                  </div>
                </div>

                <div className="bg-[#181E30] rounded-2xl p-6 border border-slate-800 text-center space-y-3">
                  <AlertTriangle className="w-10 h-10 text-rose-400 mx-auto" />
                  <h4 className="text-sm font-bold text-white">Impossible Constraints Detected</h4>
                  <div className="text-xs text-rose-300 space-y-1 text-left bg-rose-950/20 p-4 rounded-xl border border-rose-900/40">
                    {evaluation?.conflict_reasons.map((r, i) => (
                      <p key={i}>• {r}</p>
                    ))}
                  </div>
                  <p className="text-xs text-slate-400">Please modify your inputs on the left to resolve conflicts.</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
