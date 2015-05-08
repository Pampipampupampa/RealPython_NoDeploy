# -*- coding:Utf8 -*-


"""
    Flask tasks controller
"""

import datetime

from flask import (Flask, render_template, request, session, flash, redirect,
                   url_for)
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

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
    """
        Used as a decorator. It ensure that user is login before
        let him access to the decorated route.
    """
    @wraps(test)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrapper


def flash_errors(form):
    """
        Printer for all errors occuring inside form.
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the {:s} field - {:s}".format(getattr(form, field).label.text, error))


def open_tasks():
    return db.session.query(Task).filter_by(
        status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(
        status='0').order_by(Task.due_date.asc())


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User(form.name.data,
                            form.email.data,
                            form.password.data)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering. Please login.')
                return redirect(url_for('login'))
            except IntegrityError:
                error = 'That username and/or email already exist.'
                return render_template('register.html', form=form, error=error)
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
                session['role'] = user.role
                return redirect(url_for('tasks'))
            else:
                error = 'Invalid username or password. Please try again.'
    return render_template("login.html", form=form, error=error)


@app.route('/tasks/')
@login_required
def tasks():
    return render_template('tasks.html', form=AddTaskForm(request.form),
                           open_tasks=open_tasks(), closed_tasks=closed_tasks())


@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    error = None
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
            return redirect(url_for('tasks'))
    return render_template('tasks.html', form=form, error=error,
                           open_tasks=open_tasks(), closed_tasks=closed_tasks())


@app.route('/complete/<int:task_id>/', )
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        task.update({"status": "0"})
        db.session.commit()
        flash('The task was marked as complete. Well done !')
    else:
        flash('You can only update tasks that belong to you.')
    return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>/', )
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        task.delete()
        db.session.commit()
        flash('The task was deleted. Why not add a new one?')
    else:
        flash('You can only delete tasks that belong to you.')
    return redirect(url_for('tasks'))


@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You were logged out.')
    return redirect(url_for('login'))
