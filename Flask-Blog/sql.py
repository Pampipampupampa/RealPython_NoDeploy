# -*- coding:Utf8 -*-


"""
    Create a SQLite3 table and populate it with data
"""

import sqlite3

########################
#    Main Program :    #
########################


# create a new database if the database doesn't already exist
with sqlite3.connect("blog.db") as db:
    cursor = db.cursor()

    # Delete database table if exist
    cursor.execute("DROP TABLE if exists posts")

    # Add posts table
    cursor.execute("""CREATE TABLE posts
                   (title TEXT, post TEXT)
                   """)

    # Insert dummy data into the table
    cursor.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')
    cursor.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')
    cursor.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent.")')
    cursor.execute('INSERT INTO posts VALUES("Okay", "I\'m okay.")')
