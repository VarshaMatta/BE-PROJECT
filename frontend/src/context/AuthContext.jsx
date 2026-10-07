import React, { createContext, useContext, useState, useEffect } from 'react';
import API from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('pw_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      fetchProfile();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchProfile = async () => {
    try {
      const res = await API.get('/auth/me');
      setUser(res.data);
    } catch (err) {
      console.error('Failed to fetch user profile:', err);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    const res = await API.post('/auth/login', { email, password });
    const jwtToken = res.data.access_token;
    localStorage.setItem('pw_token', jwtToken);
    setToken(jwtToken);
    const profileRes = await API.get('/auth/me', {
      headers: { Authorization: `Bearer ${jwtToken}` }
    });
    setUser(profileRes.data);
    return profileRes.data;
  };

  const register = async (name, email, password) => {
    const res = await API.post('/auth/register', { name, email, password });
    const jwtToken = res.data.access_token;
    localStorage.setItem('pw_token', jwtToken);
    setToken(jwtToken);
    const profileRes = await API.get('/auth/me', {
      headers: { Authorization: `Bearer ${jwtToken}` }
    });
    setUser(profileRes.data);
    return profileRes.data;
  };

  const logout = () => {
    localStorage.removeItem('pw_token');
    localStorage.removeItem('pw_active_shop_id');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
