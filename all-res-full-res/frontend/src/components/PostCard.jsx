import './PostCard.css'

const PostCard = ({ post }) => {
  const downloadUrl = `/api/posts/${post.id}/download`
  
  return (
    <article className="post-card">
      <div className="post-images">
        <div className="post-image-wrapper">
          <img 
            src={post.image_url_display_1} 
            alt={post.caption || 'Post image 1'}
            loading="lazy"
          />
        </div>
        <div className="post-image-wrapper">
          <img 
            src={post.image_url_display_2} 
            alt={post.caption || 'Post image 2'}
            loading="lazy"
          />
        </div>
      </div>
      {post.caption && (
        <div className="post-caption">
          {post.caption}{' '}
          <a href={post.image_url_full_1} target="_blank" rel="noopener noreferrer" className="download-link">
            download full res
          </a>
        </div>
      )}
      {!post.caption && (
        <div className="post-caption">
          <a href={post.image_url_full_1} target="_blank" rel="noopener noreferrer" className="download-link">
            download full res
          </a>
        </div>
      )}
      <div className="post-author">
        <a href={`/user/${post.author.email}`}>
          {post.author.display_name}
        </a>
      </div>
    </article>
  )
}

export default PostCard
