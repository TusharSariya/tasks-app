import { useEffect, useState } from 'react'

function App() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/view/tasks')
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`)
        }
        return res.json()
      })
      .then(data => {
        // Group tasks by headline since one task can have multiple owners
        const grouped = data.reduce((acc, item) => {
          const headline = item.Headline
          if (!acc[headline]) {
            acc[headline] = {
              headline: headline,
              state: item.State,
              authors: [],
              comments: item.comments || []
            }
          }
          // Add author if not already in the list
          if (!acc[headline].authors.includes(item.Author)) {
            acc[headline].authors.push(item.Author)
          }
          return acc
        }, {})
        
        // Convert to array
        const tasksArray = Object.values(grouped)
        setTasks(tasksArray)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching tasks:', err)
        setError(err.message)
        setLoading(false)
      })
  }, [])

  const getStateColor = (state) => {
    const colors = {
      'new': '#2196F3',
      'inprogress': '#FF9800',
      'finished': '#4CAF50',
      'delayed': '#F44336',
      'canceled': '#9E9E9E'
    }
    return colors[state.toLowerCase()] || '#757575'
  }

  const getStateLabel = (state) => {
    return state.charAt(0).toUpperCase() + state.slice(1)
  }

  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <div>Loading tasks...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div style={{ padding: '20px', color: 'red' }}>
        <h2>Error loading tasks</h2>
        <p>{error}</p>
      </div>
    )
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Task List</h1>
      
      {tasks.length === 0 ? (
        <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
          No tasks found
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {tasks.map((task, index) => (
            <div
              key={index}
              style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '20px',
                backgroundColor: '#fff',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '15px' }}>
                <h2 style={{ margin: 0, color: '#333' }}>
                  {task.headline}
                </h2>
                <span
                  style={{
                    backgroundColor: getStateColor(task.state),
                    color: 'white',
                    padding: '6px 12px',
                    borderRadius: '20px',
                    fontSize: '12px',
                    fontWeight: 'bold',
                    textTransform: 'uppercase'
                  }}
                >
                  {getStateLabel(task.state)}
                </span>
              </div>

              <div style={{ marginBottom: '15px' }}>
                <strong style={{ color: '#666' }}>Owners:</strong>
                <div style={{ marginTop: '5px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {task.authors.map((author, idx) => (
                    <span
                      key={idx}
                      style={{
                        backgroundColor: '#e3f2fd',
                        padding: '4px 12px',
                        borderRadius: '12px',
                        fontSize: '14px',
                        color: '#1976d2'
                      }}
                    >
                      {author}
                    </span>
                  ))}
                </div>
              </div>

              {task.comments && task.comments.length > 0 && (
                <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #eee' }}>
                  <strong style={{ color: '#666' }}>Comments ({task.comments.length}):</strong>
                  <div style={{ marginTop: '10px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    {task.comments.map((comment, idx) => (
                      <div
                        key={idx}
                        style={{
                          backgroundColor: '#f5f5f5',
                          padding: '10px',
                          borderRadius: '6px',
                          fontSize: '14px'
                        }}
                      >
                        <div style={{ fontWeight: 'bold', marginBottom: '5px', color: '#555' }}>
                          {comment.author}
                        </div>
                        <div style={{ color: '#666' }}>
                          {comment.content}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App