import axios from 'axios';

const BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({ baseURL: BASE });

export const getStatus    = ()             => api.get('/api/status').then(r => r.data);
export const getLoginUrl  = ()             => api.get('/auth/login').then(r => r.data.url);
export const logout       = ()             => api.post('/auth/logout');
export const getOrgUsers  = ()             => api.get('/api/users').then(r => r.data);
export const startExtract = (type, p)      => api.post(`/api/extract/${type}`, null, { params: p }).then(r => r.data);
export const getJobStatus = (id)           => api.get(`/api/extract/status/${id}`).then(r => r.data);
export const getJobs      = ()             => api.get('/api/jobs').then(r => r.data);
export const getNetwork   = (params)       => api.get('/api/network', { params }).then(r => r.data);
export const getStats     = (days)         => api.get('/api/stats', { params: { days } }).then(r => r.data);
export const getPairs     = (days, top)    => api.get('/api/pairs', { params: { days, top } }).then(r => r.data);
