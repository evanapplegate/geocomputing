import { useState, useEffect } from 'react'
import axios from 'axios'
import PostCard from '../components/PostCard'
import Navbar from '../components/Navbar'
import './Home.css'

const Home = () => {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(0)
  const [hasMore, setHasMore] = useState(true)

  useEffect(() => {
    loadPosts()
  }, [])

  const loadPosts = async () => {
    try {
      const response = await axios.get(`/api/posts?skip=${page * 20}&limit=20`)
      if (response.data.length === 0) {
        setHasMore(false)
      } else {
        setPosts(prev => [...prev, ...response.data])
        setPage(prev => prev + 1)
      }
    } catch (error) {
      console.error('Error loading posts:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadMore = () => {
    if (!loading && hasMore) {
      loadPosts()
    }
  }

  if (loading && posts.length === 0) {
    return (
      <>
        <Navbar />
        <div className="home-loading">Loading...</div>
      </>
    )
  }

  return (
    <>
      <Navbar />
      <div className="home">
        <div className="container">
          <div className="posts-feed">
            {posts.map(post => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>
          {hasMore && (
            <button onClick={loadMore} className="load-more">
              Load More
            </button>
          )}
        </div>
      </div>
    </>
  )
}

export default Home
