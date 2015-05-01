# -*- coding:Utf8 -*-

from datetime import date

from views import db
from models import Task

########################
#    Main Program :    #
########################


if __name__ == '__main__':
    # Initialize database schema (all tables, views, triggers)
    db.create_all()

    # Insert data
    db.session.add(Task("Finish this tutorial", date(2014, 3, 13), 10, 1))
    db.session.add(Task("Finish Real Python", date(2014, 3, 13), 10, 1))

    # Commit changes
    db.session.commit()
