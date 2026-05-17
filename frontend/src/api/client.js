import axios from 'axios'

// In dev: vite proxy forwards /api to http://localhost:5000
// In prod: VITE_API_URL is set to the Railway backend URL
const BASE_URL = import.meta.env.VITE_API_URL ?? ''

export const client = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
})

let _getToken = () => null
let _refresh = async () => null

export function setTokenGetter(fn) { _getToken = fn }
export function setRefreshFn(fn) { _refresh = fn }

client.interceptors.request.use(config => {
  const token = _getToken()
  if (token) config.headers['Authorization'] = `Bearer ${token}`
  return config
})

let isRefreshing = false
let queue = []

client.interceptors.response.use(
  res => res,
  async err => {
    const original = err.config
    if (err.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        return new Promise((res, rej) => queue.push({ res, rej }))
          .then(token => { original.headers['Authorization'] = `Bearer ${token}`; return client(original) })
      }
      original._retry = true
      isRefreshing = true
      try {
        const newToken = await _refresh()
        queue.forEach(p => p.res(newToken))
        queue = []
        original.headers['Authorization'] = `Bearer ${newToken}`
        return client(original)
      } catch (e) {
        queue.forEach(p => p.rej(e))
        queue = []
        return Promise.reject(e)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(err)
  }
)
