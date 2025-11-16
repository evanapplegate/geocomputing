import './TabNav.css'
import '../styles/buttons.css'

const TabNav = ({ activeTab, setActiveTab }) => {
  return (
    <nav className="tab-nav">
      <div className="container">
        <div className="tab-nav-content">
          <button
            className={`tab-button button-base ${activeTab === 'feed' ? 'button-active' : ''}`}
            onClick={() => setActiveTab('feed')}
          >
            My Feed
          </button>
          <button
            className={`tab-button button-base ${activeTab === 'posts' ? 'button-active' : ''}`}
            onClick={() => setActiveTab('posts')}
          >
            My Posts
          </button>
        </div>
      </div>
    </nav>
  )
}

export default TabNav
