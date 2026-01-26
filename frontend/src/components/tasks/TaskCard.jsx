import { TaskStateBadge } from './TaskStateBadge'
import { TaskOwners } from './TaskOwners'
import { TaskComments } from './TaskComments'

export const TaskCard = ({ task }) => (
  <div
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
      <TaskStateBadge state={task.state} />
    </div>

    <TaskOwners authors={task.authors} />
    <TaskComments comments={task.comments} />
  </div>
)