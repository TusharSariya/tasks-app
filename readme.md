cd frontend
npm run dev


python3 main.py

sqlite3 site.db

.tables
.headers on
.mode column

#TODO

1. Recursive CTEs for Hierarchies
Currently, your viewreportingstruct uses a while loop that accesses auth.boss. In SQLAlchemy, every time you call auth.boss, it potentially triggers a new SQL query (the "N+1" problem). For a deep hierarchy, this is slow. The Challenge: Use a Recursive Common Table Expression (CTE) to fetch the entire reporting chain in a single database hit. This is the "world-class" way to handle tree structures in SQL.

2. Task State Machine & Validation
Tasks in the real world aren't just strings; they have lifecycles. The Challenge: Add a status field (e.g., TODO, IN_PROGRESS, DONE) and implement logic to ensure tasks move through valid states. For example, a task shouldn't be marked DONE unless it has at least one Comment. Furthermore, add a "Priority" system and a route that returns the "Most Urgent" tasks across the whole company.

3. Role-Based Access Control (RBAC)
Right now, anyone can query any author's subordinates or tasks. The Challenge: Implement logic where an Author can only view the Tasks of people they manage (their subordinates). This requires joining the Author hierarchy with the Task owners table in a single complex query.

Creating an API endpoint for org chart data, then a React component to display it. Recommended libraries:
react-organizational-chart — simple, customizable
react-d3-tree — D3-based, more features
react-organigram — lightweight


1. Visual "Heatmap" of Activity
Idea: Show a GitHub-like contribution graph on the User Details page or a dashboard.
How: You already have Tasks (with dates/status) and Comments. You can aggregate activity counts per day using a simple SQL query and render it using a heatmap library (or just CSS grid) on the frontend.
Cool Factor: Instantly shows who is "active" or "slacking".
2. AI-Powered "Task Impact" Score
Idea: Use a simple heuristic (or an LLM API if you want to go big) to calculate an "Impact Score" for each user based on their tasks completed and subordinates managed.
How:
Define a formula: 
(Tasks Completed * 10) + (Subordinates * 5) + (Comments * 1)
.
Display this score as a "Level" or "XP" bar on their profile.
Cool Factor: Gamifies the boring org chart data.
3. Interactive "Force-Directed" Graph for Teams
Idea: Instead of a strict tree, show a graph where nodes (people) are connected if they share tasks or comment on each other's work.
How: Use react-force-graph.
Cool Factor: Reveals the informal structure of the organization (who actually works together vs. who just reports to whom).
4. "Time Travel" Org Chart
Idea: A slider on the Org Chart page that lets you see what the organization looked like in the past (snapshot capability).
How: Add created_at / promoted_at dates to your 
Author
 model. Filter the tree based on the slider date.
Cool Factor: Great for visualizing growth or reorgs.
5. Task "Dependency" Visualizer
Idea: If Task A blocks Task B, show it visually.
How: Add a self-referential blocked_by field to 
Task
. Render a simple dependency tree or Gantt chart.




