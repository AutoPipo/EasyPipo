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
from multiprocessing_generator import ParallelGenerator
from matplotlib import pyplot as plt


# 색 리스트 반환 함수 (Minku koo)
@numba.jit(forceobj = True)
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
def setLabel(image, num, pt):
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.3 # 0.6
    thickness = 1 # 2

    textsize = cv2.getTextSize(num, fontface, scale, thickness)[0]
    pt = (int(pt[0]-(textsize[0]/2)+1), int(pt[1]+(textsize[1]/2)))


    cv2.putText(image, num, pt, fontface, scale, (0, 0, 0), thickness, 8)


# 컨투어 내부의 색을 평균내서 어느 색인지 체크
@numba.jit(forceobj = True)
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


@numba.jit(forceobj = True)
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


# @numba.jit(forceobj = True)
def getRadiusCenterCircle(raw_dist):
    dist_transform = cv2.distanceTransform(raw_dist, cv2.DIST_L2, maskSize=5)
    # points = [list(dist_transform)[i] for i in range(0, len(dist_transform), 300) if list(dist_transform)[i] > 50]
    # print(type(list(dist_transform)[50]), list(dist_transform)[50])
    points = 1
    _, radius, _, center = cv2.minMaxLoc(dist_transform)

    # result = cv2.normalize(dist_transform, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)
    # minVal, maxVal, a, center = cv2.minMaxLoc(result)

    return radius, center, points


# import psutil
# import ray
# import scipy.signal

@numba.jit(forceobj = True)
def setColorNumberFromContours(img, thresh, contours, hierarchy, img_lab, lab, colorNames):
    num_cpus = psutil.cpu_count(logical=False)

    ray.init(num_cpus=num_cpus)

    @ray.remote
    def f(image, random_filter):
        # Do some image processing.
        print('h')
        return scipy.signal.convolve2d(image, random_filter)[::5, ::5]

    image_id = ray.put(image)
    ray.get([f.remote(image_id, filters[i]) for i in range(num_cpus)])

    return img

@numba.jit(forceobj = True)
def mp_filter(thresh, splited_contours, contours, hierarchy, img_lab, lab, colorNames):
    k = -1

    # 컨투어 별로 체크
    for idx in trange(len(splited_contours), file=sys.stdout, desc='Set Numbering'):
        contour = contours[idx]

        # 면적 
        if cv2.contourArea(contour) < 100: continue

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

    return img


# @numba.jit(forceobj = True)
def setColorNumberFromContours2(img, thresh, contours, hierarchy, img_lab, lab, colorNames):
    # 컨투어 별로 체크
    for idx in trange(len(contours), file=sys.stdout, desc='Set Numbering'):
    # for idx in range(len(contours)):
        # print(f'contours..... {idx} / {len(contours)} \t {round(idx / len(contours)*100, 1)}%', end='\r')
        contour = contours[idx]


        # 면적 
        if cv2.contourArea(contour) < 80: continue

        # 이거 아마 폐곡선 체크
        # if cv2.isContourConvex(contour):
        #     epsilon = 0.1 * cv2.arcLength(contour, True)
        #     contour = cv2.approxPolyDP(contour, epsilon, True)

        chlidren = [ i for i, ii in enumerate(hierarchy[0]) if ii[3] == idx ]


        raw_dist = np.zeros(thresh.shape, dtype=np.uint8)
        cv2.drawContours(raw_dist, contour, -1, (255, 255, 255), 1)
        cv2.fillPoly(raw_dist, pts =[contour], color=(255, 255, 255))
        cv2.fillPoly(raw_dist, pts =[contours[i] for i in chlidren], color=(0, 0, 0))


        # 내접원 반지름, 중심좌표 추출
        radius, center, points = getRadiusCenterCircle(raw_dist)

        # for i in points:
        #     print(i)
        # print("@"*30)

        # 반지름 작은거 무시
        if radius < 10: continue

        
        if center is not None:
            #    컨투어를 그림
            cv2.drawContours(img, [contour], -1, (100, 100, 100), 1)
            # cv2.circle(img, center, int(radius), (0, 255, 0), 1, cv2.LINE_8, 0)

            # 컨투어 내부에 검출된 색을 표시
            color_text = label(img_lab, contour, lab, colorNames)

            center = (center[0], center[1])
            setLabel(img, color_text, center)
            # cv2.imwrite(f'./web/static/render_image/working_img.png', img)


            # contour 1개씩 그려지는거 확인
            # b = np.copy(255-raw_dist)
            # b = cv2.resize(b, dsize=(900, 1186), interpolation=cv2.INTER_AREA)
            # cv2.imshow('draw_contour', b)
            # cv2.waitKey(0)
            
            # ax2 = fig.add_subplot(1, 2, 2)
            # ax2.imshow(img)
            # ax2.set_title('draw_contour')
            # ax2.axis("off")
            # plt.show()

    return img

    
@numba.jit(forceobj = True)
def setColorLabel(img, colorNames, colors):
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1 # 0.6
    thickness = 2 # 2

    for idx in range(len(colors)):
        cv2.putText(img, colorNames[idx], (20, 40*(idx+1)), fontface, scale, (50, 50, 50), thickness, 8)
        cv2.rectangle(img, (60, 40*(idx+1)-20), (90, 40*(idx+1)), tuple([int(i) for i in colors[idx]]), -1, 8)
        # cv2.imwrite(f'./web/static/render_image/working_img.png', img)

    return img