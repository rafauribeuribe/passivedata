import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import { apiService } from '../services/api';
import Statistics from './Statistics';
import DataExtractor from './DataExtractor';
import CommunicationNetwork from './CommunicationNetwork';

function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    try {
      setLoading(true);
      const data = await apiService.getStatistics();
      setStats(data);
    } catch (error) {
      console.error('Error al cargar estadísticas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    if (window.confirm('¿Estás seguro de cerrar sesión?')) {
      onLogout();
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <h1>PassiveData Analytics</h1>
            <p className="subtitle">Microsoft 365 Communication Insights</p>
          </div>
          <div className="header-right">
            <div className="user-info">
              <span className="user-name">{user.display_name}</span>
              <span className="user-email">{user.email}</span>
            </div>
            <button onClick={handleLogout} className="logout-button">
              Cerrar Sesión
            </button>
          </div>
        </div>

        <nav className="dashboard-nav">
          <button
            className={activeTab === 'overview' ? 'active' : ''}
            onClick={() => setActiveTab('overview')}
          >
            Resumen
          </button>
          <button
            className={activeTab === 'extract' ? 'active' : ''}
            onClick={() => setActiveTab('extract')}
          >
            Extracción de Datos
          </button>
          <button
            className={activeTab === 'network' ? 'active' : ''}
            onClick={() => setActiveTab('network')}
          >
            Red de Comunicación
          </button>
        </nav>
      </header>

      <main className="dashboard-main">
        <div className="container">
          {activeTab === 'overview' && (
            <Statistics stats={stats} loading={loading} onRefresh={loadStatistics} />
          )}

          {activeTab === 'extract' && (
            <DataExtractor onExtractionComplete={loadStatistics} />
          )}

          {activeTab === 'network' && (
            <CommunicationNetwork />
          )}
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
