# -*- coding:Utf8 -*-

from datetime import date

from project import db
from project.models import Task, User

########################
#    Main Program :    #
########################


if __name__ == '__main__':
    # Initialize database schema (all tables, views, triggers)
    db.create_all()

    # Insert user
    db.session.add(User("admin", "ad@min.com", "admin", "admin"))

    # Insert data
    db.session.add(Task("Finish this tutorial", date(2015, 3, 13), 10, date(2015, 2, 13), 1, 1))
    db.session.add(Task("Finish Real Python", date(2015, 3, 13), 10, date(2015, 2, 13), 1, 1))

    # Commit changes
    db.session.commit()
