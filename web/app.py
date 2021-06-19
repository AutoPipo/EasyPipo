# flask create app
# Author : Ji-yong219
# Project Start:: 2021.03.10
# Last Modified from Ji-yong 2021.06.12

from flask import Flask
from .views import views
import os

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views)
    app.secret_key = "wh2fdjqw3k4rvna5dml46smv"
    
    UPLOAD_FOLDER = os.getcwd() + r'\web\static\org_image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app