# -*- coding:Utf8 -*-

"""
    Flask tasks controller
"""

from flask import (Flask, render_template, request, session, flash, redirect,
                   url_for)
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from forms import AddTaskForm

########################
#    Main Program :    #
########################

# Create application object
app = Flask(__name__)

# Populate internal dict with uppercase variables from config.py file.
app.config.from_object('config')

# Create link between DB and SQLAlchemy and Flask
db = SQLAlchemy(app)

# Import tables
from models import Task


def login_required(test):
    @wraps(test)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrapper


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
    open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
    closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())
    # See form.py for more informations
    return render_template('tasks.html', form=AddTaskForm(request.form),
                           open_tasks=open_tasks, closed_tasks=closed_tasks)


@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(form.name.data,
                            form.due_date.data,
                            form.priority.data,
                            '1')
            db.session.add(new_task)
            db.session.commit()
            flash("New entry was successfully posted, Thanks.")
        else:
            flash("Wrong input field, abort posting task.")
    return redirect(url_for('tasks'))


@app.route('/complete/<int:task_id>/', )
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).update({'status': '0'})
    db.session.commit()
    flash('The task was marked as complete. Well done !')
    return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>/', )
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash('The task was deleted. Why not add a new one?')
    return redirect(url_for('tasks'))


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))
