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

views = Blueprint("server", __name__)

@views.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@views.route("/convert", methods=["POST"])
def convert():
    img_size = json.loads(request.form['img_size'])
    img_size_origin = json.loads(request.form['img_size_origin'])
    area_arr = json.loads(request.form['area_arr'])
    img_name = 'a5.jpg'

    print(f'img_size: {img_size}')
    print('\n\n')
    print(f'img_size_origin: {img_size_origin}')
    print('\n\n')
    
    for area in area_arr:
        print(area)

    return jsonify(img_name=img_name, img_size=img_size, img_size_origin=img_size_origin, area_arr=area_arr)