import React, { useState } from 'react';
import './Login.css';
import { apiService } from '../services/api';

function Login({ onLogin }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleMicrosoftLogin = async () => {
    try {
      setLoading(true);
      setError(null);

      // Obtener URL de autorización
      const data = await apiService.login();

      if (data.auth_url) {
        // Redirigir a Microsoft para autenticación
        window.location.href = data.auth_url;
      } else {
        setError('No se pudo obtener URL de autenticación');
      }
    } catch (err) {
      setError('Error al iniciar sesión: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  // Simular login para desarrollo (remover en producción)
  const handleDemoLogin = () => {
    const demoUser = {
      id: 'demo-user-1',
      email: 'admin@demo.com',
      display_name: 'Administrador Demo',
      is_admin: true
    };
    const demoToken = 'demo-token-12345';
    onLogin(demoToken, demoUser);
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>PassiveData</h1>
          <p>Análisis de Datos Pasivos de Microsoft 365</p>
        </div>

        <div className="login-body">
          <p className="login-description">
            Inicia sesión con tu cuenta de administrador de Microsoft 365
            para analizar los datos de comunicación de tu organización.
          </p>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          <button
            onClick={handleMicrosoftLogin}
            disabled={loading}
            className="login-button"
          >
            {loading ? 'Cargando...' : 'Iniciar sesión con Microsoft'}
          </button>

          <div className="divider">
            <span>o</span>
          </div>

          <button
            onClick={handleDemoLogin}
            className="login-button demo-button"
          >
            Modo Demo (Desarrollo)
          </button>

          <div className="login-info">
            <h3>Requisitos:</h3>
            <ul>
              <li>Cuenta de administrador de Microsoft 365</li>
              <li>Permisos de lectura para Mail, Calendar y Teams</li>
              <li>App Registration configurada en Azure AD</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
