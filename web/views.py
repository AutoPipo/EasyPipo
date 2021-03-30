# flask server
# Author : minku Koo
# Project Start:: 2021.03.10
# Last Modified from Ji-yong 2021.03.30

from flask import Flask, request, render_template, jsonify, Blueprint, redirect, url_for
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sqlite
import json
import os
from libs.brush import Brush

views = Blueprint("server", __name__)

@views.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@views.route("/convert", methods=["POST"])
def convert():
    img_size = json.loads(request.form['img_size'])
    img_size_origin = json.loads(request.form['img_size_origin'])
    area_arr = json.loads(request.form['area_arr'])
    image_path = request.form['image_path']

    print(f'img_size: {img_size}')
    print('\n\n')
    print(f'img_size_origin: {img_size_origin}')
    print('\n\n')
    
    image_path = './web'+image_path[2:]
    image_name = os.path.basename(image_path)
    print(image_path)

    for item in area_arr:
        print(item)

    brush = Brush(image_path, "./databases/test.db")
    edge = brush.getEdge( blur_size = 7, block_size = 11, c = 5)
    canvas = brush.drawLine(edge, regions=[])
    
    # brush.showImage(title="hello")
    brush.save()



    return jsonify(img_name=image_name, img_size=img_size, img_size_origin=img_size_origin, area_arr=area_arr)