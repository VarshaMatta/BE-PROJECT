import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Download, Eye, Package } from 'lucide-react';
import { useShop } from '../context/ShopContext';
import { StatusBadge } from '../components/common/Badge';
import API from '../services/api';

export const ProductsList = () => {
  const { activeShop } = useShop();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (activeShop) {
      fetchProducts();
    }
  }, [activeShop, statusFilter, searchQuery]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const params = {};
      if (statusFilter !== 'All') params.status_filter = statusFilter;
      if (searchQuery) params.search = searchQuery;

      const res = await API.get(`/shops/${activeShop.shop_id}/products`, { params });
      setProducts(res.data);
    } catch (err) {
      console.error('Failed to load products:', err);
    } finally {
      setLoading(false);
    }
  };

  const counts = {
    All: products.length,
    'ML Ready': products.filter(p => p.data_sufficiency_status === 'ML READY').length,
    'Limited Data': products.filter(p => p.data_sufficiency_status === 'LIMITED DATA').length,
    'Cold Start': products.filter(p => p.data_sufficiency_status === 'COLD START').length,
  };

  const exportCSV = () => {
    const headers = "Product ID,Product Name,Category,Price,Records,Price Points,Status\n";
    const rows = products.map(p => 
      `"${p.external_code}","${p.product_name}","${p.category}",${p.current_price},${p.record_count},${p.price_point_count},"${p.data_sufficiency_status}"`
    ).join("\n");
    const blob = new Blob([headers + rows], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `products_${activeShop?.shop_name || 'shop'}.csv`;
    a.click();
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Top Title & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Products</h1>
          <p className="text-sm text-slate-400 mt-1">All products found in your uploaded data.</p>
        </div>

        <button
          onClick={exportCSV}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-purple-600/20 text-purple-300 border border-purple-500/30 hover:bg-purple-600/30 font-semibold text-xs transition self-start sm:self-auto"
        >
          <Download className="w-4 h-4" />
          <span>Export CSV</span>
        </button>
      </div>

      {/* Filter Row: Search & Status Pills */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-[#121726] border border-slate-800 p-4 rounded-2xl">
        {/* Search Input */}
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search product..."
            className="w-full bg-[#181E30] border border-slate-700 rounded-xl pl-10 pr-4 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500"
          />
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 md:pb-0">
          {['All', 'ML Ready', 'Limited Data', 'Cold Start'].map((tab) => (
            <button
              key={tab}
              onClick={() => setStatusFilter(tab)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition ${
                statusFilter === tab
                  ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md shadow-purple-600/30'
                  : 'bg-[#181E30] text-slate-400 hover:text-slate-200 border border-slate-700/60'
              }`}
            >
              {tab} ({counts[tab] || 0})
            </button>
          ))}
        </div>
      </div>

      {/* Products Table Card */}
      <div className="bg-[#121726] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-[#181E30] text-xs font-semibold text-slate-400 border-b border-slate-800">
            <tr>
              <th className="px-6 py-4">Product</th>
              <th className="px-6 py-4">Category</th>
              <th className="px-6 py-4">Records</th>
              <th className="px-6 py-4">Price Points</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {products.length > 0 ? (
              products.map((p) => (
                <tr key={p.product_id} className="hover:bg-slate-900/40 transition">
                  <td className="px-6 py-4 font-semibold text-white">
                    <div>
                      <p className="text-sm font-bold">{p.product_name}</p>
                      <p className="text-[11px] text-slate-500">ID: {p.external_code} • ₹{p.current_price.toFixed(2)}</p>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-xs text-slate-400">{p.category}</td>
                  <td className="px-6 py-4 text-xs font-medium text-slate-300">{p.record_count}</td>
                  <td className="px-6 py-4 text-xs font-medium text-slate-300">{p.price_point_count}</td>
                  <td className="px-6 py-4">
                    <StatusBadge status={p.data_sufficiency_status} />
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button
                      onClick={() => navigate(`/products/${p.product_id}`)}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#181E30] border border-slate-700 text-purple-400 hover:text-white hover:bg-purple-600 text-xs font-semibold transition"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>View</span>
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-slate-500">
                  <Package className="w-10 h-10 mx-auto mb-2 text-slate-600" />
                  <p className="text-xs font-semibold">No products found</p>
                  <p className="text-[11px] text-slate-600 mt-1">Upload CSV data to populate products list.</p>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
