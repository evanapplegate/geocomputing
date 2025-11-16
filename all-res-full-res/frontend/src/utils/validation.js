// DRY validation utilities

export const validateFileSize = (file, minSizeMB = 10, maxSizeMB = 500) => {
  const fileSizeMB = file.size / (1024 * 1024)
  
  if (file.size < minSizeMB * 1024 * 1024) {
    return {
      valid: false,
      error: `File must be at least ${minSizeMB}MB. Current size: ${fileSizeMB.toFixed(2)}MB`
    }
  }
  
  if (file.size > maxSizeMB * 1024 * 1024) {
    return {
      valid: false,
      error: `File size must be less than ${maxSizeMB}MB`
    }
  }
  
  return { valid: true }
}

export const validateFileType = (file) => {
  const allowedTypes = [
    'image/jpeg', 'image/jpg', 'image/png', 'image/webp',
    'image/tiff', 'image/tif'
  ]
  
  const allowedExtensions = [
    '.cr2', '.nef', '.arw', '.raf', '.orf', '.rw2', '.pef', '.srw', '.dng'
  ]
  
  const ext = '.' + file.name.split('.').pop().toLowerCase()
  
  if (allowedTypes.includes(file.type) || allowedExtensions.includes(ext)) {
    return { valid: true }
  }
  
  return {
    valid: false,
    error: 'Unsupported format. Allowed: PNG, JPG, TIFF, RAW (CR2, NEF, ARW, etc.)'
  }
}

export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

export const validateDisplayName = (name) => {
  if (!name || name.trim().length === 0) {
    return { valid: false, error: 'Display name is required' }
  }
  if (name.length > 50) {
    return { valid: false, error: 'Display name must be less than 50 characters' }
  }
  return { valid: true }
}
