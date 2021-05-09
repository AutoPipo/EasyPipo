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
    # img = getImageFromPath(image_path)


    print(f'블러 시작')

    
    # 클래스 선언
    paintingTool = Painting(image_path)
    image = paintingTool.image
    cv2.imwrite(f'./web/static/render_image/working_img0001.png', image)
    cv2.imwrite(f'./web/static/render_image/working_img.png', image)

    # 색 단순화 + 블러 처리
    blurImage = paintingTool.blurring(  div = 8, 
                                    radius = 10, 
                                    sigmaColor =20, 
                                    medianValue=7)
    cv2.imwrite(f'./web/static/render_image/working_img.png', blurImage)
    cv2.imwrite(f'./web/static/render_image/working_img0002.png', blurImage)
    
    
    # Way 2 )
    print(f'이미지 확장 시작')
    expandedImage = imageExpand(blurImage, guessSize = True)
    cv2.imwrite(f'./web/static/render_image/working_img.png', expandedImage)
    cv2.imwrite(f'./web/static/render_image/working_img0003.png', expandedImage)
    
    print(f'컬러 군집화 시작')
    
    # K-means 알고리즘을 활용한 컬러 군집화
    clusteredImage = paintingTool.colorClustering( expandedImage, cluster = 16, round = 1 )
    cv2.imwrite(f'./web/static/render_image/working_img.png', clusteredImage)
    cv2.imwrite(f'./web/static/render_image/working_img0004.png', clusteredImage)

    print(f'색상 매칭 시작')
    # 군집화된 색상을 지정된 색상과 가장 비슷한 색상으로 매칭
    paintingMap = paintingTool.getPaintingColorMap(clusteredImage)
    

    cv2.imwrite(f'./web/static/render_image/working_img.png', paintingMap)
    cv2.imwrite(f'./web/static/render_image/working_img0005.png', paintingMap)


    print(f'색 추출시작')
    # 색 추출
    colorNames, colors = getColorFromImage(paintingMap)

    print(f'색 {len(colorNames)}개')


    # 선 그리기
    print(f'선 그리기 시작')
    drawLineTool = DrawLine(paintingMap)
    lined_image = drawLineTool.getDrawLine()

    cv2.imwrite(f'./web/static/render_image/working_img.png', lined_image)


    lined_image = cv2.convertScaleAbs(lined_image)
    cv2.imwrite(f'./web/static/render_image/working_img0006.png', lined_image)
    cv2.imwrite(f'./web/static/render_image/working_img.png', lined_image)



    # 레이블 추출
    img_lab, lab = getImgLabelFromImage(colors, paintingMap)


    # contour, hierarchy 추출
    print(f'컨투어 추출 시작')
    contours, hierarchy, thresh = getContoursFromImage(lined_image.copy())


    # 결과 이미지 백지화
    result_img = makeWhiteFromImage(expandedImage)

    # 결과이미지 렌더링
    # image를 넣으면 원본이미지에 그려주고, result_img에 넣으면 백지에 그려줌
    # input("넘버링 시작해?")
    result_img = setColorNumberFromContours2(result_img, thresh, contours, hierarchy, img_lab, lab, colorNames)

    cv2.imwrite(f'./web/static/render_image/result_{image_name}', result_img)
    image_name = 'result_'+image_name

    for i in range(len(colors)):
        print(f'{colorNames[i]}\t{colors[i]}')

    return jsonify(img_name=image_name, area_arr=area_arr)