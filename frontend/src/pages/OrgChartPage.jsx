// src/pages/TasksPage.jsx
import { getSubordinates } from '../hooks/getSubordinates'
import { Loading } from '../components/common/Loading'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { Tree, TreeNode } from 'react-organizational-chart';

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
    return <ExampleTree />
}