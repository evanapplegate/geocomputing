import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Home from './pages/Home'
import Login from './pages/Login'
import Upload from './pages/Upload'
import Profile from './pages/Profile'
import Settings from './pages/Settings'
import ResetPassword from './pages/ResetPassword'
import PrivateRoute from './components/PrivateRoute'
import './App.css'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route
            path="/upload"
            element={
              <PrivateRoute>
                <Upload />
              </PrivateRoute>
            }
          />
          <Route path="/user/:username" element={<Profile />} />
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

export default App
