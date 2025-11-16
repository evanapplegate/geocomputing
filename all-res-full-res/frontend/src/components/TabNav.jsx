import './TabNav.css'

const TabNav = ({ activeTab, setActiveTab }) => {
  return (
    <nav className="tab-nav">
      <div className="container">
        <div className="tab-nav-content">
          <button
            className={`tab-button ${activeTab === 'feed' ? 'active' : ''}`}
            onClick={() => setActiveTab('feed')}
          >
            My Feed
          </button>
          <button
            className={`tab-button ${activeTab === 'posts' ? 'active' : ''}`}
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
