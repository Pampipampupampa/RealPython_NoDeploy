# -*- coding:Utf8 -*-

"""
    Flask blog controller
"""

import sqlite3
from flask import (Flask, render_template, request, session, flash, redirect,
                   url_for, g)


########################
#    Main Program :    #
########################

# Database file
DATABASE = "blog.db"

# Create application object
app = Flask(__name__)

# Only uppercase keys are added to the config
# app.config works like a dict.
# class flask.Config(root_path, defaults=None)
# default == dict mapping uppercase variables
app.config.from_object(__name__)


def connect_db():
    """
        Connect to the database.
        Return sqlite3 connection.
    """
    # app dict used here
    return sqlite3.connect(app.config['DATABASE'])


if __name__ == '__main__':
    # Start the development server in debug mode
    app.run(debug=True)
