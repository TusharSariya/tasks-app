export const ErrorMessage = ({ error }) => (
    <div style={{ padding: '20px', color: 'red' }}>
      <h2>Error loading tasks</h2>
      <p>{error}</p>
    </div>
  )