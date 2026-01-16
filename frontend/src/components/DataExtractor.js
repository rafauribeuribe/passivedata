import React, { useState } from 'react';
import './DataExtractor.css';
import { apiService } from '../services/api';

function DataExtractor({ onExtractionComplete }) {
  const [extracting, setExtracting] = useState({
    emails: false,
    calendar: false,
    teams: false
  });
  const [results, setResults] = useState({
    emails: null,
    calendar: null,
    teams: null
  });

  const handleExtractEmails = async () => {
    try {
      setExtracting(prev => ({ ...prev, emails: true }));
      const result = await apiService.extractEmails({
        max_emails_per_user: 1000,
        days_back: 90
      });
      setResults(prev => ({ ...prev, emails: result }));
      onExtractionComplete && onExtractionComplete();
    } catch (error) {
      console.error('Error al extraer emails:', error);
      alert('Error al extraer emails: ' + (error.response?.data?.detail || error.message));
    } finally {
      setExtracting(prev => ({ ...prev, emails: false }));
    }
  };

  const handleExtractCalendar = async () => {
    try {
      setExtracting(prev => ({ ...prev, calendar: true }));
      const result = await apiService.extractCalendar({
        max_events_per_user: 1000,
        days_back: 90
      });
      setResults(prev => ({ ...prev, calendar: result }));
      onExtractionComplete && onExtractionComplete();
    } catch (error) {
      console.error('Error al extraer calendario:', error);
      alert('Error al extraer calendario: ' + (error.response?.data?.detail || error.message));
    } finally {
      setExtracting(prev => ({ ...prev, calendar: false }));
    }
  };

  const handleExtractTeams = async () => {
    try {
      setExtracting(prev => ({ ...prev, teams: true }));
      const result = await apiService.extractTeams({
        max_messages_per_chat: 100,
        max_chats: 50
      });
      setResults(prev => ({ ...prev, teams: result }));
      onExtractionComplete && onExtractionComplete();
    } catch (error) {
      console.error('Error al extraer Teams:', error);
      alert('Error al extraer Teams: ' + (error.response?.data?.detail || error.message));
    } finally {
      setExtracting(prev => ({ ...prev, teams: false }));
    }
  };

  return (
    <div className="data-extractor">
      <div className="extractor-header">
        <h2>Extracción de Datos</h2>
        <p className="subtitle-text">
          Extrae metadata de correos, calendarios y chats de Microsoft 365.
          Los datos se procesarán de forma segura sin almacenar contenido sensible.
        </p>
      </div>

      <div className="extraction-cards">
        {/* Correos Electrónicos */}
        <div className="card extraction-card">
          <div className="extraction-header">
            <span className="extraction-icon">📧</span>
            <h3>Correos Electrónicos</h3>
          </div>
          <p className="extraction-description">
            Extrae metadata de correos: remitente, destinatario y timestamp.
            Se procesarán los últimos 90 días.
          </p>
          <div className="extraction-details">
            <span>Máximo: 1,000 correos por usuario</span>
            <span>Período: Últimos 90 días</span>
          </div>
          <button
            onClick={handleExtractEmails}
            disabled={extracting.emails}
            className="extract-button"
          >
            {extracting.emails ? 'Extrayendo...' : 'Extraer Emails'}
          </button>
          {results.emails && (
            <div className="success">
              {results.emails.message}
            </div>
          )}
        </div>

        {/* Calendario */}
        <div className="card extraction-card">
          <div className="extraction-header">
            <span className="extraction-icon">📅</span>
            <h3>Eventos de Calendario</h3>
          </div>
          <p className="extraction-description">
            Extrae metadata de reuniones: organizador, participantes y horarios.
            Se procesarán los últimos 90 días.
          </p>
          <div className="extraction-details">
            <span>Máximo: 1,000 eventos por usuario</span>
            <span>Período: Últimos 90 días</span>
          </div>
          <button
            onClick={handleExtractCalendar}
            disabled={extracting.calendar}
            className="extract-button"
          >
            {extracting.calendar ? 'Extrayendo...' : 'Extraer Calendario'}
          </button>
          {results.calendar && (
            <div className="success">
              {results.calendar.message}
            </div>
          )}
        </div>

        {/* Microsoft Teams */}
        <div className="card extraction-card">
          <div className="extraction-header">
            <span className="extraction-icon">💬</span>
            <h3>Chats de Microsoft Teams</h3>
          </div>
          <p className="extraction-description">
            Extrae metadata de chats: participantes y timestamps.
            Se procesarán hasta 50 chats por usuario.
          </p>
          <div className="extraction-details">
            <span>Máximo: 100 mensajes por chat</span>
            <span>Máximo: 50 chats por usuario</span>
          </div>
          <button
            onClick={handleExtractTeams}
            disabled={extracting.teams}
            className="extract-button"
          >
            {extracting.teams ? 'Extrayendo...' : 'Extraer Teams'}
          </button>
          {results.teams && (
            <div className="success">
              {results.teams.message}
            </div>
          )}
        </div>
      </div>

      <div className="card info-card">
        <h3>Información Importante</h3>
        <ul>
          <li>
            <strong>Privacidad:</strong> Solo se extrae metadata (remitente, destinatario, timestamps).
            El contenido de los mensajes NO se almacena.
          </li>
          <li>
            <strong>Permisos:</strong> Requiere permisos de lectura en Microsoft Graph API.
          </li>
          <li>
            <strong>Tiempo de procesamiento:</strong> La extracción puede tomar varios minutos
            dependiendo del volumen de datos.
          </li>
          <li>
            <strong>Actualización:</strong> Puedes ejecutar la extracción múltiples veces
            para actualizar los datos.
          </li>
        </ul>
      </div>
    </div>
  );
}

export default DataExtractor;
