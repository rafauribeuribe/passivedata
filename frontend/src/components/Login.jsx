import React, { useState, useEffect } from 'react';
import { getStatus, getLoginUrl } from '../api';

const S = {
  page: { minHeight:'100vh', background:'linear-gradient(135deg,#0f172a 0%,#1e293b 100%)',
          display:'flex', alignItems:'center', justifyContent:'center' },
  card: { background:'#1e293b', borderRadius:16, padding:'48px 40px', maxWidth:480, width:'100%',
          boxShadow:'0 25px 50px rgba(0,0,0,.5)', border:'1px solid #334155' },
  logo: { fontSize:36, fontWeight:800, color:'#38bdf8', marginBottom:8 },
  sub:  { color:'#94a3b8', marginBottom:32, lineHeight:1.6 },
  btn:  { display:'block', width:'100%', padding:'14px 24px', background:'#0284c7', color:'#fff',
          border:'none', borderRadius:8, fontSize:16, fontWeight:600, cursor:'pointer',
          transition:'background .2s' },
  btnHov:{ background:'#0369a1' },
  warn: { background:'#7f1d1d', border:'1px solid #991b1b', borderRadius:8, padding:'12px 16px',
          color:'#fca5a5', fontSize:14, marginBottom:16 },
  info: { background:'#0c4a6e', border:'1px solid #075985', borderRadius:8, padding:'12px 16px',
          color:'#7dd3fc', fontSize:14, marginTop:24 },
  dot:  { display:'inline-block', width:8, height:8, borderRadius:'50%', marginRight:8 },
};

export default function Login() {
  const [status, setStatus] = useState(null);
  const [hover, setHover] = useState(false);

  useEffect(() => { getStatus().then(setStatus).catch(() => {}); }, []);

  const handleLogin = async () => {
    try {
      const url = await getLoginUrl();
      window.location.href = url;
    } catch (e) {
      alert('Error: ' + (e.response?.data?.detail || e.message));
    }
  };

  const configured = status?.configured;
  const hasData = status && (status.email_records > 0 || status.calendar_records > 0);

  return (
    <div style={S.page}>
      <div style={S.card}>
        <div style={S.logo}>PassiveData</div>
        <p style={S.sub}>
          Análisis de redes organizacionales a partir de correos y agenda
          de Microsoft 365.
        </p>

        {status && !configured && (
          <div style={S.warn}>
            ⚠️ Azure no configurado. Edita el archivo <code>.env</code> con
            tus credenciales de App Registration.
          </div>
        )}

        <button
          style={{ ...S.btn, ...(hover ? S.btnHov : {}),
                   ...(configured === false ? { opacity:.5, cursor:'not-allowed' } : {}) }}
          onMouseEnter={() => setHover(true)}
          onMouseLeave={() => setHover(false)}
          onClick={handleLogin}
          disabled={configured === false}
        >
          🔑 &nbsp; Iniciar sesión con Microsoft 365
        </button>

        {status && (
          <div style={S.info}>
            <div style={{ marginBottom:6, fontWeight:600 }}>Estado del sistema</div>
            <div>
              <span style={{ ...S.dot, background: configured ? '#22c55e' : '#ef4444' }} />
              Azure {configured ? 'configurado' : 'sin configurar'}
            </div>
            {hasData && (
              <div style={{ marginTop:4, color:'#bae6fd' }}>
                📊 {status.email_records} emails · {status.calendar_records} reuniones en base de datos
              </div>
            )}
          </div>
        )}

        <div style={{ marginTop:24, fontSize:12, color:'#475569', lineHeight:1.8 }}>
          <strong style={{ color:'#64748b' }}>Permisos requeridos en Azure:</strong>
          <div>Mail.Read · Calendars.Read · User.ReadBasic.All</div>
        </div>
      </div>
    </div>
  );
}
