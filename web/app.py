# flask create app

from flask import Flask, Blueprint
from .views import views

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views)
    return app
