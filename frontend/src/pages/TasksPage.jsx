// src/pages/TasksPage.jsx
import { useTasks } from '../hooks/useTasks'
import { Loading } from '../components/common/Loading'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { TaskList } from '../components/tasks/TaskList'

export function TasksPage() {
  const { tasks, loading, error } = useTasks()

  if (loading) return <Loading />
  if (error) return <ErrorMessage error={error} />
  return <TaskList tasks={tasks} />
}