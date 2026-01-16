import React from 'react';
import './Statistics.css';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const COLORS = ['#0078d4', '#106ebe', '#2b88d8', '#50a2e6', '#74bcf4'];

function Statistics({ stats, loading, onRefresh }) {
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading">Cargando estadísticas...</div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="card">
        <h2>No hay datos disponibles</h2>
        <p>Comienza extrayendo datos desde la pestaña "Extracción de Datos"</p>
      </div>
    );
  }

  const totals = stats.totals || { emails: 0, calendar_events: 0, teams_messages: 0 };
  const topSenders = stats.top_email_senders || [];
  const topOrganizers = stats.top_meeting_organizers || [];

  const totalData = [
    { name: 'Correos', value: totals.emails, color: '#0078d4' },
    { name: 'Eventos', value: totals.calendar_events, color: '#106ebe' },
    { name: 'Chats', value: totals.teams_messages, color: '#50a2e6' }
  ];

  return (
    <div className="statistics">
      <div className="stats-header">
        <h2>Resumen de Datos</h2>
        <button onClick={onRefresh} className="refresh-button">
          Actualizar
        </button>
      </div>

      {/* Tarjetas de totales */}
      <div className="stats-cards">
        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#e3f2fd' }}>
            📧
          </div>
          <div className="stat-content">
            <h3>Correos Electrónicos</h3>
            <p className="stat-number">{totals.emails.toLocaleString()}</p>
            <span className="stat-label">mensajes analizados</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#fff3e0' }}>
            📅
          </div>
          <div className="stat-content">
            <h3>Eventos de Calendario</h3>
            <p className="stat-number">{totals.calendar_events.toLocaleString()}</p>
            <span className="stat-label">reuniones registradas</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#e8f5e9' }}>
            💬
          </div>
          <div className="stat-content">
            <h3>Mensajes de Teams</h3>
            <p className="stat-number">{totals.teams_messages.toLocaleString()}</p>
            <span className="stat-label">chats analizados</span>
          </div>
        </div>
      </div>

      {/* Gráficas */}
      <div className="charts-container">
        {/* Gráfica de pastel - Distribución */}
        <div className="card chart-card">
          <h3>Distribución de Datos</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={totalData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {totalData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Gráfica de barras - Top enviadores de email */}
        {topSenders.length > 0 && (
          <div className="card chart-card">
            <h3>Top 10 - Enviadores de Correos</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={topSenders}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="email"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  tick={{ fontSize: 12 }}
                />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#0078d4" name="Correos enviados" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Gráfica de barras - Top organizadores */}
        {topOrganizers.length > 0 && (
          <div className="card chart-card">
            <h3>Top 10 - Organizadores de Reuniones</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={topOrganizers}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="email"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  tick={{ fontSize: 12 }}
                />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#106ebe" name="Reuniones organizadas" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}

export default Statistics;
