import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar'
import './Upload.css'

const Upload = () => {
  const [image1, setImage1] = useState(null)
  const [image2, setImage2] = useState(null)
  const [preview1, setPreview1] = useState(null)
  const [preview2, setPreview2] = useState(null)
  const [caption, setCaption] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleImage1Change = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImage1(file)
      const reader = new FileReader()
      reader.onloadend = () => setPreview1(reader.result)
      reader.readAsDataURL(file)
    }
  }

  const handleImage2Change = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImage2(file)
      const reader = new FileReader()
      reader.onloadend = () => setPreview2(reader.result)
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!image1 || !image2) {
      setError('Please select both images')
      return
    }

    setLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('image1', image1)
      formData.append('image2', image2)
      if (caption) {
        formData.append('caption', caption)
      }

      await axios.post('/api/posts', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload post')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Navbar />
      <div className="upload-page">
        <div className="container">
          <div className="upload-form-container">
            <h1>Upload Post</h1>
            {error && <div className="error-message">{error}</div>}
            <form onSubmit={handleSubmit} className="upload-form">
              <div className="image-uploads">
                <div className="image-upload">
                  <label>
                    {preview1 ? (
                      <img src={preview1} alt="Preview 1" className="preview-image" />
                    ) : (
                      <div className="upload-placeholder">Select Image 1</div>
                    )}
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImage1Change}
                      style={{ display: 'none' }}
                    />
                  </label>
                </div>
                <div className="image-upload">
                  <label>
                    {preview2 ? (
                      <img src={preview2} alt="Preview 2" className="preview-image" />
                    ) : (
                      <div className="upload-placeholder">Select Image 2</div>
                    )}
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImage2Change}
                      style={{ display: 'none' }}
                    />
                  </label>
                </div>
              </div>
              <textarea
                placeholder="Caption (optional)"
                value={caption}
                onChange={(e) => setCaption(e.target.value)}
                rows={4}
              />
              <button type="submit" disabled={loading || !image1 || !image2}>
                {loading ? 'Uploading...' : 'Upload'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </>
  )
}

export default Upload
