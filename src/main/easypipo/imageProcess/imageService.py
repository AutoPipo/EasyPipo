# Image Service
# Author : Ji-yong219
# Project Start:: 2021.03.10.
# Last Modified from Ji-yong 2023.07.02.

from multiprocessing import Process, Manager
import os
from ast import literal_eval

from ..libs.utils import *
from ..libs.imageProcessing import *
from ..libs.drawLine import DrawLine
from ..libs.painting import Painting, imageExpand

"""reduce color process function for Multiprocessing
File: imageService.py
Created: 2023-06-22

@author: Ji-yong219
LastModifyDate: 
LastModifier: 
"""
def reduce_color_process(idx, image_path, img, cluster, result, colorNames, colors):
    idx = str(idx)

    paintingTool = Painting(image_path)

    print(f'{idx}번 프로세스 컬러 군집화 시작')
    clusteredImage = paintingTool.colorClustering( img, cluster = cluster )
    
    print(f'{idx}번 프로세스 이미지 확장')
    # expandedImage = imageExpand(clusteredImage, guessSize = True)
    expandedImage = imageExpand(clusteredImage, guessSize = False, size=3)
    
    print(f'{idx}번 프로세스 컬러 매칭 시작')
    paintingMap = paintingTool.expandImageColorMatch(expandedImage)

    print(f'{idx}번 프로세스 컬러 추출 시작')
    colorNames_, colors_ = getColorFromImage(paintingMap)

    print(f'{idx}번 프로세스 컬러 {len(colorNames_)}개')
    
    # number_of_color = paintingTool.getNumb
    # erOfColor(paintingMap)
    # print("Number of Color :", number_of_color)

    colorNames[idx] = colorNames_
    colors[idx] = colors_

    result.put(paintingMap)

    return


def process_start(image_name, image_path_o, image_path_r):
    paintingTool = Painting(image_path_o)
    image = paintingTool.image

    cv2.imwrite(f'{os.path.dirname(image_path_r)}/{image_name}', image)
    
    img_name_o = image_name.replace(".", "_origin.")
    cv2.imwrite(f'{os.path.dirname(image_path_r)}/{img_name_o}', image)

    return (
        "#original_img",
        image_name
    )


def reduce_color(image_name, image_path, reduce_data, clusters):
    paintingTool = Painting(image_path)
    paintingTool.image = cv2.imread(image_path)

    # 색 단순화 + 블러 처리
    blurImage = paintingTool.blurring(
        div = 8, 
        radius = 10, 
        sigmaColor =20, 
        medianValue=7
    )

    clusters = [int(i) for i in reduce_data.split(',')[:3]]

    manager = Manager()
    result_list = manager.Queue()
    colorNames_ = manager.dict()
    colors_ = manager.dict()
    processes = []

    for idx, cluster in enumerate(clusters):
        process = Process(
            target=reduce_color_process,
            args=(
                idx+1,
                image_path,
                blurImage,
                cluster,
                result_list,
                colorNames_,
                colors_
            )
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


    painting_map_list = [result_list.get() for _ in range(3)]

    colorNames = str(colorNames_)
    colors = str(colors_)
    
    base_img_path = os.path.dirname(image_path)
    reduce_img_name = image_name.replace(".", "_reduce.")

    for cluster, painting_map in zip(clusters, painting_map_list):
        reduce_img_name_ = image_name.replace(".", f"_reduce_{cluster}.")
        cv2.imwrite(f'{base_img_path}/{reduce_img_name_}', painting_map)

    return (
        "#reduce_img",
        reduce_img_name,
        colorNames,
        colors
    )


def draw_line(image_name, reduce_data, colors):
    colors = literal_eval(colors)
    cluster = colors[reduce_data]
    
    image_path = f"{os.getcwd()}/src/main/webapp/static/render_image/{image_name}"

    paintingTool = Painting(image_path)
    paintingTool.image = cv2.imread(image_path)
    paintingMap = paintingTool.image

    # 선 그리기
    drawLineTool = DrawLine(paintingMap)
    lined_image = drawLineTool.getDrawLine()
    lined_image = drawLineTool.drawOutline(lined_image)

    # 레이블 추출
    img_lab, lab = getImgLabelFromImage(cluster, paintingMap)

    base_img_path = os.path.dirname(image_path)
    lined_image_name = image_name.replace("reduce", "linedraw")
    image_lab_name = image_name.replace("reduce", "imglab")
    lab_name = image_name.replace("reduce", "lab")
    cv2.imwrite(f'{base_img_path}/{lined_image_name}', lined_image)
    cv2.imwrite(f'{base_img_path}/{image_lab_name}', img_lab)
    cv2.imwrite(f'{base_img_path}/{lab_name}', lab)

    return (
        "#linedraw_img",
        lined_image_name,
        str(img_lab),
        str(lab)
    )


def numbering_sector(reduce_img_name, linedraw_img_name, reduce_data, colors, colorNames, img_lab, lab):
    colors = literal_eval(colors)
    colorNames = literal_eval(colorNames)
    
    image_path = f"{os.getcwd()}/src/main/webapp/static/render_image/{reduce_img_name}"
    paintingTool = Painting(image_path)
    paintingTool.image = cv2.imread(image_path)
    paintingMap = paintingTool.image.copy()
    
    line_image_path = image_path.replace("reduce", "linedraw")
    paintingTool.image = cv2.imread(line_image_path)
    linedMap = paintingTool.image.copy()

    
    imglab_path = image_path.replace("reduce", "imglab")
    lab_path = image_path.replace("reduce", "lab")
    img_lab = cv2.imread(imglab_path)
    lab = cv2.imread(lab_path)

    # contour, hierarchy 추출
    print(f'컨투어 추출 시작')
    contours, hierarchy, thresh = getContoursFromImage(linedMap.copy())

    # 결과 이미지 백지화
    result_img = makeWhiteFromImage(paintingMap)
    result_img = setBackgroundAlpha(paintingMap, result_img)

    # 결과이미지 렌더링
    # image를 넣으면 원본이미지에 그려주고, result_img에 넣으면 백지에 그려줌
    print(f'넘버링 시작')
    result_img = setColorNumberFromContours(result_img, thresh, contours, hierarchy, img_lab, lab, colorNames[reduce_data], False)

    print(f'컬러 레이블링 시작')
    result_img2 = setColorLabel(result_img.copy(), colorNames[reduce_data], colors[reduce_data])

    print(f'작업 완료')

    base_img_path = os.path.dirname(image_path)
    number_img_name = reduce_img_name.replace("reduce", "_numbering.")
    number_img_name_ = number_img_name = reduce_img_name.replace("reduce", "_numbering.")

    cv2.imwrite(f'{base_img_path}/{number_img_name}', result_img)
    cv2.imwrite(f'{base_img_path}/{number_img_name_}', result_img2)

    return (
            "#numbering_img",
            number_img_name
        )