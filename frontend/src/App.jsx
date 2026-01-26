import { useTasks } from './hooks/useTasks'
import { Loading } from './components/common/Loading'
import { ErrorMessage } from './components/common/ErrorMessage'
import { TaskList } from './components/tasks/TaskList'

function App() {
  //retrieve tasks and organize by task headline
  const { tasks, loading, error } = useTasks()

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Task List</h1>
      
      {loading && <Loading />}
      {error && <ErrorMessage error={error} />}
      {!loading && !error && <TaskList tasks={tasks} />}
    </div>
  )
}

export default App