import React, { useState, useEffect, useRef, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { getNetwork } from '../api';

const card = { background:'#1e293b', borderRadius:12, padding:16, border:'1px solid #334155' };

const DEPT_COLORS = [
  '#38bdf8','#a78bfa','#34d399','#fb923c','#f472b6',
  '#facc15','#60a5fa','#f87171','#4ade80','#e879f9',
];

export default function NetworkView() {
  const [graphData, setGraphData] = useState({ nodes:[], links:[] });
  const [source, setSource] = useState('both');
  const [days, setDays]     = useState(90);
  const [minW, setMinW]     = useState(2);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState(null);
  const fgRef = useRef();

  const deptMap = useRef({});
  const colorIdx = useRef(0);

  const deptColor = (dept) => {
    if (!dept) return '#94a3b8';
    if (!deptMap.current[dept]) {
      deptMap.current[dept] = DEPT_COLORS[colorIdx.current % DEPT_COLORS.length];
      colorIdx.current++;
    }
    return deptMap.current[dept];
  };

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getNetwork({ source, days, min_weight: minW });
      const nodes = data.nodes.map(n => ({
        id: n.id,
        label: n.label,
        department: n.department,
        job_title: n.job_title,
        degree: n.degree,
        color: deptColor(n.department),
      }));
      const links = data.edges.map(e => ({
        source: e.source,
        target: e.target,
        value: e.total,
        emails: e.email_count,
        meetings: e.calendar_count,
      }));
      setGraphData({ nodes, links });
    } catch (_) {}
    setLoading(false);
  }, [source, days, minW]);

  useEffect(() => { load(); }, [load]);

  const noData = graphData.nodes.length === 0;

  return (
    <div>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:16 }}>
        <h2 style={{ color:'#f1f5f9', fontSize:22, fontWeight:700 }}>Red Organizacional</h2>
        <div style={{ display:'flex', gap:8 }}>
          <Select value={source} onChange={setSource} options={[
            ['both','Email + Calendario'],['email','Solo Email'],['calendar','Solo Calendario']
          ]} />
          <Select value={days} onChange={v => setDays(Number(v))} options={[
            [7,'7 días'],[30,'30 días'],[90,'90 días'],[180,'6 meses']
          ]} />
          <div style={{ display:'flex', alignItems:'center', gap:6 }}>
            <span style={{ color:'#94a3b8', fontSize:13 }}>Mín. interacciones:</span>
            <input type="number" min={1} max={50} value={minW}
              onChange={e => setMinW(Math.max(1, Number(e.target.value)))}
              style={{ width:56, background:'#334155', color:'#e2e8f0',
                       border:'1px solid #475569', borderRadius:6, padding:'6px 8px', fontSize:14 }} />
          </div>
          <button onClick={load} style={{ background:'#0284c7', color:'#fff', border:'none',
            borderRadius:6, padding:'6px 14px', cursor:'pointer', fontSize:14 }}>
            Actualizar
          </button>
        </div>
      </div>

      <div style={{ display:'grid', gridTemplateColumns:'1fr 260px', gap:16 }}>
        {/* Grafo */}
        <div style={{ ...card, height:560, position:'relative', overflow:'hidden' }}>
          {loading && (
            <div style={{ position:'absolute', inset:0, display:'flex', alignItems:'center',
                          justifyContent:'center', background:'#1e293bcc', zIndex:10, color:'#94a3b8' }}>
              Cargando red…
            </div>
          )}
          {noData && !loading ? (
            <div style={{ display:'flex', alignItems:'center', justifyContent:'center',
                          height:'100%', color:'#94a3b8', flexDirection:'column', gap:8 }}>
              <div style={{ fontSize:40 }}>🕸️</div>
              <div>Sin datos. Extrae correos o agenda primero.</div>
            </div>
          ) : (
            <ForceGraph2D
              ref={fgRef}
              graphData={graphData}
              nodeLabel={n => `${n.label}${n.department ? `\n${n.department}` : ''}${n.job_title ? `\n${n.job_title}` : ''}\nConexiones: ${n.degree}`}
              nodeColor={n => n.color}
              nodeRelSize={4}
              nodeVal={n => Math.max(1, Math.log(n.degree + 1) * 3)}
              linkWidth={l => Math.min(6, 1 + Math.log(l.value))}
              linkColor={() => '#334155'}
              linkDirectionalArrowLength={3}
              linkDirectionalArrowRelPos={1}
              backgroundColor="#0f172a"
              onNodeClick={node => setSelected(node)}
              nodeCanvasObject={(node, ctx, globalScale) => {
                const r = Math.max(4, Math.log(node.degree + 1) * 3);
                ctx.beginPath();
                ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
                ctx.fillStyle = node.color;
                ctx.fill();
                if (globalScale > 1.5) {
                  const label = node.label.split('@')[0];
                  ctx.font = `${10 / globalScale}px sans-serif`;
                  ctx.fillStyle = '#e2e8f0';
                  ctx.textAlign = 'center';
                  ctx.fillText(label, node.x, node.y + r + 8 / globalScale);
                }
              }}
            />
          )}
        </div>

        {/* Panel lateral */}
        <div style={{ display:'flex', flexDirection:'column', gap:12 }}>
          {/* Info del nodo seleccionado */}
          <div style={card}>
            <div style={{ color:'#94a3b8', fontSize:12, marginBottom:8, textTransform:'uppercase', letterSpacing:1 }}>
              {selected ? 'Nodo seleccionado' : 'Haz clic en un nodo'}
            </div>
            {selected ? (
              <>
                <div style={{ color:'#f1f5f9', fontWeight:600, marginBottom:4 }}>{selected.label}</div>
                {selected.department && <div style={{ color:'#94a3b8', fontSize:13 }}>🏢 {selected.department}</div>}
                {selected.job_title  && <div style={{ color:'#94a3b8', fontSize:13 }}>💼 {selected.job_title}</div>}
                <div style={{ color:'#38bdf8', fontSize:13, marginTop:4 }}>🔗 {selected.degree} interacciones</div>
              </>
            ) : (
              <div style={{ color:'#475569', fontSize:13 }}>Selecciona un nodo para ver sus detalles</div>
            )}
          </div>

          {/* Leyenda de departamentos */}
          {Object.keys(deptMap.current).length > 0 && (
            <div style={card}>
              <div style={{ color:'#94a3b8', fontSize:12, marginBottom:10, textTransform:'uppercase', letterSpacing:1 }}>
                Departamentos
              </div>
              {Object.entries(deptMap.current).map(([dept, color]) => (
                <div key={dept} style={{ display:'flex', alignItems:'center', gap:8, marginBottom:6 }}>
                  <div style={{ width:10, height:10, borderRadius:'50%', background:color, flexShrink:0 }} />
                  <span style={{ color:'#cbd5e1', fontSize:12, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>
                    {dept || '(sin departamento)'}
                  </span>
                </div>
              ))}
            </div>
          )}

          {/* Resumen */}
          <div style={card}>
            <div style={{ color:'#94a3b8', fontSize:12, marginBottom:8, textTransform:'uppercase', letterSpacing:1 }}>Resumen</div>
            <div style={{ color:'#38bdf8', fontSize:20, fontWeight:700 }}>{graphData.nodes.length}</div>
            <div style={{ color:'#94a3b8', fontSize:12 }}>personas en la red</div>
            <div style={{ color:'#a78bfa', fontSize:20, fontWeight:700, marginTop:8 }}>{graphData.links.length}</div>
            <div style={{ color:'#94a3b8', fontSize:12 }}>conexiones</div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Select({ value, onChange, options }) {
  return (
    <select value={value} onChange={e => onChange(e.target.value)}
      style={{ background:'#334155', color:'#e2e8f0', border:'1px solid #475569',
               borderRadius:6, padding:'6px 10px', fontSize:14 }}>
      {options.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
    </select>
  );
}
