import React, { useState, useEffect } from 'react';
import './CommunicationNetwork.css';
import { apiService } from '../services/api';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Legend
} from 'recharts';

function CommunicationNetwork() {
  const [networkData, setNetworkData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [daysBack, setDaysBack] = useState(30);
  const [minInteractions, setMinInteractions] = useState(1);

  useEffect(() => {
    loadNetworkData();
  }, [daysBack, minInteractions]);

  const loadNetworkData = async () => {
    try {
      setLoading(true);
      const data = await apiService.getCommunicationNetwork(daysBack, minInteractions);
      setNetworkData(data);
    } catch (error) {
      console.error('Error al cargar red de comunicación:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading">Cargando red de comunicación...</div>
      </div>
    );
  }

  if (!networkData) {
    return (
      <div className="card">
        <h2>No hay datos de red disponibles</h2>
        <p>Primero extrae datos desde la pestaña "Extracción de Datos"</p>
      </div>
    );
  }

  const emailNetwork = networkData.email_network || [];
  const meetingNetwork = networkData.meeting_network || [];

  // Preparar datos para visualización
  const emailConnections = emailNetwork.slice(0, 20).map((conn, idx) => ({
    id: idx,
    from: conn.from.split('@')[0],
    to: conn.to.split('@')[0],
    count: conn.count
  }));

  const meetingConnections = meetingNetwork.slice(0, 20).map((conn, idx) => ({
    id: idx,
    from: conn.from.split('@')[0],
    to: conn.to.split('@')[0],
    count: conn.count
  }));

  return (
    <div className="communication-network">
      <div className="network-header">
        <h2>Red de Comunicación</h2>
        <p className="subtitle-text">
          Visualiza las conexiones de comunicación entre usuarios de la organización
        </p>
      </div>

      {/* Filtros */}
      <div className="card filters-card">
        <h3>Filtros</h3>
        <div className="filters">
          <div className="filter-group">
            <label>Período (días):</label>
            <select value={daysBack} onChange={(e) => setDaysBack(Number(e.target.value))}>
              <option value={7}>Últimos 7 días</option>
              <option value={30}>Últimos 30 días</option>
              <option value={60}>Últimos 60 días</option>
              <option value={90}>Últimos 90 días</option>
            </select>
          </div>
          <div className="filter-group">
            <label>Interacciones mínimas:</label>
            <input
              type="number"
              min="1"
              value={minInteractions}
              onChange={(e) => setMinInteractions(Number(e.target.value))}
            />
          </div>
        </div>
      </div>

      {/* Estadísticas */}
      <div className="network-stats">
        <div className="stat-card">
          <h3>Conexiones por Email</h3>
          <p className="stat-number">{emailNetwork.length}</p>
          <span className="stat-label">conexiones únicas</span>
        </div>
        <div className="stat-card">
          <h3>Conexiones por Reuniones</h3>
          <p className="stat-number">{meetingNetwork.length}</p>
          <span className="stat-label">conexiones únicas</span>
        </div>
      </div>

      {/* Tabla de conexiones por email */}
      {emailConnections.length > 0 && (
        <div className="card">
          <h3>Top 20 - Conexiones por Email</h3>
          <div className="connections-table">
            <table>
              <thead>
                <tr>
                  <th>De</th>
                  <th>Para</th>
                  <th>Número de Emails</th>
                </tr>
              </thead>
              <tbody>
                {emailConnections.map((conn) => (
                  <tr key={conn.id}>
                    <td>{conn.from}</td>
                    <td>{conn.to}</td>
                    <td>
                      <span className="count-badge">{conn.count}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tabla de conexiones por reuniones */}
      {meetingConnections.length > 0 && (
        <div className="card">
          <h3>Top 20 - Conexiones por Reuniones</h3>
          <div className="connections-table">
            <table>
              <thead>
                <tr>
                  <th>Organizador</th>
                  <th>Participante</th>
                  <th>Número de Reuniones</th>
                </tr>
              </thead>
              <tbody>
                {meetingConnections.map((conn) => (
                  <tr key={conn.id}>
                    <td>{conn.from}</td>
                    <td>{conn.to}</td>
                    <td>
                      <span className="count-badge count-badge-meeting">{conn.count}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {emailNetwork.length === 0 && meetingNetwork.length === 0 && (
        <div className="card">
          <p>No se encontraron conexiones con los filtros actuales.</p>
          <p>Intenta ajustar el período o reducir el mínimo de interacciones.</p>
        </div>
      )}
    </div>
  );
}

export default CommunicationNetwork;
