import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Store, ArrowRight, Package, FileText, Calendar, Building } from 'lucide-react';
import { useShop } from '../context/ShopContext';

export const Shops = () => {
  const { shops, activeShop, selectShop, createShop } = useShop();
  const [showModal, setShowModal] = useState(false);
  const [shopName, setShopName] = useState('');
  const [businessType, setBusinessType] = useState('Grocery Store');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!shopName) return;
    setLoading(true);
    try {
      await createShop(shopName, businessType);
      setShowModal(false);
      setShopName('');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenShop = (s) => {
    selectShop(s);
    navigate('/dashboard');
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Top Header Row */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">My Shops</h1>
          <p className="text-sm text-slate-400">Manage your shops or create a new one.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-sm shadow-lg shadow-purple-600/30 hover:from-purple-500 hover:to-indigo-500 transition"
        >
          <Plus className="w-4 h-4" />
          <span>Add Shop</span>
        </button>
      </div>

      {/* Grid of Shop Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {shops.map((s) => (
          <div
            key={s.shop_id}
            className={`bg-[#121726] border ${
              activeShop?.shop_id === s.shop_id ? 'border-purple-500/80 shadow-lg shadow-purple-500/10' : 'border-slate-800'
            } rounded-2xl p-6 transition duration-200 hover:border-slate-700 flex flex-col justify-between`}
          >
            <div>
              {/* Store Thumbnail / Visual Cover */}
              <div className="h-40 w-full rounded-xl bg-gradient-to-tr from-slate-900 to-purple-950/40 border border-slate-800 flex items-center justify-center mb-5 relative overflow-hidden group">
                <Store className="w-16 h-16 text-purple-500/40 group-hover:scale-110 transition duration-300" />
                {activeShop?.shop_id === s.shop_id && (
                  <span className="absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-bold bg-purple-600 text-white shadow">
                    Active Shop
                  </span>
                )}
              </div>

              {/* Shop Title & Type */}
              <h2 className="text-xl font-bold text-white">{s.shop_name}</h2>
              <p className="text-xs text-slate-400 flex items-center gap-1.5 mt-1">
                <Building className="w-3.5 h-3.5 text-purple-400" />
                {s.business_type}
              </p>

              {/* Stats row */}
              <div className="grid grid-cols-3 gap-2 mt-6 py-4 px-4 bg-[#181E30] rounded-xl border border-slate-800 text-center">
                <div>
                  <p className="text-lg font-extrabold text-white">{s.product_count || 0}</p>
                  <p className="text-[11px] text-slate-400 font-medium">Products</p>
                </div>
                <div>
                  <p className="text-lg font-extrabold text-white">{(s.sales_record_count || 0).toLocaleString()}</p>
                  <p className="text-[11px] text-slate-400 font-medium">Sales Records</p>
                </div>
                <div>
                  <p className="text-sm font-bold text-slate-300 mt-1">{s.last_upload || 'Jan 2024'}</p>
                  <p className="text-[11px] text-slate-400 font-medium">Last Upload</p>
                </div>
              </div>
            </div>

            {/* Action button */}
            <button
              onClick={() => handleOpenShop(s)}
              className="w-full mt-6 py-3 px-4 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-sm flex items-center justify-center gap-2 shadow-lg shadow-purple-600/25 hover:from-purple-500 hover:to-indigo-500 transition"
            >
              <span>Open Shop</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>

      {/* Modal for creating a new shop */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#121726] border border-slate-800 rounded-2xl p-6 w-full max-w-md shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-1">Create New Shop</h3>
            <p className="text-xs text-slate-400 mb-4">Set up a new retail outlet in PriceWise.</p>

            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Shop Name</label>
                <input
                  type="text"
                  required
                  value={shopName}
                  onChange={(e) => setShopName(e.target.value)}
                  placeholder="e.g. City Grocery"
                  className="w-full bg-[#181E30] border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Business Type</label>
                <select
                  value={businessType}
                  onChange={(e) => setBusinessType(e.target.value)}
                  className="w-full bg-[#181E30] border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
                >
                  <option value="Grocery Store">Grocery Store</option>
                  <option value="Retail Store">Retail Store</option>
                  <option value="Supermarket">Supermarket</option>
                  <option value="Electronics">Electronics</option>
                  <option value="Pharmacy">Pharmacy</option>
                </select>
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-5 py-2.5 rounded-xl bg-purple-600 text-white font-semibold text-xs shadow-lg shadow-purple-600/30 hover:bg-purple-500"
                >
                  {loading ? 'Creating...' : 'Create Shop'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
