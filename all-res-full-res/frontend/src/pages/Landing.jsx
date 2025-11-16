import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import axios from 'axios'
import ASCIIArt from '../components/ASCIIArt'
import './Landing.css'

const Landing = () => {
  const { user, loading, checkAuth } = useAuth()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  useEffect(() => {
    const token = searchParams.get('token')
    if (token) {
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      checkAuth().then(() => {
        navigate('/app')
      })
    }
  }, [searchParams, navigate, checkAuth])

  useEffect(() => {
    if (!loading && user) {
      navigate('/app')
    }
  }, [user, loading, navigate])

  const handleGoogleLogin = async () => {
    try {
      const response = await axios.get('/api/auth/google')
      window.location.href = response.data.auth_url
    } catch (error) {
      console.error('Google login error:', error)
    }
  }

  const handleGitHubLogin = async () => {
    try {
      const response = await axios.get('/api/auth/github')
      window.location.href = response.data.auth_url
    } catch (error) {
      console.error('GitHub login error:', error)
    }
  }

  if (loading) {
    return <div className="landing-loading">Loading...</div>
  }

  return (
    <div className="landing-page">
      <div className="landing-container">
        <ASCIIArt />
        <div className="landing-auth">
          <h2>Sign in to continue</h2>
          <button onClick={handleGoogleLogin} className="sso-button google-button">
            Sign in with Google
          </button>
          <button onClick={handleGitHubLogin} className="sso-button github-button">
            Sign in with GitHub
          </button>
        </div>
      </div>
    </div>
  )
}

export default Landing
