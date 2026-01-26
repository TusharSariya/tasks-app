import { getStateColor, getStateLabel } from '../../utils/taskUtils'

export const TaskStateBadge = ({ state }) => (
  <span
    style={{
      backgroundColor: getStateColor(state),
      color: 'white',
      padding: '6px 12px',
      borderRadius: '20px',
      fontSize: '12px',
      fontWeight: 'bold',
      textTransform: 'uppercase'
    }}
  >
    {getStateLabel(state)}
  </span>
)