/**
 * API Service - Servicios para comunicarse con el backend
 */
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para agregar token a todas las peticiones
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
  }

  setToken(token) {
    if (token) {
      this.api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete this.api.defaults.headers.common['Authorization'];
    }
  }

  // Autenticación
  async login() {
    const response = await this.api.get('/auth/login');
    return response.data;
  }

  async logout() {
    const response = await this.api.post('/auth/logout');
    return response.data;
  }

  // Usuarios
  async getUsers() {
    const response = await this.api.get('/api/users/');
    return response.data;
  }

  async syncUsers() {
    const response = await this.api.get('/api/users/sync');
    return response.data;
  }

  // Extracción de datos
  async extractEmails(data) {
    const response = await this.api.post('/api/extract/emails', data);
    return response.data;
  }

  async extractCalendar(data) {
    const response = await this.api.post('/api/extract/calendar', data);
    return response.data;
  }

  async extractTeams(data) {
    const response = await this.api.post('/api/extract/teams', data);
    return response.data;
  }

  async getExtractionStatus(taskId) {
    const response = await this.api.get(`/api/extract/status/${taskId}`);
    return response.data;
  }

  // Consulta de datos
  async getEmails(params = {}) {
    const response = await this.api.get('/api/data/emails', { params });
    return response.data;
  }

  async getCalendarEvents(params = {}) {
    const response = await this.api.get('/api/data/calendar', { params });
    return response.data;
  }

  async getTeamsMessages(params = {}) {
    const response = await this.api.get('/api/data/teams', { params });
    return response.data;
  }

  async getStatistics() {
    const response = await this.api.get('/api/data/stats');
    return response.data;
  }

  async getCommunicationNetwork(daysBack = 30, minInteractions = 1) {
    const response = await this.api.get('/api/data/communication-network', {
      params: { days_back: daysBack, min_interactions: minInteractions }
    });
    return response.data;
  }
}

export const apiService = new ApiService();
