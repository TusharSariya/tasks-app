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



