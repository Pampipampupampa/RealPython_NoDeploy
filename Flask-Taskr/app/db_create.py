# -*- coding:Utf8 -*-

import sqlite3
from config import DATABASE_PATH

########################
#    Main Program :    #
########################


if __name__ == '__main__':
    with sqlite3.connect(DATABASE_PATH) as connection:

        cur = connection.cursor()

        cur.execute("""CREATE TABLE tasks (task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL, due_date TEXT NOT NULL,
                    priority INTEGER NOT NULL, status INTEGER NOT NULL)""")

        cur.execute("""INSERT INTO tasks (name, due_date, priority, status)
                    VALUES("Finish this tutorial", "02/03/2014", 10, 1)""")

        cur.execute("""INSERT INTO tasks (name, due_date, priority, status)
                    VALUES("Finish Real Python Course 2", "02/03/2014", 10, 1)""")
