import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const PrivateRoute = ({ children }) => {
  const { user, loading } = useAuth()

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center' }}>Loading...</div>
  }

  return user ? children : <Navigate to="/login" />
}

export default PrivateRoute
