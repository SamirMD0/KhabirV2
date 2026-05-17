import { createContext, useState, useCallback, useEffect } from 'react'
import { authApi } from '../api/auth'
import { setTokenGetter, setRefreshFn } from '../api/client'

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(null)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    authApi.refresh()
      .then(({ access_token }) => {
        setAccessToken(access_token)
        return authApi.me(access_token)
      })
      .then(setUser)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const login = useCallback(async (username, password) => {
    const data = await authApi.login(username, password)
    setAccessToken(data.access_token)
    setUser({ user_id: data.user_id, username: data.username, is_admin: data.is_admin })
    return data
  }, [])

  const logout = useCallback(async () => {
    await authApi.logout()
    setAccessToken(null)
    setUser(null)
  }, [])

  const refreshToken = useCallback(async () => {
    const { access_token } = await authApi.refresh()
    setAccessToken(access_token)
    return access_token
  }, [])

  useEffect(() => {
    setTokenGetter(() => accessToken)
    setRefreshFn(refreshToken)
  }, [accessToken, refreshToken])

  return (
    <AuthContext.Provider value={{ accessToken, user, loading, login, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  )
}
