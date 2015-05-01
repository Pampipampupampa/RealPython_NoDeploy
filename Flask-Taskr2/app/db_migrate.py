# -*- coding:Utf8 -*-


from views import db
from datetime import datetime
from _config import DATABASE_PATH
import sqlite3

with sqlite3.connect(DATABASE_PATH) as connection:
    cur = connection.cursor()
    cur.execute("""ALTER TABLE tasks RENAME TO old_tasks""")

    # Create new table `tasks` with ORM
    db.create_all()

    # Retrieve data from old one
    cur.execute("""SELECT name, due_date, priority, status FROM old_tasks ORDER BY task_id ASC""")

    # Assign all old data to user id == 1
    data = [(row[0], row[1], row[2], row[3], datetime.utcnow(), 1) for row in cur.fetchall()]
    cur.executemany("""INSERT INTO tasks (name, due_date, priority, status, posted_date, user_id)
                    VALUES (?, ?, ?, ?, ?, ?)""", data)

    # Delete old table tasks
    cur.execute("DROP TABLE old_tasks")
