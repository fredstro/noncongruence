r"""

Application for subgroups of the modular group etc.

Author: Fredrik Stromberg
"""

from flask import Flask
from extensions import mongoeng
import subgroups
import noncong.backend.print_table

def create_app():
    app = Flask(__name__)
    app.config.from_object('noncong.config.app_config')
    mongoeng.init_app(app)
    return app

app = create_app()
