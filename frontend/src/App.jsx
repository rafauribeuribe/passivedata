import React, { useState, useEffect } from 'react';
import { getStatus } from './api';
import Login from './components/Login.jsx';
import Dashboard from './components/Dashboard.jsx';

export default function App() {
  const [auth, setAuth] = useState(null);   // { token, email, name }
  const [loading, setLoading] = useState(true);

  // Leer token de URL (después del callback de Microsoft)
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    const email = params.get('email');
    const name  = params.get('name');
    if (token) {
      const user = { token, email, name };
      sessionStorage.setItem('auth', JSON.stringify(user));
      setAuth(user);
      window.history.replaceState({}, '', '/');
    } else {
      const saved = sessionStorage.getItem('auth');
      if (saved) setAuth(JSON.parse(saved));
    }
    setLoading(false);
  }, []);

  const handleLogout = () => {
    sessionStorage.removeItem('auth');
    setAuth(null);
  };

  if (loading) return <Splash text="Cargando…" />;

  return auth
    ? <Dashboard user={auth} onLogout={handleLogout} />
    : <Login />;
}

export function Splash({ text }) {
  return (
    <div style={{ display:'flex', alignItems:'center', justifyContent:'center',
                  height:'100vh', flexDirection:'column', gap:16 }}>
      <div style={{ fontSize:32, fontWeight:700, color:'#38bdf8' }}>PassiveData</div>
      <div style={{ color:'#94a3b8' }}>{text}</div>
    </div>
  );
}
