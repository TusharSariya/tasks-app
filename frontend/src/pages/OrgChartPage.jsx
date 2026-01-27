// src/pages/TasksPage.jsx
import { getSubordinates } from '../hooks/getSubordinates'
import { Loading } from '../components/common/Loading'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { Tree, TreeNode } from 'react-organizational-chart';

const OrgNode = ({ person, subordinatesMap }) => {
    // 1. Get children for the current person
    const children = subordinatesMap[person.id] || []

    return (
        // 2. Render the current person
        <TreeNode label={<div style={{ border: '1px solid black', padding: '8px' }}>{person.name}</div>}>
            {/* 3. Recursively render children */}
            {children.map(child => (
                <OrgNode key={child.id} person={child} subordinatesMap={subordinatesMap} />
            ))}
        </TreeNode>
    )
}

const ExampleTree = () => (
    <Tree label={<div>Root</div>}>
        <TreeNode label={<div>Child 1</div>}>
            <TreeNode label={<div>Grand Child</div>} />
        </TreeNode>
    </Tree>
);

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
        <Tree label={<div style={{ border: '1px solid black', padding: '8px' }}>{rootPerson.name}</div>}>
            {/* Start looking for subordinates of ID 1 */}
            {(subordinatesMap[1] || []).map(child => (
                <OrgNode key={child.id} person={child} subordinatesMap={subordinatesMap} />
            ))}
        </Tree>
    )
}