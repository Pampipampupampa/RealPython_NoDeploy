# -*- coding:Utf8 -*-

"""
    Flask tasks controller
"""

import sqlite3
from flask import (Flask, render_template, request, session, flash, redirect,
                   url_for, g)
from functools import wraps


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


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))
