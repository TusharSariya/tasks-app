import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Loading } from '../components/common/Loading'
import { ErrorMessage } from '../components/common/ErrorMessage'

export const UserDetailsPage = () => {
    const { userId } = useParams()
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchUser = async () => {
            try {
                setLoading(true)
                const response = await fetch(`http://127.0.0.1:5000/view/author/${userId}`)
                if (!response.ok) {
                    throw new Error('Failed to fetch user details')
                }
                const data = await response.json()
                setUser(data)
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
            <div style={{ marginTop: '20px' }}>
                <Link to="/org-chart" className="nav-link" style={{ backgroundColor: '#646cff', display: 'inline-block' }}>Back to Org Chart</Link>
            </div>
        </div>
    )
}
