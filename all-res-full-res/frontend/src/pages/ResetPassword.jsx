import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar'
import './ResetPassword.css'

const ResetPassword = () => {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleRequestReset = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      await axios.post('/api/auth/reset-password', { email })
      setMessage('If email exists, reset link has been sent')
    } catch (error) {
      setMessage('Failed to send reset email')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async (e) => {
    e.preventDefault()
    if (password !== confirmPassword) {
      setMessage('Passwords do not match')
      return
    }

    setLoading(true)
    setMessage('')

    try {
      await axios.post('/api/auth/reset-password/complete', {
        token,
        new_password: password
      })
      setMessage('Password reset successfully. You can now login.')
    } catch (error) {
      setMessage('Invalid or expired token')
    } finally {
      setLoading(false)
    }
  }

  if (token) {
    return (
      <>
        <Navbar />
        <div className="reset-password-page">
          <div className="container">
            <div className="reset-form-container">
              <h1>Reset Password</h1>
              {message && <div className="reset-message">{message}</div>}
              <form onSubmit={handleReset} className="reset-form">
                <input
                  type="password"
                  placeholder="New Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Confirm Password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
                <button type="submit" disabled={loading}>
                  {loading ? 'Resetting...' : 'Reset Password'}
                </button>
              </form>
            </div>
          </div>
        </div>
      </>
    )
  }

  return (
    <>
      <Navbar />
      <div className="reset-password-page">
        <div className="container">
          <div className="reset-form-container">
            <h1>Reset Password</h1>
            {message && <div className="reset-message">{message}</div>}
            <form onSubmit={handleRequestReset} className="reset-form">
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Sending...' : 'Send Reset Link'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </>
  )
}

export default ResetPassword
