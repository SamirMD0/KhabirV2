import { client } from './client'

export const authApi = {
  signup: (username, email, password) =>
    client.post('/api/auth/signup', { username, email, password }).then(r => r.data),

  login: (username, password) =>
    client.post('/api/auth/login', { username, password }).then(r => r.data),

  logout: () =>
    client.post('/api/auth/logout').then(r => r.data),

  me: (token) =>
    client.get('/api/auth/me', {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }).then(r => r.data),

  refresh: () =>
    client.post('/api/auth/refresh').then(r => r.data),
}
