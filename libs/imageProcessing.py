# image processing
# Author : Ji-yong
# Project Start:: 2021.04.01
# Last Modified from Ji-yong 2021.04.02


import cv2
import numpy as np
import imutils
from scipy.spatial import distance as dist
import multiprocessing as mp, parmap
import numba
from tqdm import trange
import sys


# 색 리스트 반환 함수 (Minku koo)
def createColorDict(image):
    colorDict = {}
    for y, row in enumerate(image):
        for x, bgr in enumerate(row):
            bgr = tuple(bgr)

            if colorDict == {}:
                colorDict[ bgr ] = [ (x, y) ]
            
            if bgr in colorDict.keys():
                colorDict[bgr].append( (x, y) )

            else:
                colorDict[bgr] = [ (x, y) ]
            
    return colorDict


# 색 일반화 함수 (Ji-yong)
def reducial(img, div):
    # N = 8 #8
    # A = 1024 #1024
    # qimg = np.round( img*(N/A))*( A/N )

    # div = 64 #64
    qimg = img // div * div + div // 2

    qimg = cv2.medianBlur(qimg, 3)
    return qimg

    
# Contour 영역 내에 텍스트 쓰기
# https://github.com/bsdnoobz/opencv-code/blob/master/shape-detect.cpp
def setLabel(image, str, contour, pt):
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.3 # 0.6
    thickness = 1 # 2


    ### 정 가운데 ###
    # size = cv2.getTextSize(str, fontface, scale, thickness)
    # text_width = size[0][0]
    # text_height = size[0][1]

    # x, y, width, height = cv2.boundingRect(contour)
   
    # pt = (x + int((width - text_width) / 2), y + int((height + text_height) / 2))
    #################


    ### 무게 중심 ###
    # M = cv2.moments(contour)

    # contour 0인 경우 (예외)
    # if M['m00'] == 0.0:
    #     return

    # cx = int( M['m10'] / M['m00'] )
    # cy = int( M['m01'] / M['m00'] )
    # pt = (cx, cy)
    ##################


    cv2.putText(image, str, pt, fontface, scale, (0, 0, 0), thickness, 8)


# 컨투어 내부의 색을 평균내서 어느 색인지 체크
def label(image, contour, lab, colorNames):
    mask = np.zeros(image.shape[:2], dtype="uint8")

    cv2.drawContours(mask, [contour], -1, 255, -1)

    mask = cv2.erode(mask, None, iterations=2)
    mean = cv2.mean(image, mask=mask)[:3]

    minDist = (np.inf, None)

    for (i, row) in enumerate(lab):
        d = dist.euclidean(row[0], mean)

        if d < minDist[0]:
            minDist = (d, i)
            
    return colorNames[minDist[1]]

# @numba.jit
def drawLine2(colorMap, value = 1):
    tempMap = np.zeros(colorMap.shape) + 255
    count = 0

    for y, row in enumerate(colorMap):
        line = []
        if y % 10 ==0:
            print(f"line draw: {y} / {len(colorMap)} \t {round(y / len(colorMap)*100, 1)}%", end="\r")

        for x, bgr in enumerate(row):
            colorChange = False
            blue, green, red = bgr

            for c in [-1, 1]:
                try: 
                    b, g, r = colorMap[y+c, x]
                    if b-value< blue <b+value and \
                        g-value< green <g+value and \
                        r-value< red <r+value: pass
                    else : 
                        tempMap[y, x ]=[0, 0, 0]
                        colorChange = True
                        break
                except IndexError as e: pass
                
                try: 
                    b, g, r = colorMap[y, x+c]
                        
                    if b-value< blue <b+value and \
                        g-value< green <g+value and \
                        r-value< red <r+value: pass
                    else : 
                        tempMap[y, x ]=[0, 0, 0]
                        colorChange = True
                        break
                except IndexError as e: pass

            if not colorChange:
                count +=1
                tempMap[y, x ]=[255, 255, 255]
            
    return tempMap

# 이미지 합치는 함수
def imageMerge(image, map):
    new_map = np.zeros(image.shape) + 255

    for y, row in enumerate(image):
        if y % 300 == 0: print("processing...", y, "/", image.shape[0])
        for x, bgr in enumerate(row):
            if map[y][x].tolist() == [0, 0, 0]:
                new_map[y][x] = [0, 0, 0]
            else:
                # new_map[y][x] = bgr.tolist()
                new_map[y][x] = bgr.tolist()
            
    return new_map


