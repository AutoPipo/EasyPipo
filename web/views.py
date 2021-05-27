# flask server
# Author : minku Koo
# Project Start:: 2021.03.10
# Last Modified from Ji-yong 2021.03.30

from flask import Flask, request, render_template, jsonify, Blueprint, redirect, url_for, session, current_app
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sqlite
import json
import os
from libs.brush import Brush
from libs.utils import *
from libs.imageProcessing import *
from libs.drawLine import *
from libs.painting import *

import logging
views = Blueprint("server", __name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@views.route("/", methods=["GET"])
def index():
    if "id" not in session:
        session["id"] = get_job_id()
    
    # session.pop("id")
    return render_template("index.html")

@views.route("/uploadIMG", methods=["POST"])
def upload_img():
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('file')

    errors = {}
    success = False
    filepath = None

    for file in files:
        if file:
            # filename = secure_filename(file.filename) # secure_filename은 한글명을 지원하지 않음
            filename = file.filename
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file_page_path = os.path.splitext(filepath)[0]
            
            # pdf file save (with uploaded)
            file.save(filepath)
            success = True

        else:
            errors[file.filename] = 'File type is not allowed'
    
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 206
        return resp

    # main 
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp

    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp



@views.route("/convert", methods=["POST"])
def convert():
    # line_detail = json.loads(request.form['line_detail'])
    # blur_size = json.loads(request.form['blur_size'])
    # area_arr = json.loads(request.form['area_arr'])
    job = request.form['job']
    image_path = request.form['image_path']
    
    image_path = './web'+image_path[2:]
    image_name = os.path.basename(image_path)

    paintingTool = Painting(image_path)
    image = paintingTool.image

    if job == "start":
        cv2.imwrite(f'./web/static/render_image/{image_name}', image)
        return jsonify(target="#original_img", img_name=image_name)

    elif job == "reduce_color":
        print(f'블러 시작')


        # 색 단순화 + 블러 처리
        blurImage = paintingTool.blurring(  div = 8, 
                                            radius = 10, 
                                            sigmaColor =20, 
                                            medianValue=7)
        
        
        # Way 2 )
        
        print(f'컬러 군집화 시작')
        
        # K-means 알고리즘을 활용한 컬러 군집화
        clusteredImage = paintingTool.colorClustering( blurImage, cluster = 32 )

        
        print(f'이미지 확장 시작')
        expandedImage = imageExpand(clusteredImage, guessSize = True)

        image_name2 = image_name.split('.')[0]+"_reduce." + image_name.split('.')[1]
        cv2.imwrite(f'./web/static/render_image/{image_name2}', expandedImage)


        return jsonify(target="#reduce_img", img_name=image_name2)


    elif job == "draw_line":
        expandedImage = paintingTool.image

        print(f'컬러 매칭 시작')
        # 군집화된 색상을 지정된 색상과 가장 비슷한 색상으로 매칭
        # paintingMap = paintingTool.getPaintingColorMap(clusteredImage)

        # 클러스터 이후, 확장된 이미지에서 색상 동일하게 매칭
        paintingMap = paintingTool.expandImageColorMatch(expandedImage)
        # 요게 지정된 색상과 매칭
        # paintingMap = paintingTool.getPaintingColorMap(paintingMap)


        print(f'컬러 추출 시작', end='\t')
        # 색 추출
        colorNames, colors = getColorFromImage(paintingMap)

        print(f'→\t컬러 {len(colorNames)}개')


        # 선 그리기
        print(f'선 그리기 시작')
        drawLineTool = DrawLine(paintingMap)
        lined_image = drawLineTool.getDrawLine()
        lined_image = drawLineTool.drawOutline(lined_image)

        image_name2 = image_name.split('.')[0]+"_linedraw." + image_name.split('.')[1]
        cv2.imwrite(f'./web/static/render_image/{image_name2}', lined_image)


        # lined_image = cv2.convertScaleAbs(lined_image)
        return jsonify(target="#linedraw_img", img_name=image_name2)



    # 레이블 추출
    img_lab, lab = getImgLabelFromImage(colors, paintingMap)


    # contour, hierarchy 추출
    print(f'컨투어 추출 시작')
    contours, hierarchy, thresh = getContoursFromImage(lined_image.copy())


    # 결과 이미지 백지화
    # result_img = makeWhiteFromImage(expandedImage)
    result_img = paintingMap

    # 결과이미지 렌더링
    # image를 넣으면 원본이미지에 그려주고, result_img에 넣으면 백지에 그려줌
    print(f'넘버링 시작')
    result_img = setColorNumberFromContours2(result_img, thresh, contours, hierarchy, img_lab, lab, colorNames)

    print(f'컬러 레이블링 시작')
    result_img = setColorLabel(result_img, colorNames, colors)

    image_name = 'result_'+image_name
    print(f'작업 완료')


    return jsonify(img_name=image_name, area_arr=area_arr)