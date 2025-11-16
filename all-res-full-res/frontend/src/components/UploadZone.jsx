import { useState, useRef } from 'react'
import axios from 'axios'
import './UploadZone.css'
import '../styles/buttons.css'
import { validateFileSize, validateFileType } from '../utils/validation'
import { handleApiError } from '../utils/errorHandler'

const UploadZone = ({ onUploadComplete }) => {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const fileInputRef = useRef(null)

  const handleFileSelect = (file) => {
    // Validate file type
    const typeValidation = validateFileType(file)
    if (!typeValidation.valid) {
      setError(typeValidation.error)
      setSelectedFile(null)
      return
    }
    
    // Validate file size
    const sizeValidation = validateFileSize(file)
    if (!sizeValidation.valid) {
      setError(sizeValidation.error)
      setSelectedFile(null)
      return
    }

    setError('')
    setSelectedFile(file)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files[0]
    if (file) {
      handleFileSelect(file)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleFileInput = (e) => {
    const file = e.target.files[0]
    if (file) {
      handleFileSelect(file)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setUploading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('image1', selectedFile)
      formData.append('image2', selectedFile) // Duplicate for two-column layout requirement
      formData.append('caption', '')

      await axios.post('/api/posts', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          // Could show progress here
        }
      })

      setSelectedFile(null)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      onUploadComplete()
    } catch (err) {
      setError(handleApiError(err))
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="upload-zone-wrapper">
      <div
        className={`upload-zone ${isDragging ? 'dragging' : ''} ${selectedFile ? 'has-file' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".png,.jpg,.jpeg,.tiff,.tif,.cr2,.nef,.arw,.raf,.orf,.rw2,.pef,.srw,.dng"
          onChange={handleFileInput}
          style={{ display: 'none' }}
        />
        {selectedFile ? (
          <div className="file-info">
            <div className="file-name">{selectedFile.name}</div>
            <div className="file-size">{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</div>
            <button
              onClick={(e) => {
                e.stopPropagation()
                setSelectedFile(null)
                setError('')
                if (fileInputRef.current) {
                  fileInputRef.current.value = ''
                }
              }}
              className="remove-file"
            >
              Remove
            </button>
          </div>
        ) : (
          <div className="upload-zone-content">
            <div className="upload-text">
              drop at least 1x 10mb image here
            </div>
            <div className="upload-formats">
              [PNG/JPG/TIFF/RAW]
            </div>
          </div>
        )}
      </div>
      {error && <div className="upload-error">{error}</div>}
      {selectedFile && (
        <button
          onClick={handleUpload}
          disabled={uploading}
          className="upload-button button-base button-primary"
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      )}
    </div>
  )
}

export default UploadZone
