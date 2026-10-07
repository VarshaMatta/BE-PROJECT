import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Sparkles, Trophy, TrendingUp, DollarSign, Percent, ShieldCheck, ArrowRight, RefreshCw } from 'lucide-react';
import { useShop } from '../context/ShopContext';
import API from '../services/api';

export const Recommendations = () => {
  const { activeShop } = useShop();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const productIdParam = searchParams.get('product_id');
  const [products, setProducts] = useState([]);
  const [selectedProductId, setSelectedProductId] = useState(productIdParam || '');
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [modelType, setModelType] = useState('sklearn');

  useEffect(() => {
    if (activeShop) {
      loadProductsList();
    }
  }, [activeShop]);

  useEffect(() => {
    if (activeShop && selectedProductId) {
      generateRecommendations(selectedProductId, modelType);
    }
  }, [selectedProductId, modelType]);

  const loadProductsList = async () => {
    try {
      const res = await API.get(`/shops/${activeShop.shop_id}/products`);
      setProducts(res.data);
      if (!selectedProductId && res.data.length > 0) {
        setSelectedProductId(res.data[0].product_id);
      }
    } catch (err) {
      console.error('Failed to load products list:', err);
    }
  };

  const generateRecommendations = async (pid, mType) => {
    try {
      setLoading(true);
      const res = await API.post(`/shops/${activeShop.shop_id}/products/${pid}/recommendations/generate?model_type=${mType}`);
      setRecommendations(res.data);
    } catch (err) {
      console.error('Failed to generate recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const recommended = recommendations?.recommended_scenario;

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Sparkles className="w-6 h-6 text-purple-400" />
            <span>AI Scenario Recommendations</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">Constraint-aware pricing & promotion scenario decision support.</p>
        </div>

        {/* Controls: Select Product + Model Selector */}
        <div className="flex flex-wrap items-center gap-3">
          <select
            value={selectedProductId}
            onChange={(e) => setSelectedProductId(e.target.value)}
            className="bg-[#121726] border border-slate-700 text-xs font-semibold text-slate-200 rounded-xl px-4 py-2.5 focus:outline-none cursor-pointer"
          >
            {products.map((p) => (
              <option key={p.product_id} value={p.product_id} className="bg-slate-900 text-slate-200">
                {p.product_name} (₹{p.current_price.toFixed(2)})
              </option>
            ))}
          </select>

          <select
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
            className="bg-[#121726] border border-slate-700 text-xs font-semibold text-slate-200 rounded-xl px-4 py-2.5 focus:outline-none cursor-pointer"
          >
            <option value="sklearn">Baseline: Scikit-learn (Ridge)</option>
            <option value="xgboost">Advanced: XGBoost Model</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-20 text-slate-400">
          <RefreshCw className="w-8 h-8 text-purple-400 animate-spin mx-auto mb-3" />
          <p>Training demand model & evaluating constraint scenarios...</p>
        </div>
      ) : recommendations ? (
        <div className="space-y-8">
          {/* Top Recommendation Highlight Card */}
          {recommended ? (
            <div className="bg-gradient-to-r from-purple-950/60 via-[#121726] to-indigo-950/60 border border-purple-500/40 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
              <div className="flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40 w-max mb-4">
                <Trophy className="w-3.5 h-3.5 text-amber-400" />
                <span>#1 RANKED OPTIMAL SCENARIO</span>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-center">
                <div>
                  <p className="text-xs font-semibold text-slate-400">Recommended Price Point</p>
                  <h2 className="text-4xl font-extrabold text-white mt-1">₹{recommended.candidate_price.toFixed(2)}</h2>
                  <p className="text-xs text-emerald-400 font-semibold mt-1">
                    Current: ₹{recommendations.current_price.toFixed(2)}
                  </p>
                </div>

                <div className="bg-[#181E30]/80 rounded-2xl p-4 border border-slate-800 text-center">
                  <p className="text-xs text-slate-400">Estimated Demand</p>
                  <p className="text-2xl font-bold text-white mt-1">{recommended.predicted_demand} units</p>
                </div>

                <div className="bg-[#181E30]/80 rounded-2xl p-4 border border-slate-800 text-center">
                  <p className="text-xs text-slate-400">Estimated Gross Profit</p>
                  <p className="text-2xl font-bold text-emerald-400 mt-1">₹{recommended.estimated_profit.toFixed(2)}</p>
                </div>

                <div className="bg-[#181E30]/80 rounded-2xl p-4 border border-slate-800 text-center">
                  <p className="text-xs text-slate-400">Profit Margin</p>
                  <p className="text-2xl font-bold text-purple-400 mt-1">{recommended.profit_margin_pct}%</p>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-purple-900/30 flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1.5 text-emerald-400">
                  <ShieldCheck className="w-4 h-4" /> Validated by Backend Constraint Engine (Feasible Range: ₹{recommendations.min_allowed_price.toFixed(2)} - ₹{recommendations.max_allowed_price.toFixed(2)})
                </span>
                <span>Model Engine: {recommendations.model_used}</span>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center bg-[#121726] rounded-2xl border border-rose-500/30 text-rose-400">
              <p>No feasible scenario found for current product constraints.</p>
            </div>
          )}

          {/* Table of Scenarios Ranked */}
          <div className="bg-[#121726] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
            <div className="p-6 border-b border-slate-800 flex items-center justify-between">
              <h3 className="text-base font-bold text-white">All Feasible Pricing Scenarios</h3>
              <span className="text-xs text-slate-400">Ranked by estimated gross profit</span>
            </div>

            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-[#181E30] text-xs font-semibold text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="px-6 py-4">Rank</th>
                  <th className="px-6 py-4">Candidate Price</th>
                  <th className="px-6 py-4">Predicted Demand</th>
                  <th className="px-6 py-4">Est. Revenue</th>
                  <th className="px-6 py-4">Est. Profit</th>
                  <th className="px-6 py-4">Profit Margin</th>
                  <th className="px-6 py-4 text-right">Feasibility</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {recommendations.scenarios.map((sc) => (
                  <tr
                    key={sc.rank}
                    className={`hover:bg-slate-900/40 transition ${
                      sc.rank === 1 ? 'bg-purple-950/20 font-semibold text-white' : ''
                    }`}
                  >
                    <td className="px-6 py-4">
                      {sc.rank === 1 ? (
                        <span className="w-6 h-6 rounded-full bg-amber-400 text-slate-950 font-bold flex items-center justify-center text-xs">
                          1
                        </span>
                      ) : (
                        <span className="text-slate-500">#{sc.rank}</span>
                      )}
                    </td>
                    <td className="px-6 py-4 font-bold text-white">₹{sc.candidate_price.toFixed(2)}</td>
                    <td className="px-6 py-4 text-slate-300">{sc.predicted_demand} units</td>
                    <td className="px-6 py-4 text-slate-300">₹{sc.estimated_revenue.toFixed(2)}</td>
                    <td className="px-6 py-4 text-emerald-400 font-bold">₹{sc.estimated_profit.toFixed(2)}</td>
                    <td className="px-6 py-4 text-purple-400">{sc.profit_margin_pct}%</td>
                    <td className="px-6 py-4 text-right">
                      <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                        Feasible
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : null}
    </div>
  );
};
