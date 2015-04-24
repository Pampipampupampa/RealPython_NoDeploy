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

# Error handling and automatic code loader
#  --> change code and save --> update take effect inside the browser
# without having to reload it.
app.config["DEBUG"] = True


# Use decorator to link the function to a url
@app.route("/")
@app.route("/hello")
def hello_world():
    """
        Define a view which return a string
    """
    return "Hey buddy"


# Dynamic route text
@app.route("/test/<search_query>")
def search(search_query):
    return search_query


# Dynamic route which cast to integer
@app.route("/integer/<int:value>")
def int_type(value):
    print(value + 1)
    return "correct"


# Dynamic route which cast to float
@app.route("/float/<float:value>")
def float_type(value):
    print(value + 1)
    return "correct"


# Dynamic route which cast to path
@app.route("/path/<path:value>")
def path_type(value):
    print(value)
    return "correct"


@app.route("/name/<name>")
def index(name):
    if name.lower() == "michael":
        # Status code can be guess by Flask but better to define it myself
        return "Hello {}".format(name), 200
    else:
        return "Not found", 404


if __name__ == '__main__':
    # Start the development server
    app.run()
