# -*- coding:Utf8 -*-


import sqlite3
from views import db
from _config import DATABASE_PATH
# from datetime import datetime


# Recup old data from older database schema and add to new one: tasks table
# with sqlite3.connect(DATABASE_PATH) as connection:
#     cur = connection.cursor()
#     cur.execute("""ALTER TABLE tasks RENAME TO old_tasks""")

#     # Create new table `tasks` with ORM
#     db.create_all()

#     # Retrieve data from old one
#     cur.execute("""SELECT name, due_date, priority, status FROM old_tasks ORDER BY task_id ASC""")

#     # Assign all old data to user id == 1
#     data = [(row[0], row[1], row[2], row[3], datetime.utcnow(), 1) for row in cur.fetchall()]
#     cur.executemany("""INSERT INTO tasks (name, due_date, priority, status, posted_date, user_id)
#                     VALUES (?, ?, ?, ?, ?, ?)""", data)

#     # Delete old table tasks
#     cur.execute("DROP TABLE old_tasks")


# Recup old data from older database schema and add to new one: users table
with sqlite3.connect(DATABASE_PATH) as connection:
    cur = connection.cursor()
    cur.execute("""ALTER TABLE users RENAME TO old_users""")

    # # Create new table `tasks` with ORM
    db.create_all()

    # # Retrieve data from old one
    cur.execute("""SELECT name, email, password FROM old_users ORDER BY user_id ASC""")

    # Assign all old data to user id == 1
    data = [(row[0], row[1], row[2], 'user') for row in cur.fetchall()]
    cur.executemany("""INSERT INTO users (name, email, password, role)
                    VALUES (?, ?, ?, ?)""", data)

    # Delete old table tasks
    cur.execute("DROP TABLE old_users")
