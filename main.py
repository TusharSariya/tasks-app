from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timezone
import enum
import sqltap.wsgi
from sqlalchemy import func
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_ECHO'] = True
app.wsgi_app = sqltap.wsgi.SQLTapMiddleware(app.wsgi_app)
db = SQLAlchemy(app)
CORS(app) # Enable CORS for all routes

class TaskState(enum.Enum):
    NEW = "new"
    IN_PROGRESS = "inprogress"
    FINISHED = "finished"
    DELAYED = "delayed"
    CANCELED = "canceled"

# Association table for the Many-to-Many relationship
task_owners = db.Table('task_owners',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

#all usernames are unique
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    author = db.relationship("Author", back_populates="account") #creates an account field in author

#author names are not unique
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    account = db.relationship("Account", back_populates='author', lazy=True) # allows me to get the Username Author.username.username, creates a author field in account
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False, unique=True) #this is the actual constraint, all users have a unique account
    age = db.Column(db.Integer,nullable=False)
    height = db.Column(db.Float,nullable=False)

    # Self-referential relationship
    boss_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=True) # when you create a subordinate it is associated to the boss and populates the subordinates list
    subordinates = db.relationship('Author', backref=db.backref('boss', remote_side=[id])) #this is magically a list because of how sql alchemy works

    # relationship to Task table, secondary the asociation table for many to many relationship, backref is a reverse relationship, 
    tasks = db.relationship('Task', secondary=task_owners, backref=db.backref('owners', lazy='dynamic'), lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    @property
    def peers(self):
        """Returns a list of other Authors who share the same boss."""
        if self.boss:
            return [x for x in self.boss.subordinates if x.id != self.id]
        return []
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date    = db.Column(db.DateTime,default=None,nullable=True)
    creation_date = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))
    state = db.Column(db.Enum(TaskState), default=TaskState.NEW, nullable=False)

    def __repr__(self):
        return f'<Task {self.id}>'
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    # Relationships for easier data traversal
    #relationships create dynamic sql queries under the hood which is convenient.
    author = db.relationship('Author', backref=db.backref('comments', lazy=True))
    task = db.relationship('Task', backref=db.backref('comments', lazy=True)) # comment.task and task.comment, these are both the actual objects
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

with app.app_context():
    db.drop_all()
    db.create_all()
    blockbuster = Account(username="blockbuster")
    jones = Author(name="Jonny Jones", age=25, height=1.8, account=blockbuster)              # level 0

    hermione = Account(username="hermione")
    emily = Author(name="Emily Hynes", age=30, height=1.0, boss=jones, account=hermione)  # level 1

    shaddowheart = Account(username="Shaddowheart")
    acadia = Author(name="Acadia Philips", age=30, height=1.0, boss=jones, account=shaddowheart)  # level 1

    ron = Account(username="ron")
    steven = Author(name="Steven Butt", age=22, height=1.7, boss=emily,account=ron) # level 2

    dumbeldore = Account(username="dumbledore")
    evan = Author(name="Evan Butt", age=22, height=1.7, boss=emily, account=dumbeldore) # level 2

    sauron = Account(username="sauron")
    greg = Author(name="Gregory Butt", age=22, height=1.7, boss=acadia, account=sauron)  # level 2

    paul = Account(username="Paul")
    Kazawitch = Author(name="Kazawitch Haderach", age=22, height=1.7, boss=greg, account=paul)  # level 3

    tanner = Account(username="Tanner")
    jimbo = Author(name="Jimmy Jimbo", age=22, height=1.7, account=tanner)

    due_date = datetime(2026, 1, 7, 9, 0)
    meeting_prep_mon = Task(headline="monday meeting prep", content="lorem ipsum how the buisness makes money on monday", date=due_date, owners=[emily])

    due_date3 = datetime(2026, 1, 9, 9, 0)
    meeting_prep_wed = Task(headline="wednesday meeting prep", content="lorem ipsum how the buisness makes money on wednesday", date=due_date3, owners=[emily])

    due_date2 = datetime(2026, 1, 14, 9, 0)
    project_1   = Task(headline="project about stuff", content="stuff stuff stuff", date=due_date2,owners=[steven,evan])

    due_date3 = datetime(2026, 1, 14, 9, 0)
    project_2   = Task(headline="another project about stuff", content="another stuff stuff stuff", date=due_date3,owners=[acadia])

    first_post = Post(headline="this is the first post", content="lorem ipsum how to make money",author=jones)

    first_comment = Comment(content="example comment",task=meeting_prep_wed,author=jones)
    second_comment = Comment(content="example comment",task=meeting_prep_wed,author=emily)

    db.session.add_all([blockbuster,hermione,shaddowheart,ron,dumbeldore,sauron,paul,tanner])
    db.session.add_all([jones, emily, steven, meeting_prep_mon, meeting_prep_wed, project_1, first_post, first_comment, second_comment, jimbo])
    db.session.commit()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# http://127.0.0.1:5000/view/tasks
