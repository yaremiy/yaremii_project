from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .. import db, login_manager

assosiation_table = db.Table('task_user', 
db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    about_me = db.Column(db.String(120), nullable=True, default='Just simple user')
    last_seen = db.Column(db.DateTime, default=datetime.now())

    tasks = db.relationship('Task', secondary=assosiation_table, backref=db.backref('collaborators'))    

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password=password)
        print(self.password)
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def repr(self):
        return f"User('{self.username}', '{self.email}'"


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))
