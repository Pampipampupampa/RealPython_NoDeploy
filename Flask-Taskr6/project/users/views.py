# -*- coding:Utf8 -*-

"""
    Flask controller for users.
"""


# Imports
from flask import (render_template, request, session, flash, redirect,
                   url_for, Blueprint)
from functools import wraps
from sqlalchemy.exc import IntegrityError

# Forms
from .forms import RegisterForm, LoginForm
from project import db, bcrypt
from project.models import User


# Config
users_blueprint = Blueprint('users', __name__)


# Tools
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
            return redirect(url_for('users.login'))
    return wrapper


# Routes
@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User(form.name.data,
                            form.email.data,
                            bcrypt.generate_password_hash(form.password.data))
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering. Please login.')
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = 'That username and/or email already exist.'
                return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form)


@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user is not None and bcrypt.check_password_hash(user.password,
                                                               request.form['password']):
                flash("Welcome ! You were successfully logged in.")
                session['logged_in'] = True
                session['user_id'] = user.user_id
                session['role'] = user.role
                session['name'] = user.name
                return redirect(url_for('tasks.tasks'))
            else:
                error = 'Invalid username or password. Please try again.'
    return render_template("login.html", form=form, error=error)


@users_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('name', None)
    flash('You were logged out.')
    return redirect(url_for('users.login'))
