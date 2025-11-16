import { useState, useEffect } from 'react'
import axios from 'axios'
import { useAuth } from '../contexts/AuthContext'
import PostCard from './PostCard'
import './MyPosts.css'

const MyPosts = ({ onPostCreated }) => {
  const { user } = useAuth()
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadMyPosts()
  }, [])

  useEffect(() => {
    if (onPostCreated) {
      loadMyPosts()
    }
  }, [onPostCreated])

  const loadMyPosts = async () => {
    try {
      const response = await axios.get('/api/posts/my')
      setPosts(response.data)
    } catch (error) {
      console.error('Error loading posts:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="my-posts-container">
        <div className="container">
          <div className="loading-state">Loading...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="my-posts-container">
      <div className="container">
        {posts.length === 0 ? (
          <div className="empty-state">
            <p>No posts yet. Upload your first image above.</p>
          </div>
        ) : (
          <div className="posts-list">
            {posts.map(post => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default MyPosts
