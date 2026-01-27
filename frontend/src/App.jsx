import { Routes, Route, Link } from 'react-router-dom'
import { useTasks } from './hooks/useTasks'
import { Loading } from './components/common/Loading'
import { ErrorMessage } from './components/common/ErrorMessage'
import { TaskList } from './components/tasks/TaskList'

function App() {
  const { tasks, loading, error } = useTasks()

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <nav style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <Link to="/">Home</Link>
        <Link to="/tasks">Tasks</Link>
      </nav>

      <Routes>
        <Route
          path="/"
          element={<div>Home page (put whatever you want here)</div>}
        />
        <Route
          path="/tasks"
          element={
            loading ? (
              <Loading />
            ) : error ? (
              <ErrorMessage error={error} />
            ) : (
              <TaskList tasks={tasks} />
            )
          }
        />
      </Routes>
    </div>
  )
}

export default App