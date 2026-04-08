import React, { useState, useEffect } from 'react';
import { getPairs } from '../api';

const card = { background:'#1e293b', borderRadius:12, padding:24, border:'1px solid #334155' };

export default function PairsTable() {
  const [data, setData] = useState(null);
  const [days, setDays] = useState(90);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    setData(null);
    getPairs(days, 100).then(setData).catch(() => {});
  }, [days]);

  const pairs = data?.pairs ?? [];
  const filtered = filter
    ? pairs.filter(p => p.from.includes(filter) || p.to.includes(filter))
    : pairs;
  const maxTotal = filtered[0]?.total || 1;

  return (
    <div>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:20 }}>
        <h2 style={{ color:'#f1f5f9', fontSize:22, fontWeight:700 }}>Pares de Comunicación</h2>
        <div style={{ display:'flex', gap:8 }}>
          <input placeholder="Filtrar por email…" value={filter} onChange={e => setFilter(e.target.value)}
            style={{ background:'#334155', color:'#e2e8f0', border:'1px solid #475569',
                     borderRadius:6, padding:'6px 12px', fontSize:14, width:200 }} />
          <select value={days} onChange={e => setDays(Number(e.target.value))}
            style={{ background:'#334155', color:'#e2e8f0', border:'1px solid #475569',
                     borderRadius:6, padding:'6px 10px', fontSize:14 }}>
            <option value={7}>7 días</option>
            <option value={30}>30 días</option>
            <option value={90}>90 días</option>
            <option value={180}>6 meses</option>
          </select>
        </div>
      </div>

      <div style={card}>
        {!data && <div style={{ color:'#94a3b8', textAlign:'center', padding:32 }}>Cargando…</div>}
        {data && filtered.length === 0 && (
          <div style={{ color:'#94a3b8', textAlign:'center', padding:32 }}>
            Sin datos. Extrae emails o agenda primero.
          </div>
        )}
        {data && filtered.length > 0 && (
          <table style={{ width:'100%', borderCollapse:'collapse' }}>
            <thead>
              <tr>
                {['#','De','Para','📧 Emails','📅 Reuniones','Total','Barra'].map(h => (
                  <th key={h} style={{ textAlign:'left', color:'#94a3b8', fontSize:12,
                                       textTransform:'uppercase', letterSpacing:.5,
                                       padding:'0 12px 12px', borderBottom:'1px solid #334155' }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map((p, i) => (
                <tr key={i} style={{ borderBottom:'1px solid #1e293b' }}
                  onMouseEnter={e => e.currentTarget.style.background = '#ffffff08'}
                  onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
                  <td style={{ padding:'10px 12px', color:'#475569', fontSize:13 }}>{i + 1}</td>
                  <td style={{ padding:'10px 12px', color:'#cbd5e1', fontSize:13, maxWidth:180, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>
                    {p.from.split('@')[0]}<span style={{ color:'#475569' }}>@{p.from.split('@')[1]}</span>
                  </td>
                  <td style={{ padding:'10px 12px', color:'#cbd5e1', fontSize:13, maxWidth:180, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>
                    {p.to.split('@')[0]}<span style={{ color:'#475569' }}>@{p.to.split('@')[1]}</span>
                  </td>
                  <td style={{ padding:'10px 12px', color:'#38bdf8', fontSize:14, fontWeight:600 }}>{p.emails}</td>
                  <td style={{ padding:'10px 12px', color:'#a78bfa', fontSize:14, fontWeight:600 }}>{p.meetings}</td>
                  <td style={{ padding:'10px 12px', color:'#f1f5f9', fontSize:14, fontWeight:700 }}>{p.total}</td>
                  <td style={{ padding:'10px 12px', width:120 }}>
                    <div style={{ background:'#334155', borderRadius:4, height:6 }}>
                      <div style={{ background:'linear-gradient(90deg,#38bdf8,#a78bfa)',
                                    borderRadius:4, height:6, width:`${(p.total/maxTotal)*100}%` }} />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
