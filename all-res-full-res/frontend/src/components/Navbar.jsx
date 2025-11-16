import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './Navbar.css'

const Navbar = () => {
  const { user, logout } = useAuth()

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="navbar-logo">
            All Res Full Res
          </Link>
          <div className="navbar-links">
            {user ? (
              <>
                <Link to="/upload">Upload</Link>
                <Link to="/settings">Settings</Link>
                <Link to={`/user/${user.email}`}>Profile</Link>
                <button onClick={logout}>Logout</button>
              </>
            ) : (
              <Link to="/login">Login</Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
