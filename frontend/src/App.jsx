import { useEffect, useState } from 'react'

function App() {
  const [tasks, setTasks] = useState([])

  useEffect(() => {
    fetch('/view/tasks')
      .then(res => res.json())
      .then(data => setTasks(data))
      .catch(err => console.error(err))
  }, [])

  return (
    <div>
      <h1>Task List</h1>
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>
            <strong>{task.headline}</strong> - Owner: {task.owner}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
