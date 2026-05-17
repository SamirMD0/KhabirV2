import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <nav className="border-b border-neutral-800 bg-neutral-950/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link to="/" className="font-semibold text-lg tracking-tight">
          KHABIR
        </Link>
        <div className="flex items-center gap-4 text-sm">
          {user ? (
            <>
              <span className="text-neutral-400">{user.username}</span>
              {user.is_admin && (
                <Link to="/dashboard" className="text-neutral-300 hover:text-white transition-colors">
                  Dashboard
                </Link>
              )}
              <button
                onClick={handleLogout}
                className="text-neutral-400 hover:text-white transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-neutral-300 hover:text-white transition-colors">Login</Link>
              <Link to="/signup" className="bg-red-600 hover:bg-red-700 text-white px-3 py-1.5 rounded-md transition-colors">
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
