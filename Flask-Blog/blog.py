# -*- coding:Utf8 -*-

"""
    Flask blog controller
"""

import sqlite3
from flask import (Flask, render_template, request, session, flash, redirect,
                   url_for, g)
from functools import wraps

########################
#    Main Program :    #
########################

# Configuration files
# Only works with full path (maybe a python3 bug ?)
DATABASE = "/home/pampi/Documents/Courses/RealPython/Flask-Blog/blog.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = 'hard_to_guess'

# Create application object
app = Flask(__name__)

# Only uppercase keys are added to the config
# app.config works like a dict.
# class flask.Config(root_path, defaults=None)
# default == dict mapping uppercase variables
app.config.from_object(__name__)


def login_required(test):
    @wraps(test)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrapper


def connect_db():
    """
        Connect to the database.
        Return sqlite3 connection.
    """
    # app dict used here
    return sqlite3.connect(app.config['DATABASE'])


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        if request.form['username'] != app.config["USERNAME"] or \
           request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
        else:
            flash("You were successfully logged in.")
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template("login.html", error=error)


@app.route("/main")
@login_required
def main():
    g.db = connect_db()
    # Used try/except clause to catch errors and perform db rollback.
    cursor = g.db.execute('SELECT * FROM posts')
    posts = [dict(title=row[0], post=row[1]) for row in
             cursor.fetchall()]
    g.db.close()
    return render_template("main.html", posts=posts)


@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash("All fields are required. Please try again.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('INSERT INTO posts (title, post) VALUES (?, ?)',
                     ([request.form['title'], request.form['post']]))
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted!')
        return redirect(url_for('main'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    # Start the development server in debug mode
    app.run(debug=True)
