# image processing
# Author : Ji-yong
# Project Start:: 2021.04.01
# Last Modified from Ji-yong 2021.04.02


import cv2
import numpy as np
import imutils
from scipy.spatial import distance as dist


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


def drawLine(colorMap, value = 1):
    map = []
    tempMap = np.zeros(colorMap.shape) + 255
    count = 0

    for y, row in enumerate(colorMap):
        line = []
        if y % 100 ==0: print("line draw:", y)

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
            
    # print("count:", count)
    return tempMap


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


def getImageFromPath(path):
    return cv2.imread(path)


def getColorFromImage(img):
    # 인식할 색 입력
    temp = [ (idx, color) for (idx, color) in enumerate(   list( createColorDict(img).keys() ),  1   ) ]

    return [str(i[0]) for i in temp], [i[1] for i in temp]


def getContoursFromImage(img):
    # 이진화
    # cv2.COLOR_BGR2HSV

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

    thresh = cv2.erode(thresh, None, iterations=2)


    # 컨투어 검출
    # contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # 컨투어 리스트가 OpenCV 버전에 따라 차이있기 때문에 추가
    if len(contours) == 2:
        contours = contours[0]

    elif len(contours) == 3:
        contours = contours[1]

    return contours


def makeWhiteFromImage(img):
    return np.zeros(img.copy().shape) + 255


def getImgLabelFromImage(colors, img):
    lab = np.zeros((len(colors), 1, 3), dtype="uint8")
    for i in range(len(colors)):
        lab[i] = colors[i]

    lab = cv2.cvtColor(lab, cv2.COLOR_BGR2LAB)

    # 색검출할 색공간으로 LAB사용
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    return img_lab, lab



def setColorNumberFromContours(img, contours, hierarchy, img_lab, lab, colorNames, center):
    # 컨투어 별로 체크
    for idx in range(len(contours)):
        contour = contours[idx]
        contour_org = contour.copy()
        child_idx = hierarchy[0][idx][2]
        
        # 자식 contour 있으면 걔랑 합침 (도넛모양)
        if child_idx != -1:
            contour = np.concatenate( (contour, contours[child_idx]) )

        
        # Calculate the distances to the contour
        raw_dist = np.empty(thresh.shape, dtype=np.float32)
        for i in range(thresh.shape[0]):
            for j in range(thresh.shape[1]):
                raw_dist[i,j] = cv2.pointPolygonTest(contour, (j,i), True)
                
        minVal, maxVal, _, center = cv2.minMaxLoc(raw_dist)

        
        if center is not None:
            # 작은 컨투어 무시
            if int(maxVal) < 3 : continue

            #    컨투어를 그림
            cv2.drawContours(img, [contour_org], -1, (0, 0, 0), 1)

            # 컨투어 내부에 검출된 색을 표시
            color_text = label(img_lab, contour, lab, colorNames)

            setLabel(img, color_text, contour, center)

            # contour 1개씩 그려지는거 확인
            # cv2.imshow('draw_contour', img)
            # cv2.waitKey(0)
    return img