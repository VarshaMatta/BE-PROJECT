import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, Download, FileSpreadsheet, CheckCircle2, AlertCircle } from 'lucide-react';
import { useShop } from '../context/ShopContext';
import API from '../services/api';

export const DataUpload = () => {
  const { activeShop } = useShop();
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (!selected.name.endsWith('.csv')) {
        setError('Please select a valid .csv file.');
        return;
      }
      setFile(selected);
      setError('');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const dropped = e.dataTransfer.files[0];
      if (!dropped.name.endsWith('.csv')) {
        setError('Please drop a valid .csv file.');
        return;
      }
      setFile(dropped);
      setError('');
    }
  };

  const handleProceedToMapping = async () => {
    if (!file || !activeShop) return;
    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await API.post(`/shops/${activeShop.shop_id}/uploads/preview`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      // Pass preview and suggested mapping data to next ColumnMapping screen
      navigate('/upload/mapping', { state: { previewData: res.data, file } });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload CSV file.');
    } finally {
      setLoading(false);
    }
  };

  const downloadSampleTemplate = () => {
    const csvContent = "data:text/csv;charset=utf-8," 
      + "Item_Code,Sale_Date,Units,Rate,Promo,Category\n"
      + "MLK101,2024-01-01,12,64.0,None,Dairy\n"
      + "MLK101,2024-01-02,15,64.0,None,Dairy\n"
      + "MLK101,2024-01-03,10,68.0,None,Dairy\n"
      + "BRD202,2024-01-01,25,35.0,Discount,Bakery\n"
      + "BIS303,2024-01-01,40,20.0,None,Snacks\n";
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "pricewise_sample_sales.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Upload Historical Sales Data</h1>
        <p className="text-sm text-slate-400 mt-1">Upload your shop's sales CSV file to get started.</p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm font-medium flex items-center gap-2 max-w-2xl mx-auto">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Drag & Drop Card */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`bg-[#121726] border-2 border-dashed ${
          isDragging ? 'border-purple-500 bg-purple-950/20' : 'border-slate-800'
        } rounded-3xl p-12 text-center transition duration-200 shadow-2xl relative overflow-hidden`}
      >
        <div className="w-20 h-20 rounded-3xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 mx-auto mb-6">
          <UploadCloud className="w-10 h-10" />
        </div>

        {file ? (
          <div className="space-y-4">
            <div className="inline-flex items-center gap-3 px-4 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm font-semibold">
              <CheckCircle2 className="w-5 h-5" />
              <span>{file.name} ({(file.size / (1024 * 1024)).toFixed(2)} MB)</span>
            </div>
            <div className="flex justify-center gap-4 mt-6">
              <button
                onClick={() => setFile(null)}
                className="px-4 py-2 rounded-xl text-slate-400 hover:text-white text-xs font-semibold"
              >
                Change File
              </button>
              <button
                onClick={handleProceedToMapping}
                disabled={loading}
                className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-sm shadow-lg shadow-purple-600/30 hover:from-purple-500 hover:to-indigo-500 transition"
              >
                {loading ? 'Reading File...' : 'Map Columns →'}
              </button>
            </div>
          </div>
        ) : (
          <div>
            <h3 className="text-xl font-bold text-white">Drag & drop your CSV file here</h3>
            <p className="text-xs text-slate-500 mt-1">or</p>
            
            <label className="inline-block mt-4">
              <input type="file" accept=".csv" onChange={handleFileChange} className="hidden" />
              <span className="cursor-pointer px-6 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-sm shadow-lg shadow-purple-600/30 hover:from-purple-500 hover:to-indigo-500 transition inline-block">
                Browse File
              </span>
            </label>

            <p className="text-[11px] text-slate-500 mt-6">Maximum file size: 50 MB</p>
          </div>
        )}
      </div>

      {/* Template Download Section */}
      <div className="text-center pt-4">
        <p className="text-xs text-slate-400 mb-3">Don't have a CSV?</p>
        <button
          onClick={downloadSampleTemplate}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#181E30] border border-slate-700 text-purple-400 text-xs font-semibold hover:bg-slate-800 transition"
        >
          <Download className="w-4 h-4" />
          <span>Download PriceWise Template</span>
        </button>
      </div>
    </div>
  );
};
