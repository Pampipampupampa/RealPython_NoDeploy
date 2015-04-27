# -*- coding:Utf8 -*-

"""
    Flask tasks controller
"""

import sqlite3
from flask import (Flask, render_template, request, session, flash, redirect,
                   url_for, g)
from functools import wraps

# Form class validator
from forms import AddTaskForm

########################
#    Main Program :    #
########################

# Create application object
app = Flask(__name__)

# Populate internal dict with uppercase variables from config.py file.
app.config.from_object('config')


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
    if request.method == "POST":
        if request.form['username'] != app.config["USERNAME"] or \
           request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            return render_template("login.html", error=error)
        else:
            flash("You were successfully logged in.")
            session['logged_in'] = True
            return redirect(url_for('tasks'))
    if request.method == "GET":
        return render_template("login.html")


@app.route('/tasks/')
@login_required
def tasks():
    g.db = connect_db()
    # Get open tasks
    cur = g.db.execute(""" SELECT name, due_date, priority, task_id FROM tasks
                       WHERE tasks.status = 1""")
    open_tasks = [dict(name=row[0], due_date=row[1],
                       priority=row[2], task_id=row[3]) for row in cur.fetchall()]
    # Get closed tasks
    cur = g.db.execute(""" SELECT name, due_date, priority, task_id FROM tasks
                       WHERE tasks.status = 0""")
    closed_tasks = [dict(name=row[0], due_date=row[1],
                         priority=row[2], task_id=row[3]) for row in cur.fetchall()]
    g.db.close()
    # See form.py for more informations
    return render_template('tasks.html', form=AddTaskForm(request.form),
                           open_tasks=open_tasks, closed_tasks=closed_tasks)


@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    g.db = connect_db()
    name = request.form["name"]
    date = request.form["due_date"]
    priority = request.form["priority"]
    if not name or not date or not priority:
        flash("All fields are required. Please try again.")
        return redirect(url_for('tasks'))
    else:
        g.db.execute("""INSERT INTO tasks(name, due_date, priority, status)
                     VALUES(?, ?, ?, 1)""", (name, date, priority))
        g.db.commit()
        g.db.close()
        flash("New entry was successfully posted, Thanks.")
        return redirect(url_for('tasks'))


@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    g.db = connect_db()
    g.db.execute("""UPDATE tasks SET status = 0 WHERE task_id=?""", (task_id, ))
    g.db.commit()
    g.db.close()
    flash('The task was marked as complete.')
    return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    g.db = connect_db()
    g.db.execute("""DELETE FROM tasks WHERE task_id=?""", (task_id, ))
    g.db.commit()
    g.db.close()
    flash('The task was deleted.')
    return redirect(url_for('tasks'))


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))
