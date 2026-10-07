import React, { createContext, useContext, useState, useEffect } from 'react';
import API from '../services/api';
import { useAuth } from './AuthContext';

const ShopContext = createContext();

export const ShopProvider = ({ children }) => {
  const { user } = useAuth();
  const [shops, setShops] = useState([]);
  const [activeShop, setActiveShop] = useState(null);
  const [loadingShops, setLoadingShops] = useState(true);

  useEffect(() => {
    if (user) {
      loadShops();
    } else {
      setShops([]);
      setActiveShop(null);
      setLoadingShops(false);
    }
  }, [user]);

  const loadShops = async () => {
    try {
      setLoadingShops(true);
      const res = await API.get('/shops');
      setShops(res.data);

      const savedShopId = localStorage.getItem('pw_active_shop_id');
      if (savedShopId && res.data.some(s => s.shop_id === parseInt(savedShopId))) {
        const found = res.data.find(s => s.shop_id === parseInt(savedShopId));
        setActiveShop(found);
      } else if (res.data.length > 0) {
        setActiveShop(res.data[0]);
        localStorage.setItem('pw_active_shop_id', res.data[0].shop_id);
      } else {
        setActiveShop(null);
      }
    } catch (err) {
      console.error('Failed to load user shops:', err);
    } finally {
      setLoadingShops(false);
    }
  };

  const selectShop = (shop) => {
    setActiveShop(shop);
    localStorage.setItem('pw_active_shop_id', shop.shop_id);
  };

  const createShop = async (shop_name, business_type) => {
    const res = await API.post('/shops', { shop_name, business_type });
    await loadShops();
    selectShop(res.data);
    return res.data;
  };

  return (
    <ShopContext.Provider value={{ shops, activeShop, loadingShops, selectShop, createShop, refreshShops: loadShops }}>
      {children}
    </ShopContext.Provider>
  );
};

export const useShop = () => useContext(ShopContext);
