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

    __tablename__ = "task"

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
