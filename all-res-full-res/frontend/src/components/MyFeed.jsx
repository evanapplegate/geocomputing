import { useState, useEffect } from 'react'
import axios from 'axios'
import PostCard from './PostCard'
import './MyFeed.css'

const MyFeed = () => {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(0)
  const [hasMore, setHasMore] = useState(true)

  useEffect(() => {
    loadFeed()
  }, [])

  const loadFeed = async () => {
    try {
      const response = await axios.get(`/api/posts/feed?skip=${page * 20}&limit=20`)
      if (response.data.length === 0) {
        setHasMore(false)
      } else {
        setPosts(prev => [...prev, ...response.data])
        setPage(prev => prev + 1)
      }
    } catch (error) {
      console.error('Error loading feed:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadMore = () => {
    if (!loading && hasMore) {
      loadFeed()
    }
  }

  if (loading && posts.length === 0) {
    return (
      <div className="my-feed-container">
        <div className="container">
          <div className="loading-state">Loading...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="my-feed-container">
      <div className="container">
        {posts.length === 0 ? (
          <div className="empty-state">No posts yet.</div>
        ) : (
          <>
            <div className="feed-posts">
              {posts.map(post => (
                <PostCard key={post.id} post={post} />
              ))}
            </div>
            {hasMore && (
              <button onClick={loadMore} className="load-more">
                Load More
              </button>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default MyFeed
