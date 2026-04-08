import React, { useState, useEffect } from 'react';
import { getStats } from '../api';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, LineChart, Line
} from 'recharts';

const card = {
  background:'#1e293b', borderRadius:12, padding:24,
  border:'1px solid #334155', marginBottom:20,
};

const metricCard = (color) => ({
  ...card,
  borderLeft: `4px solid ${color}`,
  display:'flex', flexDirection:'column', gap:4,
});

export default function Stats() {
  const [data, setData] = useState(null);
  const [days, setDays] = useState(90);

  useEffect(() => {
    setData(null);
    getStats(days).then(setData).catch(() => {});
  }, [days]);

  if (!data) return <div style={{ color:'#94a3b8', padding:40, textAlign:'center' }}>Cargando estadísticas…</div>;

  const totals = data.totals;
  const noData = totals.emails === 0 && totals.meetings === 0;

  return (
    <div>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:24 }}>
        <h2 style={{ color:'#f1f5f9', fontSize:22, fontWeight:700 }}>Estadísticas</h2>
        <select value={days} onChange={e => setDays(Number(e.target.value))}
          style={{ background:'#334155', color:'#e2e8f0', border:'1px solid #475569',
                   borderRadius:6, padding:'6px 12px', fontSize:14 }}>
          <option value={7}>Últimos 7 días</option>
          <option value={30}>Últimos 30 días</option>
          <option value={90}>Últimos 90 días</option>
          <option value={180}>Últimos 6 meses</option>
        </select>
      </div>

      {noData && (
        <div style={{ ...card, color:'#94a3b8', textAlign:'center', padding:48 }}>
          Sin datos aún. Ve a <strong style={{color:'#38bdf8'}}>⬇️ Extraer Datos</strong> para comenzar la extracción.
        </div>
      )}

      {/* Métricas */}
      <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(200px,1fr))', gap:16, marginBottom:20 }}>
        <MetricCard color="#38bdf8" label="Emails extraídos" value={totals.emails} icon="📧" />
        <MetricCard color="#a78bfa" label="Reuniones extraídas" value={totals.meetings} icon="📅" />
        <MetricCard color="#34d399" label="Usuarios enviadores" value={totals.email_senders} icon="👤" />
        <MetricCard color="#fb923c" label="Organizadores de reuniones" value={totals.meeting_organizers} icon="🗓️" />
      </div>

      {!noData && (
        <>
          {/* Actividad por hora */}
          <div style={card}>
            <h3 style={{ color:'#e2e8f0', marginBottom:16 }}>Actividad por hora del día</h3>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={data.activity_by_hour}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="hour" tick={{ fill:'#94a3b8', fontSize:11 }} tickFormatter={h => `${h}h`} />
                <YAxis tick={{ fill:'#94a3b8', fontSize:11 }} />
                <Tooltip contentStyle={{ background:'#1e293b', border:'1px solid #334155', color:'#e2e8f0' }} />
                <Legend wrapperStyle={{ color:'#94a3b8' }} />
                <Bar dataKey="emails" name="Emails" fill="#38bdf8" radius={[2,2,0,0]} />
                <Bar dataKey="meetings" name="Reuniones" fill="#a78bfa" radius={[2,2,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Actividad por día de semana */}
          <div style={card}>
            <h3 style={{ color:'#e2e8f0', marginBottom:16 }}>Actividad por día de la semana</h3>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={data.activity_by_dow}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="day" tick={{ fill:'#94a3b8', fontSize:12 }} />
                <YAxis tick={{ fill:'#94a3b8', fontSize:11 }} />
                <Tooltip contentStyle={{ background:'#1e293b', border:'1px solid #334155', color:'#e2e8f0' }} />
                <Legend wrapperStyle={{ color:'#94a3b8' }} />
                <Bar dataKey="emails" name="Emails" fill="#38bdf8" radius={[2,2,0,0]} />
                <Bar dataKey="meetings" name="Reuniones" fill="#a78bfa" radius={[2,2,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Top senders y organizers */}
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16 }}>
            <TopList title="Top enviadores de email" data={data.top_senders} color="#38bdf8" />
            <TopList title="Top organizadores de reuniones" data={data.top_organizers} color="#a78bfa" />
          </div>
        </>
      )}
    </div>
  );
}

function MetricCard({ color, label, value, icon }) {
  return (
    <div style={{ background:'#1e293b', borderRadius:12, padding:'20px 24px',
                  border:`1px solid ${color}33`, borderLeft:`4px solid ${color}` }}>
      <div style={{ fontSize:24, marginBottom:4 }}>{icon}</div>
      <div style={{ fontSize:28, fontWeight:700, color }}>{(value ?? 0).toLocaleString()}</div>
      <div style={{ color:'#94a3b8', fontSize:13 }}>{label}</div>
    </div>
  );
}

function TopList({ title, data, color }) {
  const max = data[0]?.count || 1;
  return (
    <div style={{ background:'#1e293b', borderRadius:12, padding:20, border:'1px solid #334155' }}>
      <h3 style={{ color:'#e2e8f0', marginBottom:16, fontSize:15 }}>{title}</h3>
      {data.map((row, i) => (
        <div key={i} style={{ marginBottom:8 }}>
          <div style={{ display:'flex', justifyContent:'space-between', marginBottom:3 }}>
            <span style={{ color:'#cbd5e1', fontSize:13, overflow:'hidden', textOverflow:'ellipsis',
                           whiteSpace:'nowrap', maxWidth:'75%' }}>
              {row.email.split('@')[0]}
            </span>
            <span style={{ color, fontSize:13, fontWeight:600 }}>{row.count}</span>
          </div>
          <div style={{ background:'#334155', borderRadius:4, height:4 }}>
            <div style={{ background:color, borderRadius:4, height:4,
                          width:`${(row.count/max)*100}%`, transition:'width .4s' }} />
          </div>
        </div>
      ))}
    </div>
  );
}
