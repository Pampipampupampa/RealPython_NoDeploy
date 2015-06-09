# -*- coding:Utf8 -*-

import os

########################
#    Main Program :    #
########################

# Grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = "flask-taskr.db"
WTF_CSRF_ENABLED = True
SECRET_KEY = "secret"

# Defines the full path of the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# Database URI
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

# Define app mode.
DEBUG = False  # Deployement to heroku
