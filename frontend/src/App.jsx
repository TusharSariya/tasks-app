import { Routes, Route, Link } from 'react-router-dom'
import { TasksPage } from './pages/TasksPage'

function App() {
  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <nav style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <Link to="/">Home</Link>
        <Link to="/tasks">Tasks</Link>
      </nav>

      <Routes>
        <Route path="/" element={<div>Home page</div>} />
        <Route path="/tasks" element={<TasksPage />} />
      </Routes>
    </div>
  )
}

export default App