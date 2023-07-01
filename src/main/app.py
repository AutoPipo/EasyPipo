# flask create app
# Author : Ji-yong219
# Project Start:: 2021.03.10.
# Last Modified from Ji-yong 2023.06.22.

from flask import Flask
from src.main.easypipo.index.indexController import contoller as idx_controller
from src.main.easypipo.imageProcess.imageContoller import contoller as img_controller
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
    app.register_blueprint(img_controller, url_prefix="/imageProcess")
    app.register_blueprint(idx_controller)
    app.template_folder = "webapp/templates"
    app.static_folder = "webapp/static"
    app.secret_key = "wh2fdjqw3k4rvna5dml46smv"
    
    UPLOAD_FOLDER = f"{os.getcwd()}/src/main/webapp/static/org_image"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app