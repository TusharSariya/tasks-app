// src/pages/TasksPage.jsx
import { getSubordinates } from '../hooks/getSubordinates'
import { Loading } from '../components/common/Loading'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { Tree, TreeNode } from 'react-organizational-chart';

import { useNavigate } from 'react-router-dom';
import { useState } from 'react'; // Don't forget to import useState

const OrgNode = ({ person, subordinatesMap }) => {
    const navigate = useNavigate();
    const children = subordinatesMap[person.id] || []
    const [isHovering, setIsHovering] = useState(false);
    const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

    const handleMouseEnter = (e) => {
        setIsHovering(true);
        setMousePos({ x: e.clientX, y: e.clientY });
    }

    const handleMouseMove = (e) => {
        setMousePos({ x: e.clientX, y: e.clientY });
    }

    const handleMouseLeave = () => {
        setIsHovering(false);
    }

    return (
        <TreeNode label={
            <div
                style={{
                    border: '1px solid #ddd',
                    borderRadius: '8px',
                    padding: '20px',
                    backgroundColor: '#fff',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                    cursor: 'pointer',
                    color: 'black',
                    width: '100px',
                    margin: '0 auto'
                }}
                onMouseEnter={handleMouseEnter}
                onMouseMove={handleMouseMove}
                onMouseLeave={handleMouseLeave}
                onClick={() => navigate(`/user/${person.id}`)}
            >
                {person.name}
                {isHovering && (
                    <div style={{
                        position: 'fixed',
                        top: mousePos.y + 15,
                        left: mousePos.x + 15,
                        background: 'lightgray',
                        padding: '5px',
                        border: '1px solid gray',
                        zIndex: 10,
                        width: 'max-content'
                    }}>
                        Hovering: {person.name}
                    </div>
                )}
            </div>
        }>
            {children.map(child => (
                <OrgNode key={child.id} person={child} subordinatesMap={subordinatesMap} />
            ))}
        </TreeNode>
    )
}

export function OrgChartPage() {
    //jonny is id 1 so lets just assume that and continue
    const { subordinates, loading, error } = getSubordinates("Jonny Jones", 1, 3)
    console.log(subordinates)
    const subordinatesMap = {};
    subordinates.forEach(subordinate => {
        if (!subordinatesMap[subordinate.boss_id]) {
            subordinatesMap[subordinate.boss_id] = []
        }
        subordinatesMap[subordinate.boss_id].push(subordinate)
    })
    console.log(subordinatesMap)

    if (loading) return <Loading />
    if (error) return <ErrorMessage error={error} />
    const rootPerson = { id: 1, name: "Jonny Jones" }
    return (
        <div style={{ overflowX: 'auto', padding: '2rem', width: '100%' }}>
            <Tree label={<div style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '20px',
                backgroundColor: '#fff',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                cursor: 'pointer',
                color: 'black',
                width: '100px',
                margin: '0 auto'
            }}>{rootPerson.name}</div>}>
                {/* Start looking for subordinates of ID 1 */}
                {(subordinatesMap[1] || []).map(child => (
                    <OrgNode key={child.id} person={child} subordinatesMap={subordinatesMap} />
                ))}
            </Tree>
        </div>
    )
}