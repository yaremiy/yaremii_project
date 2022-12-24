from .. import db
from . import task_bp
from datetime import datetime
import enum

class PriorityEnum(enum.Enum):
    low = 1
    medium = 2
    high = 3


class ProgressEnum(enum.Enum):
    todo = 1
    doing = 2
    done = 3


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    created = db.Column(db.DateTime,default=datetime.utcnow())
    modified = db.Column(db.DateTime,default=datetime.utcnow())
    deadline = db.Column(db.Date,default=datetime.utcnow())
    priority = db.Column(db.Enum(PriorityEnum), default='low')
    progress = db.Column(db.Enum(ProgressEnum), default='todo')

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    owner = db.relationship("User", backref="own_tasks")
    category = db.relationship("Category", backref="tasks")
    comments = db.relationship('Comment', backref="task")
    
    def repr(self):
        return f"Task('{self.id}', '{self.title}', '{self.deadline}', '{self.priority}', '{self.progress}'"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def repr(self):
        return f"Category('{self.id}', '{self.name}'"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))    
    user = db.relationship('User', backref=db.backref('comments'))