import { useState, useEffect } from 'react'
import axios from 'axios'
import Navbar from '../components/Navbar'
import { useAuth } from '../contexts/AuthContext'
import './Settings.css'

const Settings = () => {
  const { user, checkAuth } = useAuth()
  const [displayName, setDisplayName] = useState('')
  const [email, setEmail] = useState('')
  const [links, setLinks] = useState([
    { link_type: 'twitter', url: '' },
    { link_type: 'instagram', url: '' },
    { link_type: 'website', url: '' }
  ])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (user) {
      setDisplayName(user.display_name || '')
      setEmail(user.email || '')
      if (user.links) {
        const linkMap = {}
        user.links.forEach(link => {
          linkMap[link.link_type] = link.url
        })
        setLinks([
          { link_type: 'twitter', url: linkMap.twitter || '' },
          { link_type: 'instagram', url: linkMap.instagram || '' },
          { link_type: 'website', url: linkMap.website || '' }
        ])
      }
    }
  }, [user])

  const handleAvatarUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      await axios.post('/api/users/me/avatar', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      checkAuth()
      setMessage('Avatar updated')
    } catch (error) {
      setMessage('Failed to upload avatar')
    }
  }

  const handleSave = async () => {
    setLoading(true)
    setMessage('')

    try {
      await axios.put('/api/users/me', { display_name: displayName })
      await axios.put('/api/users/me/links', { links })
      checkAuth()
      setMessage('Settings saved')
    } catch (error) {
      setMessage('Failed to save settings')
    } finally {
      setLoading(false)
    }
  }

  const handleChangeEmail = async () => {
    if (!email) return
    try {
      await axios.put('/api/users/me/email', { new_email: email })
      setMessage('Verification email sent')
    } catch (error) {
      setMessage('Failed to send verification email')
    }
  }

  const updateLink = (index, url) => {
    const newLinks = [...links]
    newLinks[index].url = url
    setLinks(newLinks)
  }

  return (
    <>
      <Navbar />
      <div className="settings-page">
        <div className="container">
          <div className="settings-container">
            <h1>Settings</h1>
            {message && <div className="settings-message">{message}</div>}
            
            <div className="settings-section">
              <h2>Avatar</h2>
              {user?.avatar_url && (
                <img src={user.avatar_url} alt="Avatar" className="settings-avatar" />
              )}
              <input
                type="file"
                accept="image/*"
                onChange={handleAvatarUpload}
                className="file-input"
              />
            </div>

            <div className="settings-section">
              <h2>Display Name</h2>
              <input
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="Display name"
              />
            </div>

            <div className="settings-section">
              <h2>Email</h2>
              <div className="email-change">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="New email"
                />
                <button onClick={handleChangeEmail}>Change Email</button>
              </div>
            </div>

            <div className="settings-section">
              <h2>Profile Links</h2>
              <div className="links-inputs">
                <div className="link-input">
                  <label>Twitter</label>
                  <input
                    type="url"
                    value={links[0].url}
                    onChange={(e) => updateLink(0, e.target.value)}
                    placeholder="https://twitter.com/username"
                  />
                </div>
                <div className="link-input">
                  <label>Instagram</label>
                  <input
                    type="url"
                    value={links[1].url}
                    onChange={(e) => updateLink(1, e.target.value)}
                    placeholder="https://instagram.com/username"
                  />
                </div>
                <div className="link-input">
                  <label>Website</label>
                  <input
                    type="url"
                    value={links[2].url}
                    onChange={(e) => updateLink(2, e.target.value)}
                    placeholder="https://example.com"
                  />
                </div>
              </div>
            </div>

            <button onClick={handleSave} disabled={loading} className="save-btn">
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

export default Settings
