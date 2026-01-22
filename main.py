from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer,nullable=False)
    height = db.Column(db.Float,nullable=False)

    # Self-referential relationship
    boss_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=True)
    subordinates = db.relationship('Author', backref=db.backref('boss', remote_side=[id])) #this is magically a list because of how sql alchemy works

    tasks = db.relationship('Task', backref='author', lazy=True)

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
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    creation_date = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Task {self.id}>'

with app.app_context():
    db.drop_all()
    db.create_all()
    
    jones = Author(name="Jonny Jones", age=25, height=1.8)
    emily = Author(name="Emily Hynes", age=30, height=1.0, boss=jones)
    due_date = datetime(2026, 1, 7, 9, 0)
    meeting_prep = Task(headline="meeting prep", content="lorem ipsum how the buisness makes money", date=due_date, author=emily)
    db.session.add_all([jones, emily, meeting_prep])
    db.session.commit()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route("/viewtasks")
def viewtasks():
    tasks = db.session.query(Task.headline, Author.name).join(Author).all()
    print(tasks)
    return str(tasks)

if __name__ == '__main__':
    app.run(debug=True)