# 해당 경로에서 이미지를 numpy형태로 반환
def getImageFromPath(path):
    return cv2.imread(path)


# 해당 이미지에서 색 추출
@numba.jit(forceobj = True)
def getColorFromImage(img):
    # 인식할 색 입력
    temp = [ (idx, color) for (idx, color) in enumerate(   list( createColorDict(img).keys() ),  1   ) ]

    return [str(i[0]) for i in temp], [i[1] for i in temp]


# 해당 이미지에서 contours, hierarchy, image_bin 반환
@numba.jit(forceobj = True)
def getContoursFromImage(img):
    # 이진화
    # cv2.COLOR_BGR2HSV

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # retval, image_bin = cv2.threshold(img, 254,255, cv2.THRESH_BINARY_INV)
    retval, image_bin = cv2.threshold(img, 127,255, cv2.THRESH_BINARY_INV)

    # 이로션
    # image_bin = cv2.erode(image_bin, None, iterations=2)

    contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    return contours, hierarchy, image_bin


def makeWhiteFromImage(img):
    return np.zeros(img.copy().shape) + 255


@numba.jit(forceobj = True)
def getImgLabelFromImage(colors, img):
    lab = np.zeros((len(colors), 1, 3), dtype="uint8")
    for i in range(len(colors)):
        lab[i] = colors[i]

    lab = cv2.cvtColor(lab, cv2.COLOR_BGR2LAB)

    # 색검출할 색공간으로 LAB사용
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    return img_lab, lab


@numba.jit(forceobj = True)
def getRadiusCenterCircle(raw_dist):
    dist_transform = cv2.distanceTransform(raw_dist, cv2.DIST_L2, maskSize=5)
    result = cv2.normalize(dist_transform, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)
    
    minVal, maxVal, a, center = cv2.minMaxLoc(result)

    return center



@numba.jit(forceobj = True)
def setColorNumberFromContours(img, thresh, contours, hierarchy, img_lab, lab, colorNames):

    k = -1

    # 컨투어 별로 체크
    for idx in trange(len(contours), file=sys.stdout, desc='Set Numbering'):
    # for idx in range(len(contours)):
        # print(f'contours..... {idx} / {len(contours)} \t {round(idx / len(contours)*100, 1)}%', end='\r')
        contour = contours[idx]

        # if cv2.isContourConvex(contour):
        #     epsilon = 0.01 * cv2.arcLength(contour, True)
        #     contour = cv2.approxPolyDP(contour, epsilon, True)

        # print(f'이거 봐라:{img_lab.shape}')
        # print(f'이거 봐라2:{thresh.shape}')

        # 면적 
        if cv2.contourArea(contour) < 100: continue

        # 둘레
        # if cv2.arcLength(contour)
        # if contour.shape[0] < 20 : continue

        contour_org = contour.copy()

        child_idx = hierarchy[0, idx, 2]
        
        
        raw_dist = np.zeros(thresh.shape, dtype=np.uint8)
        cv2.drawContours(raw_dist, contour_org, -1, (255, 255, 255), 1)
        cv2.fillPoly(raw_dist, pts =[contour_org], color=(255, 255, 255))

        # 자식 contour 있으면 걔랑 합침 (도넛모양)
        if child_idx != -1:
            child = contours[child_idx]
            cv2.fillPoly(raw_dist, pts =[child], color=(0, 0, 0))

        n_white_pix = np.sum(raw_dist == 255)

        # 작은 컨투어 무시
        if n_white_pix < 200: continue

        center = getRadiusCenterCircle(raw_dist)

        
        if center is not None:
            #    컨투어를 그림
            cv2.drawContours(img, [contour_org], -1, (0, 0, 0), 1)
            # cv2.circle(img, center, int(radius), (0,0,255), 1, cv2.LINE_8, 0)

            # 컨투어 내부에 검출된 색을 표시
            color_text = label(img_lab, contour_org, lab, colorNames)

            center = (center[0], center[1])
            setLabel(img, color_text, contour_org, center)
            cv2.imwrite(f'./web/static/render_image/working_img.png', img)


            # contour 1개씩 그려지는거 확인
            # cv2.imshow('draw_contour', img)
            # cv2.waitKey(0)

    return img