# flask server
# Author : minku Koo
# Project Start:: 2021.03.10
# Last Modified from Ji-yong 2021.03.30

from flask import Flask, request, render_template, jsonify, Blueprint, redirect, url_for, session
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sqlite
import json
import os
from libs.brush import Brush
from libs.getSession import Sessions

views = Blueprint("server", __name__)
veiws.secret_key = "wh2fdjqw3k4rvna5dml46smv"

@views.route("/", methods=["GET"])
def index():
    session["id"] = Sessions.getSession()
    print("session:",session["id"])
    return render_template("index.html")


@views.route("/convert", methods=["POST"])
def convert():
    line_detail = json.loads(request.form['line_detail'])
    area_arr = json.loads(request.form['area_arr'])
    image_path = request.form['image_path']
    
    image_path = './web'+image_path[2:]
    image_name = os.path.basename(image_path)


    brush = Brush(image_path, "./databases/test.db")
    
    edge = brush.getEdge( line_detail = line_detail, block_size = 11)
    
    canvas = brush.drawLine(edge, regions=area_arr)

    brush.save("./web/static/render_image/")
    brush.finish()

    return jsonify(img_name=image_name, area_arr=area_arr)
    
    