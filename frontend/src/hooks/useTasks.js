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
        console.log("fetched data")
        console.log("--------------------------------------------------")
        console.log(data)
        // tasks to author is a many to many relationship
        // a task can have many owners/authors
        // what is returned by the API is by author, we want to render by task/headline
        // thus data must be transformed so that one task have multiple authors
        // storing data this way has issues with scalability as paginating the API will result in inconsistent owners for tasks
        const grouped = groupTasksByHeadline(data)
        console.log("transformed data")
        console.log("--------------------------------------------------")
        console.log(grouped)
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