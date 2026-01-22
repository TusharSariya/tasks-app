from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Association table for the Many-to-Many relationship
task_owners = db.Table('task_owners',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer,nullable=False)
    height = db.Column(db.Float,nullable=False)

    # Self-referential relationship
    boss_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=True)
    subordinates = db.relationship('Author', backref=db.backref('boss', remote_side=[id])) #this is magically a list because of how sql alchemy works

    # Updated to Many-to-Many using the secondary table
    tasks = db.relationship('Task', secondary=task_owners, backref=db.backref('owners', lazy='dynamic'), lazy=True)

    @property
    def peers(self):
        """Returns a list of other Authors who share the same boss."""
        if self.boss:
            return [x for x in self.boss.subordinates if x.id != self.id]
        return []

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date    = db.Column(db.DateTime,default=None,nullable=True)
    creation_date = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Task {self.id}>'

with app.app_context():
    db.drop_all()
    db.create_all()
    
    jones = Author(name="Jonny Jones", age=25, height=1.8)              # level 0
    emily = Author(name="Emily Hynes", age=30, height=1.0, boss=jones)  # level 1
    acadia = Author(name="Acadia Philips", age=30, height=1.0, boss=jones)  # level 1
    steven = Author(name="Steven Butt", age=22, height=1.7, boss=emily) # level 2
    greg = Author(name="Gregory Butt", age=22, height=1.7, boss=acadia)  # level 2
    due_date = datetime(2026, 1, 7, 9, 0)
    # Now we pass a list of authors to 'owners'
    meeting_prep = Task(headline="meeting prep", content="lorem ipsum how the buisness makes money", date=due_date, owners=[emily, jones])
    db.session.add_all([jones, emily, steven, meeting_prep])
    db.session.commit()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route("/view/tasks")
def viewtasks():
    #SELECT task.headline AS task_headline, author.name AS author_name 
    #FROM task 
    #JOIN task_owners ON task.id = task_owners.task_id 
    #JOIN author ON author.id = task_owners.author_id;

    tasks = db.session.query(Task.headline, Author.name).join(Task.owners).all()
    print(tasks)
    return str(tasks)


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
        print(curname)
        print(curlevel)
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

if __name__ == '__main__':
    app.run(debug=True)