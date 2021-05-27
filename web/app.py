# flask create app

from flask import Flask, Blueprint
from .views import views
import os

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views)
    app.secret_key = "wh2fdjqw3k4rvna5dml46smv"
    
    UPLOAD_FOLDER = os.getcwd() + r'\web\static\org_image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app
