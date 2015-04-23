# -*- coding:Utf8 -*-

"""
    Flask hello World
"""

from flask import Flask

########################
#    Main Program :    #
########################

# Create application object
app = Flask(__name__)

# Use decorator to link the function to a url
@app.route("/")
@app.route("/hello")
def hello_world():
    """
        Define a view which return a string
    """
    return "Hello World"


if __name__ == '__main__':
    # Start the development server
    app.run()
