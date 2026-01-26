import { useState, useEffect } from 'react'
import { fetchTasks } from '../services/taskService'
import { groupTasksByHeadline } from '../utils/taskUtils'

export const useTasks = () => {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadTasks = async () => {
      try {
        setLoading(true)
        const data = await fetchTasks()
        const grouped = groupTasksByHeadline(data)
        setTasks(grouped)
        setError(null)
      } catch (err) {
        console.error('Error fetching tasks:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    loadTasks()
  }, [])

  return { tasks, loading, error }
}