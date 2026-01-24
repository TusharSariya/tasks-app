from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timezone
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_ECHO'] = True
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

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    author = db.relationship("Author", back_populates="account") #creates an account field in author


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

    # Updated to Many-to-Many using the secondary table
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

    due_date = datetime(2026, 1, 7, 9, 0)
    meeting_prep_mon = Task(headline="monday meeting prep", content="lorem ipsum how the buisness makes money on monday", date=due_date, owners=[emily])

    due_date3 = datetime(2026, 1, 9, 9, 0)
    meeting_prep_wed = Task(headline="wednesday meeting prep", content="lorem ipsum how the buisness makes money on wednesday", date=due_date3, owners=[emily])

    due_date2 = datetime(2026, 1, 14, 9, 0)
    project_1   = Task(headline="project about stuff", content="stuff stuff stuff", date=due_date2,owners=[steven,evan])

    first_post = Post(headline="this is the first post", content="lorem ipsum how to make money",author=jones)

    first_comment = Comment(content="example comment",task=meeting_prep_wed,author=jones)
    second_comment = Comment(content="example comment",task=meeting_prep_wed,author=emily)

    db.session.add_all([blockbuster,hermione,shaddowheart,ron,dumbeldore,sauron,paul])
    db.session.add_all([jones, emily, steven, meeting_prep_mon, meeting_prep_wed, project_1, first_post, first_comment, second_comment])
    db.session.commit()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# http://127.0.0.1:5000/view/tasks
@app.route("/view/tasks")
def viewtasks():
    tasks = db.session.query(Task, Author).join(Task.owners).all()
    # Return a list of dictionaries as JSON
    print(tasks)
    json = []
    for task in tasks:
        json.append({
            "Author": task.Author.name,
            "Headline": task.Task.headline,
            "State": task.Task.state.value,
            "comments": [{"content": comment.content, "author": comment.author.name} for comment in task.Task.comments]
        })
    
    return jsonify(json)

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
    
    subs = []

    bfs = []

    bfs.append((name,0))

    while bfs:
        curname,curlevel = bfs.pop(0)
        if curlevel == end_level:
            continue
        #this logic assumes names are unique
        subordinates = Author.query.filter_by(name=curname).all()[0].subordinates
        for sub in subordinates:
            if curlevel >= start_level-1:
                subs.append({"name":sub.name,"distance":curlevel+1})
            bfs.append((sub.name,curlevel+1))

    print(subs)
    return subs

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
        auth = auth.boss # this magic 
        reportingstruct.add(auth.account.username)

    auth = Author.query.filter_by(name=name2).first()

    while auth is not None and auth.account.username not in reportingstruct:
        auth = auth.boss

    if auth.account.username in reportingstruct:
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


if __name__ == '__main__':
    app.run(debug=True)