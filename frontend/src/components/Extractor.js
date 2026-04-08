import React, { useState, useEffect } from 'react';
import { startExtract, getJobs } from '../api';

const card = { background:'#1e293b', borderRadius:12, padding:24, border:'1px solid #334155', marginBottom:16 };

const STATUS_COLORS = { running:'#fbbf24', done:'#34d399', error:'#f87171' };
const STATUS_ICONS  = { running:'⏳', done:'✅', error:'❌' };

export default function Extractor({ onDone }) {
  const [jobs, setJobs] = useState([]);
  const [days, setDays]      = useState(90);
  const [maxPerUser, setMax] = useState(500);

  const refresh = () => getJobs().then(r => setJobs(r.jobs)).catch(() => {});

  useEffect(() => {
    refresh();
    const iv = setInterval(refresh, 5000);
    return () => clearInterval(iv);
  }, []);

  const launch = async (type) => {
    try {
      await startExtract(type, { days_back: days, max_per_user: maxPerUser });
      refresh();
    } catch (e) {
      alert('Error: ' + (e.response?.data?.detail || e.message));
    }
  };

  const activeJob = jobs.find(j => j.status === 'running');

  return (
    <div>
      <h2 style={{ color:'#f1f5f9', fontSize:22, fontWeight:700, marginBottom:20 }}>Extracción de Datos</h2>

      {/* Parámetros */}
      <div style={card}>
        <h3 style={{ color:'#e2e8f0', marginBottom:16, fontSize:15 }}>Parámetros</h3>
        <div style={{ display:'flex', gap:20, flexWrap:'wrap' }}>
          <Param label="Período (días)" value={days} onChange={setDays} min={7} max={365} />
          <Param label="Máx. registros por usuario" value={maxPerUser} onChange={setMax} min={50} max={2000} />
        </div>
      </div>

      {/* Botones de extracción */}
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16, marginBottom:24 }}>
        <ExtractCard
          icon="📧" title="Correos Electrónicos"
          desc="Extrae metadata: quién envía a quién, cuándo, importancia. Sin contenido de mensajes."
          color="#38bdf8"
          loading={activeJob?.type === 'emails'}
          onStart={() => launch('emails')}
        />
        <ExtractCard
          icon="📅" title="Agenda / Calendario"
          desc="Extrae reuniones: organizador, participantes, horario, duración. Sin asuntos ni descripción."
          color="#a78bfa"
          loading={activeJob?.type === 'calendar'}
          onStart={() => launch('calendar')}
        />
      </div>

      {/* Historial de jobs */}
      <div style={card}>
        <h3 style={{ color:'#e2e8f0', marginBottom:16, fontSize:15 }}>Historial de extracciones</h3>
        {jobs.length === 0 && (
          <div style={{ color:'#475569', textAlign:'center', padding:20 }}>
            Aún no se ha ejecutado ninguna extracción
          </div>
        )}
        {jobs.map(j => (
          <div key={j.id} style={{ display:'flex', justifyContent:'space-between', alignItems:'center',
                                    padding:'10px 0', borderBottom:'1px solid #334155' }}>
            <div style={{ display:'flex', alignItems:'center', gap:10 }}>
              <span>{STATUS_ICONS[j.status]}</span>
              <span style={{ color:'#e2e8f0', fontSize:14, textTransform:'capitalize' }}>{j.type}</span>
              <span style={{ color:STATUS_COLORS[j.status], fontSize:13, fontWeight:600 }}>{j.status}</span>
            </div>
            <div style={{ color:'#94a3b8', fontSize:13, textAlign:'right' }}>
              <span>{j.users_processed} usuarios · {j.records_found} registros</span>
              {j.started_at && (
                <div style={{ fontSize:11, color:'#475569' }}>
                  {new Date(j.started_at).toLocaleString()}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div style={{ ...card, background:'#0c4a6e', borderColor:'#075985' }}>
        <h3 style={{ color:'#7dd3fc', marginBottom:8, fontSize:14 }}>🔒 Privacidad</h3>
        <ul style={{ color:'#bae6fd', fontSize:13, lineHeight:2, paddingLeft:20 }}>
          <li>Solo se extrae metadata (remitente, destinatario, fecha/hora).</li>
          <li>El contenido de los mensajes <strong>nunca</strong> se almacena.</li>
          <li>Los asuntos de correos y reuniones <strong>no</strong> se guardan.</li>
          <li>Todos los datos se almacenan localmente en SQLite.</li>
        </ul>
      </div>
    </div>
  );
}

function Param({ label, value, onChange, min, max }) {
  return (
    <div style={{ display:'flex', flexDirection:'column', gap:6 }}>
      <label style={{ color:'#94a3b8', fontSize:13 }}>{label}</label>
      <input type="number" min={min} max={max} value={value}
        onChange={e => onChange(Math.min(max, Math.max(min, Number(e.target.value))))}
        style={{ width:120, background:'#334155', color:'#e2e8f0',
                 border:'1px solid #475569', borderRadius:6, padding:'6px 10px', fontSize:14 }} />
    </div>
  );
}

function ExtractCard({ icon, title, desc, color, loading, onStart }) {
  return (
    <div style={{ background:'#1e293b', borderRadius:12, padding:24, border:`1px solid ${color}44` }}>
      <div style={{ fontSize:32, marginBottom:8 }}>{icon}</div>
      <h3 style={{ color:'#f1f5f9', marginBottom:8 }}>{title}</h3>
      <p style={{ color:'#94a3b8', fontSize:13, lineHeight:1.6, marginBottom:20 }}>{desc}</p>
      <button
        onClick={onStart}
        disabled={loading}
        style={{ background: loading ? '#334155' : color, color: loading ? '#94a3b8' : '#0f172a',
                 border:'none', borderRadius:8, padding:'10px 20px',
                 fontSize:14, fontWeight:700, cursor: loading ? 'not-allowed' : 'pointer',
                 width:'100%', transition:'all .2s' }}>
        {loading ? '⏳ Extrayendo…' : `Extraer ${title}`}
      </button>
    </div>
  );
}

