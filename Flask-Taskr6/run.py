# -*- coding:Utf8 -*-

"""
    Run the main server.
"""

import os
from project import app


if __name__ == '__main__':
    # Start the development server in debug mode
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
