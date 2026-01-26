export const TaskOwners = ({ authors }) => (
    <div style={{ marginBottom: '15px' }}>
      <strong style={{ color: '#666' }}>Owners:</strong>
      <div style={{ marginTop: '5px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
        {authors.map((author, idx) => (
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
  )