# SELECT task.id AS task_id, task.headline AS task_headline, task.content AS task_content, task.date AS task_date, task.creation_date AS task_creation_date, task.state AS task_state, author.id AS author_id, author.name AS author_name, author.account_id AS author_account_id, author.age AS author_age, author.height AS author_height, author.boss_id AS author_boss_id FROM task JOIN task_owners AS task_owners_1 ON task.id = task_owners_1.task_id JOIN author ON author.id = task_owners_1.author_id
@app.route("/view/tasks")
def viewtasks():
    #you may be wondering Author and Task already have a relationship so why do i need to join them.
    #the reason is to make one efficient query instead of N+1 queries
    time.sleep(0.5)
    tasks = db.session.query(Task, Author).join(Task.owners).all()
    print(tasks)
    json = []
    for task in tasks:
        json.append({
            "Author": task.Author.name,
            "Headline": task.Task.headline,
            "State": task.Task.state.value,
            # task.Task.comments leverages relationships, i wrote it this way because i want to group comments by task
            # this does produce N+1 queries though
            "comments": [{"content": comment.content, "author": comment.author.name} for comment in task.Task.comments]
        })
    
    return jsonify(json)

# http://127.0.0.1:5000/view/tasks/account?username=hermione&start_level=1&end_level=2
@app.route("/view/tasks/account")
def viewtasksaccount():
    username = request.args.get('username')
    start_level = int(request.args.get('start_level',1))
    end_level = int(request.args.get('end_level',1))

    #first you need to get all subbordinates
    #unpack the tuple :galaxy-brain:
    author, = db.session.query(Author.name).join(Account).filter(Account.username == username).first()
    print("--------------------------------------------------------------")
    print(author)
    subs = _viewsubordinates(author,start_level,end_level)

    names = [sub["name"] for sub in subs]+[author]
    print("--------------------------------------------------------------")
    print(names)

    #then you need to get all tasks for yourself and your subbordinates
    #this uses author name which is not unique
    results = db.session.query(Task, Author, Account).\
        join(Task.owners).\
        join(Account).\
        filter(Author.name.in_(names)).all()

    tasks = []

    for row in results:
        tasks.append({
            "headline": row.Task.headline,
            "content": row.Task.content,
            "date": row.Task.date,
            "state": row.Task.state.value,
            "author": row.Author.name,
            "account": row.Account.username
        })
    return jsonify(tasks)

@app.route("/view/tasks/update")
def viewtasksupdate():
    name = request.args.get('name')
    state = request.args.get('state')
    content = request.args.get('content')

    if not name:
        return jsonify({"error": "no name provided"}), 400

    task = Task.query.filter_by(headline=name).first()
    if not task:
        return jsonify({"error": "task not found"}), 404
    
    newState = TaskState(state)
    task.state = newState #this is the actual staged change
    db.session.commit()
    return jsonify({"success": "succefully updated task"}),200



# http://127.0.0.1:5000/view/subordinates?name=Jonny+Jones
# http://127.0.0.1:5000/view/subordinates?name=Jonny+Jones&start_level=1&end_level=2
@app.route("/view/subordinates")
def viewsubordinates():
    # Get the 'boss_id' from the URL query parameters (e.g., ?boss_id=1)
    name = request.args.get('name')
    start_level = int(request.args.get('start_level',1))
    end_level = int(request.args.get('end_level',1))

    if not name:
        print("no name provided")
        return "no name provided"
    
    return _viewsubordinates(name,start_level,end_level)

def _viewsubordinates(name,start_level,end_level):

    subs = [] # suboardinate,suboardinate_id, boss, boss_id,depth

    bfs = []

    bfs.append((name,0))

    while bfs:
        curname,curlevel = bfs.pop(0)
        if curlevel == end_level:
            continue
        #this logic assumes names are unique, this produces N+1 queries
        subordinates = Author.query.filter_by(name=curname).all()[0].subordinates
        for sub in subordinates:
            if curlevel >= start_level-1:
                subs.append({"name":sub.name,"id":sub.id,"boss":curname,"boss_id":sub.boss_id,"distance":curlevel+1})
            bfs.append((sub.name,curlevel+1))

    print(subs)
    return subs



# ai magic CTE
# http://127.0.0.1:5000/view/subordinates/efficient?username=hermione
# http://127.0.0.1:5000/view/subordinates/efficient?username=hermione&start_level=1&end_level=2
@app.route("/view/subordinates/efficient")
def viewsubordinatesefficient():
    # Get the 'boss_id' from the URL query parameters (e.g., ?boss_id=1)
    name = request.args.get('name')
    start_level = int(request.args.get('start_level', 1))
    end_level = int(request.args.get('end_level', 1))

    if not name:
        return jsonify({"error": "no name provided"}), 400
    
    # Get the starting author
    start_author = Author.query.filter_by(name=name).first()
    if not start_author:
        return jsonify({"error": "Author not found"}), 404

    # 1. Define the Anchor: Start with the specific author at level 0
    subordinates = db.session.query(
        Author.id,
        Author.name,
        Author.boss_id,
        func.cast(0, db.Integer).label('level')
    ).filter(Author.name == name).cte(name="subordinates", recursive=True)

    # 2. Define the Recursive Step: Find subordinates of people already in the CTE
    # Join on Author.boss_id == subordinates.c.id (find people whose boss is in the CTE)
    subordinates = subordinates.union_all(
        db.session.query(
            Author.id,
            Author.name,
            Author.boss_id,
            (subordinates.c.level + 1).label('level')
        ).join(subordinates, Author.boss_id == subordinates.c.id)
    )

    # 3. Execute the query, filter by level, and exclude the starting person (level 0)
    results = db.session.query(
        subordinates.c.name,
        subordinates.c.level
    ).filter(
        subordinates.c.level >= start_level,
        subordinates.c.level <= end_level
    ).all()

    # 4. Format results
    subs = [{"name": r.name, "distance": r.level} for r in results]
    
    return jsonify(subs)

