import axios from 'axios'

export const api = axios.create({
  // Use the same origin in production; Nginx proxies /api to Practice Service.
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 60_000,
})
