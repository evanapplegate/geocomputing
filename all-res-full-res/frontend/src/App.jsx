import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Landing from './pages/Landing'
import App from './pages/App'
import Settings from './pages/Settings'
import ResetPassword from './pages/ResetPassword'
import PrivateRoute from './components/PrivateRoute'
import './App.css'

function AppRouter() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route
            path="/app"
            element={
              <PrivateRoute>
                <App />
              </PrivateRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <PrivateRoute>
                <Settings />
              </PrivateRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default AppRouter
