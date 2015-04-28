# -*- coding:Utf8 -*-

from views import db

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
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, name, due_date, priority, status):
        super().__init__()
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def __repr__(self):
        return '<name {:r}>'.format(self.body)


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

    def __init__(self, name=None, email=None, password=None):
        super().__init__()
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {:r}>'.format(self.name)
