import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Loading } from '../components/common/Loading'
import { ErrorMessage } from '../components/common/ErrorMessage'

export const UserDetailsPage = () => {
    const { userId } = useParams()
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [posts, setPosts] = useState([])
    const [tasks, setTasks] = useState([])
    const [comments, setComments] = useState([])

    useEffect(() => {
        const fetchUser = async () => {
            try {
                setLoading(true)
                const response = await fetch(`http://127.0.0.1:5000/view/author/${userId}`)
                if (!response.ok) {
                    throw new Error('Failed to fetch user details')
                }
                const data = await response.json()
                console.log(data)
                setUser(data)

                // Fetch posts for this user
                if (data.name) {
                    const postsResponse = await fetch(`http://127.0.0.1:5000/view/post?name=${encodeURIComponent(data.name)}`)
                    if (postsResponse.ok) {
                        const postsData = await postsResponse.json()
                        setPosts(postsData)
                    }
                }

                // Fetch tasks for this user
                const tasksResponse = await fetch(`http://127.0.0.1:5000/view/author/${userId}/tasks`)
                if (tasksResponse.ok) {
                    const tasksData = await tasksResponse.json()
                    setTasks(tasksData)
                }

                // Fetch comments for this user
                const commentsResponse = await fetch(`http://127.0.0.1:5000/view/author/${userId}/comments`)
                if (commentsResponse.ok) {
                    const commentsData = await commentsResponse.json()
                    setComments(commentsData)
                }

            } catch (err) {
                setError(err.message)
            } finally {
                setLoading(false)
            }
        }

        if (userId) {
            fetchUser()
        }
    }, [userId])

    if (loading) return <Loading />
    if (error) return <ErrorMessage error={error} />
    if (!user) return <div>User not found</div>

    return (
        <div className="card">
            <h1>User Details</h1>
            <div style={{ textAlign: 'left', marginTop: '20px' }}>
                <p><strong>ID:</strong> {user.id}</p>
                <p><strong>Name:</strong> {user.name}</p>
                <p><strong>Age:</strong> {user.age}</p>
                <p><strong>Height:</strong> {user.height}m</p>
                <p><strong>Boss:</strong> {user.boss_name || 'None'}</p>
                <p><strong>Subordinates Count:</strong> {user.subordinates_count}</p>
            </div>

            <div style={{ textAlign: 'left', marginTop: '30px', display: 'flex', flexDirection: 'column', gap: '30px' }}>

                {/* Posts Section */}
                <div>
                    <h2>Posts</h2>
                    {posts.length === 0 ? (
                        <p>No posts found.</p>
                    ) : (
                        <div className="posts-list">
                            {posts.map(post => (
                                <div key={post.id} style={{
                                    border: '1px solid #ddd',
                                    borderRadius: '8px',
                                    padding: '15px',
                                    marginBottom: '10px',
                                    backgroundColor: '#f9f9f9',
                                    color: '#333'
                                }}>
                                    <h3 style={{ marginTop: 0 }}>{post.headline}</h3>
                                    <p>{post.content}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Tasks Section */}
                <div>
                    <h2>Tasks</h2>
                    {tasks.length === 0 ? (
                        <p>No tasks found.</p>
                    ) : (
                        <div className="tasks-list">
                            {tasks.map((task, index) => (
                                <div key={index} style={{
                                    border: '1px solid #ddd',
                                    borderRadius: '8px',
                                    padding: '15px',
                                    marginBottom: '10px',
                                    backgroundColor: '#fff',
                                    color: '#333'
                                }}>
                                    <h3 style={{ marginTop: 0 }}>{task.headline}</h3>
                                    <p><strong>Status:</strong> {task.state}</p>
                                    <p>{task.content}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Comments Section */}
                <div>
                    <h2>Comments</h2>
                    {comments.length === 0 ? (
                        <p>No comments found.</p>
                    ) : (
                        <div className="comments-list">
                            {comments.map((comment, index) => (
                                <div key={index} style={{
                                    border: '1px solid #ddd',
                                    borderRadius: '8px',
                                    padding: '10px',
                                    marginBottom: '10px',
                                    backgroundColor: '#f0f0f0',
                                    color: '#333',
                                    fontSize: '0.9rem'
                                }}>
                                    <p style={{ margin: 0, fontStyle: 'italic' }}>"{comment.content}"</p>
                                    <p style={{ margin: '5px 0 0', fontSize: '0.8rem', color: '#666' }}>
                                        {comment.on_task ? `On Task: ${comment.on_task}` : `On Post: ${comment.on_post}`}
                                    </p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

            </div>

            <div style={{ marginTop: '20px' }}>
                <Link to="/org-chart" className="nav-link" style={{ backgroundColor: '#646cff', display: 'inline-block' }}>Back to Org Chart</Link>
            </div>
        </div>
    )
}
