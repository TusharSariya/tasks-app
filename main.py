from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.string(30), nullable=False)
    age = db.Column(db.Integer,nullable=False)
    height = db.Column(db.Float,nullable=False)
    subordinates = db.Column(db.List,default=[])
    peers        = db.Column(db.List,default=[])
    reporting_to = db.Column(db.String,nullable=True)
    tasks = db.relationship('Task', backref='author', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.string(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date    = db.Column(db.dateTime,default=None,nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    creation_date = db.Column(db.dateTime,default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Task {self.id}>'

with app.app_context():
    db.create_all()
    dentist = Task(content="dentist")

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
