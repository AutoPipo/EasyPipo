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
from libs.painting2 import *

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



    # 색 일반화
    # image = reducial(img, 64)
    print(f'색 일반화 시작')
    paintingTool = Painting(image_path)
    image = paintingTool.image
    cv2.imwrite(f'./web/static/render_image/working_img0001.png', image)
    cv2.imwrite(f'./web/static/render_image/working_img.png', image)
    # image = paintingTool.getSimilarColorMap(image)
    # image = paintingTool.blurring(image)
    # image = paintingTool.getPaintingColorMap(image)

    def kmeans_color_quantization(image, clusters=8, rounds=1):
        h, w = image.shape[:2]
        samples = np.zeros([h*w,3], dtype=np.float32)
        count = 0

        for x in range(h):
            for y in range(w):
                samples[count] = image[x][y]
                count += 1

        compactness, labels, centers = cv2.kmeans(samples,
                clusters, 
                None,
                (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
                rounds, 
                cv2.KMEANS_RANDOM_CENTERS)

        centers = np.uint8(centers)
        res = centers[labels.flatten()]
        return res.reshape((image.shape))

    # image = cv2.GaussianBlur(image, (5,5), 0)

    image = cv2.medianBlur(image, 3)
    image = kmeans_color_quantization(image, clusters=20)

    cv2.imwrite(f'./web/static/render_image/working_img0002.png', image)
    cv2.imwrite(f'./web/static/render_image/working_img.png', image)


    # 색 추출
    colorNames, colors = getColorFromImage(image)

    print(f'색 {len(colorNames)}개')


    # 선 그리기
    print(f'선 그리기 시작')
    drawLineTool = DrawLine(image)
    image2 = drawLineTool.getDrawLine()

    cv2.imwrite(f'./web/static/render_image/working_img.png', image2)

    print(f'이미지 확장 시작')
    image = imageExpand(image, guessSize=True)
    image2 = imageExpand(image2, guessSize=True)
    image2 = leaveOnePixel(image2)

    image2 = cv2.convertScaleAbs(image2)
    cv2.imwrite(f'./web/static/render_image/working_img0003.png', image2)
    cv2.imwrite(f'./web/static/render_image/working_img.png', image2)

    
    # 선 합성
    # image3 = imageMerge(image, image2)


    # 라벨 추출
    img_lab, lab = getImgLabelFromImage(colors, image)


    # contour, hierarchy 추출
    print(f'컨투어 추출 시작')
    contours, hierarchy, thresh = getContoursFromImage(image2.copy())


    # 결과 이미지 백지화
    result_img = makeWhiteFromImage(image)

    # 결과이미지 렌더링
    # image를 넣으면 원본이미지에 그려주고, result_img에 넣으면 백지에 그려줌
    result_img = setColorNumberFromContours(result_img, thresh, contours, hierarchy, img_lab, lab, colorNames)

    cv2.imwrite(f'./web/static/render_image/result_{image_name}', result_img)
    image_name = 'result_'+image_name

    for i in range(len(colors)):
        print(f'{colorNames[i]}\t{colors[i]}')

    return jsonify(img_name=image_name, area_arr=area_arr)