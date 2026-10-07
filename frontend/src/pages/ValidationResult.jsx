import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { CheckCircle2, AlertTriangle, Calendar, Package, ArrowLeft, ArrowRight, Sparkles } from 'lucide-react';
import { useShop } from '../context/ShopContext';
import API from '../services/api';

export const ValidationResult = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { activeShop, refreshShops } = useShop();

  const validationResult = location.state?.validationResult;
  const mapping = location.state?.mapping;
  const file = location.state?.file;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!validationResult || !file || !mapping) {
    return (
      <div className="text-center py-20">
        <p className="text-slate-400">No validation data found.</p>
        <button onClick={() => navigate('/upload')} className="mt-4 px-4 py-2 bg-purple-600 rounded-xl text-white font-semibold">
          Go to Upload
        </button>
      </div>
    );
  }

  const handleCleanAndCommit = async () => {
    if (!file || !activeShop) return;
    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('mapping_str', JSON.stringify(mapping));

    try {
      await API.post(`/shops/${activeShop.shop_id}/uploads/process`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      await refreshShops();
      navigate('/products');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to clean and process dataset.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Data Validation</h1>
        <p className="text-sm text-slate-400 mt-1">We checked your file for common issues.</p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm font-medium">
          {error}
        </div>
      )}

      {/* Validation Status Banner */}
      <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-2xl p-6 flex items-center gap-4 text-emerald-400 shadow-lg">
        <div className="w-12 h-12 rounded-full bg-emerald-500/20 flex items-center justify-center flex-shrink-0">
          <CheckCircle2 className="w-7 h-7 text-emerald-400" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-emerald-300">CSV Validated Successfully</h2>
          <p className="text-xs text-emerald-400/90 mt-0.5">Your file is ready to be cleaned and processed.</p>
        </div>
      </div>

      {/* 4 Stat Boxes Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-5 text-center">
          <p className="text-2xl font-extrabold text-white">{validationResult.total_rows.toLocaleString()}</p>
          <p className="text-xs text-slate-400 font-medium mt-1">Total Rows</p>
        </div>

        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-5 text-center">
          <p className="text-2xl font-extrabold text-emerald-400">{validationResult.valid_rows.toLocaleString()}</p>
          <p className="text-xs text-slate-400 font-medium mt-1">Valid Rows</p>
        </div>

        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-5 text-center">
          <p className="text-2xl font-extrabold text-amber-400">{validationResult.duplicate_rows.toLocaleString()}</p>
          <p className="text-xs text-slate-400 font-medium mt-1">Duplicate Rows</p>
        </div>

        <div className="bg-[#121726] border border-slate-800 rounded-2xl p-5 text-center">
          <p className="text-2xl font-extrabold text-rose-400">{validationResult.invalid_rows.toLocaleString()}</p>
          <p className="text-xs text-slate-400 font-medium mt-1">Invalid Rows</p>
        </div>
      </div>

      {/* Details Grid: Issues Breakdown + Metadata Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Issues List Breakdown */}
        <div className="md:col-span-2 bg-[#121726] border border-slate-800 rounded-2xl p-6">
          <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <span>Issues Found</span>
          </h3>

          <div className="space-y-3 text-xs text-slate-300">
            {validationResult.issues && validationResult.issues.length > 0 ? (
              validationResult.issues.map((issue, idx) => (
                <div key={idx} className="flex items-center gap-2.5">
                  <span className="w-2 h-2 rounded-full bg-amber-400 flex-shrink-0"></span>
                  <span><strong className="text-amber-300 font-semibold">{issue.count} rows</strong> {issue.description}</span>
                </div>
              ))
            ) : (
              <p className="text-slate-500">No data quality issues detected!</p>
            )}
          </div>
        </div>

        {/* Metadata Side Cards */}
        <div className="space-y-4">
          <div className="bg-[#121726] border border-slate-800 rounded-2xl p-5 flex items-center gap-4">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <Calendar className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[11px] text-slate-400 font-medium">Date Range</p>
              <p className="text-xs font-bold text-white mt-0.5">
                {validationResult.date_range_start || 'Jan 2024'} → {validationResult.date_range_end || 'Sep 2026'}
              </p>
            </div>
          </div>

          <div className="bg-[#121726] border border-slate-800 rounded-2xl p-5 flex items-center gap-4">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
              <Package className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[11px] text-slate-400 font-medium">Products Found</p>
              <p className="text-xl font-bold text-white mt-0.5">{validationResult.products_found}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Action Footer Buttons */}
      <div className="flex items-center justify-between pt-4">
        <button
          onClick={() => navigate('/upload/mapping', { state: { previewData: location.state?.previewData, file } })}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-slate-700 text-slate-300 hover:text-white font-semibold text-xs transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back</span>
        </button>

        <button
          onClick={handleCleanAndCommit}
          disabled={loading}
          className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-sm shadow-lg shadow-purple-600/30 hover:from-purple-500 hover:to-indigo-500 transition"
        >
          <span>{loading ? 'Cleaning Data...' : 'Clean & Continue'}</span>
          <Sparkles className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
