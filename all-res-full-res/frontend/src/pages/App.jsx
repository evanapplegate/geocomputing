import { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import TabNav from '../components/TabNav'
import MyPosts from '../components/MyPosts'
import MyFeed from '../components/MyFeed'
import UploadZone from '../components/UploadZone'
import './App.css'

const App = () => {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('feed')
  const [refreshKey, setRefreshKey] = useState(0)

  const handlePostCreated = () => {
    setRefreshKey(prev => prev + 1)
    setActiveTab('posts')
  }

  return (
    <div className="app-page">
      <TabNav activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="app-content">
        {activeTab === 'feed' && <MyFeed key={`feed-${refreshKey}`} />}
        {activeTab === 'posts' && <MyPosts key={`posts-${refreshKey}`} onPostCreated={handlePostCreated} />}
      </div>
      {activeTab === 'posts' && (
        <div className="upload-zone-wrapper-fixed">
          <UploadZone onUploadComplete={handlePostCreated} />
        </div>
      )}
    </div>
  )
}

export default App
