from ast import main
from flask import Flask

app = Flask(__name__)

from app import routes

def create_app():
    app.config.from_pyfile('../instance/config.py')

    app.register_blueprint(main)

    return app