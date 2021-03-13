# flask app
from flask import Flask, Blueprint
from .server import server

def create_app():
    app = Flask(__name__)
    app.register_blueprint(server)
    return app
