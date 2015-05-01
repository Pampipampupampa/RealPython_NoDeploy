# -*- coding:Utf8 -*-


"""
    Flask tasks controller
"""

import datetime

from flask import (Flask, render_template, request, session, flash, redirect,
                   url_for)
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy

# Forms
from forms import AddTaskForm, RegisterForm, LoginForm


########################
#    Main Program :    #
########################

# Create application object
app = Flask(__name__)

# Populate internal dict with uppercase variables from _config.py file.
app.config.from_object('_config')

# Create link between DB and SQLAlchemy and Flask
db = SQLAlchemy(app)

# Import tables
from models import Task, User


def login_required(test):
    @wraps(test)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrapper


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User(form.name.data,
                            form.email.data,
                            form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering. Please login.')
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form, error=error)
    if request.method == "GET":
        return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user is not None and user.password == request.form["password"]:
                flash("Welcome ! You were successfully logged in.")
                session['logged_in'] = True
                session['user_id'] = user.user_id
                return redirect(url_for('tasks'))
            else:
                error = 'Invalid username or password. Please try again.'
        else:
            error = 'Both fields are required.'
    return render_template("login.html", form=form, error=error)


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
                            datetime.datetime.utcnow(),
                            '1',
                            session["user_id"])
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
    session.pop('user_id', None)
    flash('You were logged out.')
    return redirect(url_for('login'))
