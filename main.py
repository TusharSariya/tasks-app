from flask import Flask, render_template
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
    
    jones = Author(name="Jonny Jones", age=25, height=1.8)
    emily = Author(name="Emily Hynes", age=30, height=1.0, boss=jones)
    steven = Author(name="Steven Butt", age=22, height=1.7, boss=emily)
    due_date = datetime(2026, 1, 7, 9, 0)
    # Now we pass a list of authors to 'owners'
    meeting_prep = Task(headline="meeting prep", content="lorem ipsum how the buisness makes money", date=due_date, owners=[emily, jones])
    db.session.add_all([jones, emily, steven, meeting_prep])
    db.session.commit()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route("/viewtasks")
def viewtasks():
    #SELECT task.headline AS task_headline, author.name AS author_name 
    #FROM task 
    #JOIN task_owners ON task.id = task_owners.task_id 
    #JOIN author ON author.id = task_owners.author_id;

    tasks = db.session.query(Task.headline, Author.name).join(Task.owners).all()
    print(tasks)
    return str(tasks)

if __name__ == '__main__':
    app.run(debug=True)