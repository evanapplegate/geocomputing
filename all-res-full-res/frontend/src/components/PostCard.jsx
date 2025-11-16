import './PostCard.css'

const PostCard = ({ post }) => {
  return (
    <article className="post-card">
      <div className="post-images">
        <div className="post-image-wrapper">
          <a href={post.image_url_full_1} target="_blank" rel="noopener noreferrer">
            <img 
              src={post.image_url_display_1} 
              alt={post.caption || 'Post image 1'}
              loading="lazy"
            />
          </a>
        </div>
        <div className="post-image-wrapper">
          <a href={post.image_url_full_2} target="_blank" rel="noopener noreferrer">
            <img 
              src={post.image_url_display_2} 
              alt={post.caption || 'Post image 2'}
              loading="lazy"
            />
          </a>
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
        {post.author.display_name}
      </div>
    </article>
  )
}

export default PostCard
