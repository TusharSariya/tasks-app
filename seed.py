from faker import Faker
from main import app, db, Account, Author, Task, Post, Comment, TaskState
import random
from datetime import datetime, timezone

fake = Faker()

def seed_data():
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        db.create_all()
        print("Tables created.")

        authors = []
        accounts = []

        print("Creating 100 users and authors...")
        print("Creating 100 users and authors...")
        for i in range(100):
            
            if i == 0:
                # The Big Boss
                username = "blockbuster"
                name = "Jonny Jones"
                boss = None
                age = 45
                height = 1.85
            else:
                username = fake.unique.user_name()
                name = fake.name()
                # Pick a boss from existing authors to ensure a single tree rooted at Jonny Jones
                # Everyone else has a boss.
                boss = random.choice(authors)
                age = random.randint(20, 65)
                height = round(random.uniform(1.5, 2.0), 2)

            account = Account(username=username)
            accounts.append(account)
            
            author = Author(name=name, age=age, height=height, account=account, boss=boss)
            authors.append(author)
        
        db.session.add_all(accounts)
        db.session.add_all(authors)
        db.session.commit()
        print("Users and Authors committed.")

        print("Creating 100 projects (tasks)...")
        tasks = []
        for _ in range(100):
            headline = fake.sentence(nb_words=6)
            content = fake.paragraph(nb_sentences=3)
            date = fake.future_datetime(end_date="+30d", tzinfo=timezone.utc)
            state = random.choice(list(TaskState))
            
            # Assign 1 to 3 random owners
            owners = random.sample(authors, k=random.randint(1, 3))
            
            task = Task(headline=headline, content=content, date=date, state=state, owners=owners)
            tasks.append(task)
        
        db.session.add_all(tasks)
        db.session.commit()
        print("Tasks committed.")

        print("Creating 100 posts...")
        posts = []
        for _ in range(100):
            headline = fake.sentence(nb_words=8)
            content = fake.text(max_nb_chars=1000)
            author = random.choice(authors)
            
            post = Post(headline=headline, content=content, author=author)
            posts.append(post)
            
        db.session.add_all(posts)
        db.session.commit()
        print("Posts committed.")

        print("Creating 1000 comments...")
        comments = []
        for _ in range(1000):
            content = fake.sentence(nb_words=10)
            author = random.choice(authors)
            
            # Randomly assign to a task or a post
            if random.choice([True, False]): # Comment on Task
                task = random.choice(tasks)
                comment = Comment(content=content, author=author, task=task)
            else: # Comment on Post
                post = random.choice(posts)
                comment = Comment(content=content, author=author, post=post)
            
            comments.append(comment)
            
        db.session.add_all(comments)
        db.session.commit()
        print("Comments committed.")
        print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
