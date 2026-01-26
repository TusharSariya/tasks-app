export const TaskComments = ({ comments }) => {
    if (!comments || comments.length === 0) return null
  
    return (
      <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #eee' }}>
        <strong style={{ color: '#666' }}>Comments ({comments.length}):</strong>
        <div style={{ marginTop: '10px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {comments.map((comment, idx) => (
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
    )
  }