# SELECT author.id AS author_id, author.name AS author_name, author.age AS author_age, author.height AS author_height, author.boss_id AS author_boss_id FROM author WHERE author.name = ?
# http://127.0.0.1:5000/view/reportingstruct?name=Kazawitch+Haderach
@app.route("/view/reportingstruct")
def viewreportingstruct():
    name = request.args.get('name')
    if name is None:
        return("no name provided")

    auth = Author.query.filter_by(name=name).first()
    if not auth:
        return jsonify({"error": "Author not found"}), 404
        
    ret = []

    while auth.boss is not None:
        auth = auth.boss # this magic does sql queries under the hood, this is a bit insane tbh, ctes are better
        ret.append(auth.name)
    return jsonify(ret)

# http://127.0.0.1:5000/view/closestshared/lead?name1=Steven+Butt&name2=Evan+Butt -> emily hynes/hermione
# http://127.0.0.1:5000/view/closestshared/lead?name1=Steven+Butt&name2=Jimmy+Jimbo -> invalid
@app.route("/view/closestshared/lead")
def viewclosestsharedlead():
    name1 = request.args.get('name1')
    name2 = request.args.get('name2')
    if name1 is None or name2 is None:
        return("two names not provided")
    
    reportingstruct = set([])

    auth = Author.query.filter_by(name=name1).first()
    if not auth:
        return jsonify({"error": "Author not found"}), 404
    
    reportingstruct.add(auth.account.username)

    while auth.boss is not None:
        auth = auth.boss # this magic, but it also does an sql query for every call, which is bad
        reportingstruct.add(auth.account.username)

    auth = Author.query.filter_by(name=name2).first()
    if not auth:
        return jsonify({"error": "Author not found"}), 404

    while auth is not None and auth.account.username not in reportingstruct:
        auth = auth.boss

    if auth is not None and auth.account.username in reportingstruct:
        return jsonify({"closest lead":auth.account.username})
    
    return jsonify({"failed": "is this an invalid org structure?"})

# magic i dont understand
# WITH RECURSIVE ancestors(id, name, boss_id) AS (SELECT author.id AS id, author.name AS name, author.boss_id AS boss_id FROM author WHERE author.name = ? UNION ALL SELECT author.id AS author_id, author.name AS author_name, author.boss_id AS author_boss_id FROM author JOIN ancestors ON ancestors.boss_id = author.id) SELECT ancestors.name AS ancestors_name FROM ancestors
# http://127.0.0.1:5000/view/reportingstruct/cte?name=Kazawitch+Haderach
@app.route("/view/reportingstruct/cte")
def viewreportingstructcte():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "no name provided"}), 400

    # 1. Define the Anchor: Start with the specific author
    ancestors = db.session.query(
        Author.id,
        Author.name,
        Author.boss_id
    ).filter(Author.name == name).cte(name="ancestors", recursive=True)

    # 2. Define the Recursive Step: Join the CTE with the Author table to find the boss
    ancestors = ancestors.union_all(
        db.session.query(
            Author.id,
            Author.name,
            Author.boss_id
        ).join(ancestors, ancestors.c.boss_id == Author.id)
    )

    # 3. Execute the query and fetch results
    results = db.session.query(ancestors.c.name).all()

    if not results:
        return jsonify({"error": "Author not found"}), 404

    # results[0] is the author themselves, so we skip it to match your original logic
    ret = [r[0] for r in results][1:]
    return jsonify(ret)

# http://127.0.0.1:5000/view/post?name=Jonny+Jones
@app.route("/view/post")
def viewpost():
    name = request.args.get('name')
    if name is None:
        return("no name provided")
    
    # SELECT post.id AS post_id, post.headline AS post_headline, post.content AS post_content, post.author_id AS post_author_id FROM post JOIN author ON author.id = post.author_id 
    posts = db.session.query(Post).join(Author).filter(Author.name == name).all()
    
    # Return a list of headlines so Flask can serialize it
    return jsonify([post.headline for post in posts])

# http://127.0.0.1:5000/view/author/1
@app.route("/view/author/<int:id>")
def viewauthor(id):
    author = Author.query.get(id)
    if not author:
        return jsonify({"error": "Author not found"}), 404

    return jsonify({
        "id": author.id,
        "name": author.name,
        "age": author.age,
        "height": author.height,
        "boss_name": author.boss.name if author.boss else None,
        "subordinates_count": len(author.subordinates)
    })


if __name__ == '__main__':
    app.run(debug=True)