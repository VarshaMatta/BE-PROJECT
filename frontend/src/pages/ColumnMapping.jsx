import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Table, AlertCircle } from 'lucide-react';
import { useShop } from '../context/ShopContext';
import API from '../services/api';

export const ColumnMapping = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { activeShop } = useShop();

  const previewData = location.state?.previewData;
  const file = location.state?.file;

  const columns = previewData?.columns || [];
  const suggested = previewData?.suggested_mapping || {};

  const [mapping, setMapping] = useState(() => {
    const initial = {};
    columns.forEach(col => {
      initial[col] = suggested[col] || 'ignore';
    });
    return initial;
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const priceWiseFields = [
    { key: 'product_id', label: 'Product ID (Required)', required: true },
    { key: 'date', label: 'Date (Required)', required: true },
    { key: 'quantity_sold', label: 'Quantity Sold (Required)', required: true },
    { key: 'selling_price', label: 'Selling Price (Required)', required: true },
    { key: 'promotion', label: 'Promotion (Optional)', required: false },
    { key: 'category', label: 'Category (Optional)', required: false },
    { key: 'ignore', label: '-- Ignore Column --', required: false },
  ];

  const handleMappingChange = (colName, targetField) => {
    setMapping(prev => ({
      ...prev,
      [colName]: targetField
    }));
  };

  const handleValidate = async () => {
    setError('');

    // Client-side check required fields mapped
    const mappedValues = Object.values(mapping);
    const requiredKeys = ['product_id', 'date', 'quantity_sold', 'selling_price'];
    for (const req of requiredKeys) {
      if (!mappedValues.includes(req)) {
        setError(`Please map a CSV column to '${req.replace('_', ' ').toUpperCase()}' (Required).`);
        return;
      }
    }

    if (!file || !activeShop) {
      setError('File or active shop session lost. Please re-upload.');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('mapping_str', JSON.stringify(mapping));

    try {
      const res = await API.post(`/shops/${activeShop.shop_id}/uploads/validate`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      // Pass validation result to ValidationResult screen
      navigate('/upload/validation', { state: { validationResult: res.data, mapping, file } });
    } catch (err) {
      setError(err.response?.data?.detail || 'Validation error.');
    } finally {
      setLoading(false);
    }
  };

  if (!previewData || !file) {
    return (
      <div className="text-center py-20">
        <p className="text-slate-400">No file data found. Please upload a CSV first.</p>
        <button onClick={() => navigate('/upload')} className="mt-4 px-4 py-2 bg-purple-600 rounded-xl text-white font-semibold">
          Go to Upload
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Map Your Columns</h1>
        <p className="text-sm text-slate-400 mt-1">Tell PriceWise what each column in your CSV represents.</p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm font-medium flex items-center gap-2">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Column Mapping Table Card */}
      <div className="bg-[#121726] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-[#181E30] text-xs font-semibold text-slate-400 border-b border-slate-800">
            <tr>
              <th className="px-6 py-4">Your CSV Column</th>
              <th className="px-6 py-4">PriceWise Field</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {columns.map((col) => (
              <tr key={col} className="hover:bg-slate-900/40 transition">
                <td className="px-6 py-4 font-semibold text-white flex items-center gap-2">
                  <Table className="w-4 h-4 text-purple-400" />
                  <span>{col}</span>
                </td>
                <td className="px-6 py-4">
                  <select
                    value={mapping[col]}
                    onChange={(e) => handleMappingChange(col, e.target.value)}
                    className="w-full max-w-md bg-[#181E30] border border-slate-700 rounded-xl px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
                  >
                    {priceWiseFields.map((field) => (
                      <option key={field.key} value={field.key} className="bg-slate-900 text-slate-200">
                        {field.label}
                      </option>
                    ))}
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Action Footer Buttons */}
      <div className="flex items-center justify-between pt-4">
        <button
          onClick={() => navigate('/upload')}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-slate-700 text-slate-300 hover:text-white font-semibold text-xs transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back</span>
        </button>

        <button
          onClick={handleValidate}
          disabled={loading}
          className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-sm shadow-lg shadow-purple-600/30 hover:from-purple-500 hover:to-indigo-500 transition"
        >
          <span>{loading ? 'Validating...' : 'Validate Data'}</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
