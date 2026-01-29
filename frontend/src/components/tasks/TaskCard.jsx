import { useState } from 'react'
import { TaskStateBadge } from './TaskStateBadge'
import { TaskOwners } from './TaskOwners'
import { TaskComments } from './TaskComments'

export const TaskCard = ({ task }) => {
  const [showComments, setShowComments] = useState(false)

  return (
    <div
      onClick={() => setShowComments(!showComments)}
      style={{
        border: '1px solid #ddd',
        borderRadius: '8px',
        padding: '20px',
        backgroundColor: '#fff',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        cursor: 'pointer'
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '15px' }}>
        <h2 style={{ margin: 0, color: '#333' }}>
          {task.headline}
        </h2>
        <TaskStateBadge state={task.state} />
      </div>

      <TaskOwners authors={task.authors} />
      {showComments && <TaskComments comments={task.comments} />}
    </div>
  )
}