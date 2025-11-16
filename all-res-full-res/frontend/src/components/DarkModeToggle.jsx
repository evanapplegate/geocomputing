import { useTheme } from '../contexts/ThemeContext'
import './DarkModeToggle.css'

const DarkModeToggle = () => {
  const { darkMode, toggleDarkMode } = useTheme()

  return (
    <button onClick={toggleDarkMode} className="dark-mode-toggle button-base">
      {darkMode ? '☀️' : '🌙'}
    </button>
  )
}

export default DarkModeToggle
