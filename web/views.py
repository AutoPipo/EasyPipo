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
from libs.utils import *
from libs.imageProcessing import *

views = Blueprint("server", __name__)


@views.route("/", methods=["GET"])
def index():
    
    if "id" not in session:
        session["id"] = get_job_id()
    
    # session.pop("id")
    return render_template("index.html")


@views.route("/convert", methods=["POST"])
def convert():
    line_detail = json.loads(request.form['line_detail'])
    blur_size = json.loads(request.form['blur_size'])
    area_arr = json.loads(request.form['area_arr'])
    image_path = request.form['image_path']
    
    image_path = './web'+image_path[2:]
    image_name = os.path.basename(image_path)


    ###### minku koo

    # brush = Brush(image_path, session["id"], "./databases/test.db")
    
    # edge = brush.getEdge( line_detail = line_detail, blur_size= blur_size)
    
    # canvas = brush.drawLine(edge, regions=area_arr)

    # brush.save("./web/static/render_image/")
    # brush.finish()
    


    # 원본 이미지 불러오기
    img = getImageFromPath(image_path)

    # 색 일반화
    image = reducial(img)

    # 선 그리기
    image2 = drawLine(image)
    
    # 선 합성
    image3 = imageMerge(image, image2)

    # image2 = cv2.convertScaleAbs(image2)
    image3 = cv2.convertScaleAbs(image3)

    # 색 추출
    colorNames, colors = getColorFromImage(image3)
    print(f'색 {len(colorNames)}개')

    # contour 추출
    contours = getContoursFromImage(image3)

    # 라벨 추출
    img_lab, lab = getImgLabelFromImage(colors, image)

    # 결과 이미지 백지화
    result_img = makeWhiteFromImage(image)

    # 결과이미지 렌더링
    result_img = setColorNumberFromContours(result_img, contours, img_lab, lab, colorNames)

    cv2.imwrite(f'./web/static/render_image/result_{image_name}', result_img)
    image_name = 'result_'+image_name
    


    return jsonify(img_name=image_name, area_arr=area_arr)