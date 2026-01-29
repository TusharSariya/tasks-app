import { Routes, Route, Link } from 'react-router-dom'
import { TasksPage } from './pages/TasksPage'
import { OrgChartPage } from './pages/OrgChartPage'
import { UserDetailsPage } from './pages/UserDetailsPage'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="nav-links">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/tasks" className="nav-link">Tasks</Link>
          <Link to="/org-chart" className="nav-link">Org Chart</Link>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<div>Home page</div>} />
        <Route path="/tasks" element={<TasksPage />} />
        <Route path="/org-chart" element={<OrgChartPage />} />
        <Route path="/user/:userId" element={<UserDetailsPage />} />
      </Routes>
    </div>
  )
}

export default App