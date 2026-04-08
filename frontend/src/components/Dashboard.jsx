import React, { useState, useEffect } from 'react';
import { logout, getStatus, getJobs } from '../api';
import Stats from './Stats.jsx';
import Extractor from './Extractor.jsx';
import NetworkView from './NetworkView.jsx';
import PairsTable from './PairsTable.jsx';

const NAV = [
  { id: 'stats',   label: '📊 Estadísticas' },
  { id: 'network', label: '🕸️ Red Organizacional' },
  { id: 'pairs',   label: '🔗 Pares de Comunicación' },
  { id: 'extract', label: '⬇️ Extraer Datos' },
];

const S = {
  layout: { display:'flex', flexDirection:'column', minHeight:'100vh', background:'#0f172a' },
  header: { background:'#1e293b', borderBottom:'1px solid #334155', padding:'0 32px',
            display:'flex', alignItems:'center', justifyContent:'space-between', height:56 },
  logo:   { fontSize:20, fontWeight:800, color:'#38bdf8' },
  nav:    { display:'flex', gap:4 },
  navBtn: (active) => ({
    padding:'6px 14px', borderRadius:6, border:'none', cursor:'pointer', fontSize:14,
    background: active ? '#0284c7' : 'transparent',
    color: active ? '#fff' : '#94a3b8',
    transition:'all .2s',
  }),
  userArea: { display:'flex', alignItems:'center', gap:12 },
  email:  { color:'#94a3b8', fontSize:13 },
  logoutBtn: { padding:'6px 14px', background:'#7f1d1d', color:'#fca5a5',
               border:'none', borderRadius:6, cursor:'pointer', fontSize:13 },
  content: { flex:1, padding:'24px 32px' },
  statusBar: { background:'#0c4a6e', borderBottom:'1px solid #075985',
               padding:'8px 32px', fontSize:13, color:'#7dd3fc',
               display:'flex', gap:24 },
};

export default function Dashboard({ user, onLogout }) {
  const [tab, setTab] = useState('stats');
  const [status, setStatus] = useState(null);
  const [jobs, setJobs] = useState([]);

  const refreshStatus = () => {
    getStatus().then(setStatus).catch(() => {});
    getJobs().then(r => setJobs(r.jobs)).catch(() => {});
  };

  useEffect(() => {
    refreshStatus();
    const iv = setInterval(refreshStatus, 8000);
    return () => clearInterval(iv);
  }, []);

  const handleLogout = async () => {
    try { await logout(); } catch (_) {}
    onLogout();
  };

  const runningJob = jobs.find(j => j.status === 'running');

  return (
    <div style={S.layout}>
      <header style={S.header}>
        <div style={{ display:'flex', alignItems:'center', gap:24 }}>
          <div style={S.logo}>PassiveData</div>
          <nav style={S.nav}>
            {NAV.map(n => (
              <button key={n.id} style={S.navBtn(tab === n.id)} onClick={() => setTab(n.id)}>
                {n.label}
              </button>
            ))}
          </nav>
        </div>
        <div style={S.userArea}>
          <span style={S.email}>{user.email}</span>
          <button style={S.logoutBtn} onClick={handleLogout}>Salir</button>
        </div>
      </header>

      {/* Barra de estado */}
      {status && (
        <div style={S.statusBar}>
          <span>📧 {status.email_records ?? 0} emails</span>
          <span>📅 {status.calendar_records ?? 0} reuniones</span>
          {runningJob && (
            <span style={{ color:'#fbbf24' }}>
              ⏳ Extrayendo {runningJob.type}… {runningJob.users_processed} usuarios / {runningJob.records_found} registros
            </span>
          )}
        </div>
      )}

      <main style={S.content}>
        {tab === 'stats'   && <Stats />}
        {tab === 'network' && <NetworkView />}
        {tab === 'pairs'   && <PairsTable />}
        {tab === 'extract' && <Extractor onDone={refreshStatus} />}
      </main>
    </div>
  );
}
