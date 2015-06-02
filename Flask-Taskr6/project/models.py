# -*- coding:Utf8 -*-


from project import db
import datetime


########################
#    Main Program :    #
########################


class Task(db.Model):
    """
        Model representing the task table.
        Use instances and init values to populate the table.
    """

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    posted_date = db.Column(db.Date, default=datetime.datetime.utcnow())
    status = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, name, due_date, priority, posted_date, status, user_id):
        super().__init__()
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.posted_date = posted_date
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return '<Task {0}>'.format(self.name)


class User(db.Model):
    """
        Model representing the user table.
        Use instances and init values to populate the table.
    """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='poster')
    role = db.Column(db.String, default='user')

    def __init__(self, name=None, email=None, password=None, role=None):
        super().__init__()
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User {0}>'.format(self.name)
