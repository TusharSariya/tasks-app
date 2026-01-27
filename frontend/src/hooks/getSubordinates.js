import { useState, useEffect } from 'react'
import { fetchSubordinates } from '../services/subordinatesService'
import { groupTasksByHeadline } from '../utils/taskUtils'

export const getSubordinates = (name, start_level, end_level) => {
  const [subordinates, setSubordinates] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadSubordinates = async () => {
      try {
        setLoading(true)
        const data = await fetchSubordinates(name, start_level, end_level)
        console.log(data)

        setSubordinates(data)
        setError(null)
      } catch (err) {
        console.error('Error fetching tasks:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    loadSubordinates()
  }, [])

  return { subordinates, loading, error }
}