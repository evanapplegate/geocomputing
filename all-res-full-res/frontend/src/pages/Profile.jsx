import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import PostCard from '../components/PostCard'
import Navbar from '../components/Navbar'
import { useAuth } from '../contexts/AuthContext'
import './Profile.css'

const Profile = () => {
  const { username } = useParams()
  const { user: currentUser } = useAuth()
  const [user, setUser] = useState(null)
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProfile()
  }, [username])

  const loadProfile = async () => {
    try {
      const [userResponse, postsResponse] = await Promise.all([
        axios.get(`/api/users/${username}`),
        axios.get(`/api/users/${username}/posts`)
      ])
      setUser(userResponse.data)
      setPosts(postsResponse.data)
    } catch (error) {
      console.error('Error loading profile:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="profile-loading">Loading...</div>
      </>
    )
  }

  if (!user) {
    return (
      <>
        <Navbar />
        <div className="profile-error">User not found</div>
      </>
    )
  }

  const isOwnProfile = currentUser && currentUser.id === user.id

  return (
    <>
      <Navbar />
      <div className="profile-page">
        <div className="container">
          <div className="profile-header">
            {user.avatar_url && (
              <img src={user.avatar_url} alt={user.display_name} className="profile-avatar" />
            )}
            <div className="profile-info">
              <h1>{user.display_name}</h1>
              {user.links && user.links.length > 0 && (
                <div className="profile-links">
                  {user.links.map(link => (
                    <a
                      key={link.id}
                      href={link.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="profile-link"
                    >
                      {link.link_type}
                    </a>
                  ))}
                </div>
              )}
            </div>
            {isOwnProfile && (
              <a href="/settings" className="edit-profile-btn">
                Edit Profile
              </a>
            )}
          </div>
          <div className="profile-posts">
            {posts.map(post => (
              <PostCard key={post.id} post={post} />
            ))}
            {posts.length === 0 && (
              <div className="no-posts">No posts yet</div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

export default Profile
