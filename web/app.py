# flask create app
# Author : Ji-yong219
# Project Start:: 2021.03.10.
# Last Modified from Ji-yong 2023.06.22.

from flask import Flask
from .views import views
import os

"""App factory
File: app.py
Created: 2023-06-22

@author: Ji-yong219
LastModifyDate: 
LastModifier: 
"""
def create_app():
    app = Flask(__name__)
    app.register_blueprint(views)
    app.secret_key = "wh2fdjqw3k4rvna5dml46smv"
    
    UPLOAD_FOLDER = os.getcwd() + r'\web\static\org_image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app