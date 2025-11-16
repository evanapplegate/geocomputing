// DRY error handling utilities

export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error
    return error.response.data?.detail || error.response.data?.message || 'An error occurred'
  } else if (error.request) {
    // Request made but no response
    return 'Network error. Please check your connection.'
  } else {
    // Something else happened
    return error.message || 'An unexpected error occurred'
  }
}

export const logError = (error, context = '') => {
  const message = context ? `${context}: ${error.message}` : error.message
  console.error(message, error)
  
  // In production, could send to error tracking service
  if (process.env.NODE_ENV === 'production') {
    // Example: send to Sentry, LogRocket, etc.
  }
}
