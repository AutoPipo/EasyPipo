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
from libs.drawLine import DrawLine

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
    image = reducial(img, 64)

    # 선 그리기
    drawLineTool = DrawLine(image)
    image2 = drawLineTool.getDrawLine()


    image2 = cv2.convertScaleAbs(image2)



    
    # 선 합성
    # image3 = imageMerge(image, image2)

    # image2 = cv2.convertScaleAbs(image2)
    # image3 = cv2.convertScaleAbs(image3)

    # 색 추출
    colorNames, colors = getColorFromImage(image)


    colors2 = """
FF0000,00FF00,0000FF,
CD5C5C,7FFFD4,
00FFFF,E9967A,00FA9A,
00FFFF,F08080,
00FF7F,48D1CC,FA8072,
98FB98,00CED1,
FF4500,ADFF2F,5F9EA0,
DC143C,7FFF00,
708090,B22222,7CFC00,
E0FFFF,8B0000,
008000,AFEEEE,C71585,
90EE90,B0E0E6,
FFC0CB,9ACD32,B0C4DE,
FFB6C1,32CD32,
4682B4,FF69B4,3CB371,
ADD8E6,FF1493,
8FBC8F,87CEEB,DB7093,
228B22,87CEFA,
BDB76B,2E8B57,00BFFF,
F0E68C,6B8E23,
6495ED,EEE8AA,808000,
4169E1,FAFAD2,
556B2F,7B68EE,FFFFE0,
006400,1E90FF,
FFFACD,66CDAA,0000CD,
FFFF00,40E0D0,
00008B,FFD700,20B2AA,
000080,FFEFD5,
008B8B,191970,FFE4B5,
008080,DCDCDC,
FFDAB9,F0FFF0,D3D3D3,
FFA07A,F5FFFA,
C0C0C0,FFA500,F0FFFF,
A9A9A9,FF8C00,
F0F8FF,808080,FF7F50,
F8F8FF,696969,
FF6347,F5F5F5,2F4F4F,
FF4500,FFF0F5,
778899,E6E6FA,FFE4E1,
CD853F,D8BFD8,
FAEBD7,D2691E,DDA0DD,
FFF5EE,800000,
EE82EE,FFFAFA,8B4513,
FF00FF,F5F5DC,
A52A2A,FF00FF,FAF0E6,
A0522D,DA70D6,
FDF5E6,8B0000,FFF8DC,
FFFAF0,DEB887,
FFEBCD,FFFFF0,D2B48C,
FFE4E4,BA55D3,
BC8F8F,FFDEAD,9932CC,
9370DB,8A2BE2,
9400D3,8B008B,6A5ACD,
800080,F5DEB3,
483D8B,4B0082,B8860B,
F4A460,DAA520,
000000,FFFFFF,
472B09,683B04,432F16,65441C,492902,5D3A0F,
076C0E,104913,17731D,1F6724,24782A,06B912,1E6723,
6F0505,4A1010,6B1111,9E0E09,720A06,400603,370D0C,450B09,
0E0F58,06086D,040695,090A56,1A1A42,14154B""".split(',')

    for idx in range(len(colors2)):
        colors2[idx] = tuple(int(colors2[idx][i:i+2], 16) for i in (4, 2, 0))

    colorNames2 = [ str(i+1) for i in range(len(colors2)) ]

    colorNames, colors = colorNames2, colors2
    print(f'색 {len(colorNames)}개')



    # 라벨 추출
    img_lab, lab = getImgLabelFromImage(colors, image)

    img = image2.copy()
    # img = image.copy()

    # contour, hierarchy 추출
    contours, hierarchy, thresh = getContoursFromImage(img)


    # 결과 이미지 백지화
    result_img = makeWhiteFromImage(image)

    # 결과이미지 렌더링
    # image를 넣으면 원본이미지에 그려주고, result_img에 넣으면 백지에 그려줌
    result_img = setColorNumberFromContours(result_img, thresh, contours, hierarchy, img_lab, lab, colorNames)

    cv2.imwrite(f'./web/static/render_image/result_{image_name}', result_img)
    image_name = 'result_'+image_name

    return jsonify(img_name=image_name, area_arr=area_arr)