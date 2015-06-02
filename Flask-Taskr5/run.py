# -*- coding:Utf8 -*-

"""
    Run the main server.
"""

from project import app


if __name__ == '__main__':
    # Start the development server in debug mode
    app.run(debug=True)
