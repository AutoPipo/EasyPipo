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
def getColorFromImage(img):
    # 인식할 색 입력
    temp = [ (idx, color) for (idx, color) in enumerate(   list( createColorDict(img).keys() ),  1   ) ]

    return [str(i[0]) for i in temp], [i[1] for i in temp]


# 해당 이미지에서 contours, hierarchy, image_bin 반환
def getContoursFromImage(img):
    # 이진화
    # cv2.COLOR_BGR2HSV

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    retval, image_bin = cv2.threshold(gray, 254,255, cv2.THRESH_BINARY_INV)

    # 이로션
    # image_bin = cv2.erode(image_bin, None, iterations=2)

    contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    return contours, hierarchy, image_bin


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


# def mp_filter(x, output):
def doPointPolygonMulti(raw_dist, contour, thresh, num_cores):
    # print(f'바뀐 raw_dist len : {len(raw_dist)}\t{raw_dist.shape}')
    # for i in range(thresh.shape[0]):
    #     for j in range(thresh.shape[1]):
    #         raw_dist[i,j] = cv2.pointPolygonTest(contour, (j,i), True)

    # for idx, item in enumerate(thresh):
    #     for i in range(item.shape[0]):
    #         i += (item.shape[0] * idx)
    #         for j in range(item.shape[1]):
    #             j += (item.shape[0] * idx)
    #             # raw_dist[i][j] = cv2.pointPolygonTest(contour, (j,i), True)
    #             a= cv2.pointPolygonTest(contour, (j,i), True)
    # return [
    #             [cv2.pointPolygonTest(contour, (j+item.shape[1]*idx, i+item.shape[0]*idx), True) for j in range(item.shape[1])]
    #             for idx, item in enumerate(thresh)
    #             for i in range(item.shape[0])
    #         ]
    
    return [
                [cv2.pointPolygonTest(contour, (j+item.shape[1]*idx, i+item.shape[0]*idx), True) for j in range(item.shape[1])]
                for idx, item in enumerate(thresh)
                for i in range(item.shape[0])
            ]

    # temp = raw_dist[ raw_dist.shape[0]/num_cores*x : raw_dist.shape[0]/num_cores*(x+1), :]

    # print(psutil.virtual_memory())  # monitor memory usage
    # output.put(x, cv2.GaussianBlur(img[img.shape[0]/num_processes*x:img.shape[0]/num_processes*(x+1), :], 
    #         (kernel_size, kernel_size), kernel_size/5))


# contour 내심원 반지름이랑 가운데 좌표 반환 함수
def getRadiusCenterCircle2(contour, thresh):
    num_cores = mp.cpu_count() # cpu core 개수
    kernel_size = 11
    tile_size = thresh.shape[0] / num_cores  # Assuming img.shape[0] is divisible by 4 in this case

    # Calculate the distances to the contour
    raw_dist = np.empty(thresh.shape, dtype=np.float32)
    # raw_dist = [[0.0 for j in range(thresh.shape[1])] for i in range(thresh.shape[0])]
    splited_thresh = np.array_split(thresh, num_cores)
    # print(f'원래 raw_dist len : {len(raw_dist)}\t{type(raw_dist)}')

    # results = parmap.map(doPointPolygonMulti, raw_dist, contour, splited_thresh, num_cores, pm_pbar=True, pm_processes=num_cores)
    results = parmap.map(doPointPolygonMulti, raw_dist.shape, contour, splited_thresh, num_cores, pm_pbar=False, pm_processes=num_cores)
    
    results = np.column_stack(results)

    # print('results', len(results), type(results))
    
    # print('results[0]', len(results[0]), type(results[0]))
    
    # print('results[1]', len(results[1]), type(results[1]))


    minVal, maxVal, _, center = cv2.minMaxLoc(np.array(results))


    return maxVal, center
    
# contour 내심원 반지름이랑 가운데 좌표 반환 함수
@numba.jit(forceobj = True)
def getRadiusCenterCircle(contour, thresh):
    # Calculate the distances to the contour

    # raw_dist = np.empty(thresh.shape, dtype=np.float32)
    # for i in range(thresh.shape[0]):
    #     for j in range(thresh.shape[1]):
    #         raw_dist[i,j] = cv2.pointPolygonTest(contour, (j,i), True)

    for i, j in np.ndindex(thresh.shape):
        raw_dist[i,j] = cv2.pointPolygonTest(contour, (j,i), True)
            
    minVal, maxVal, _, center = cv2.minMaxLoc(raw_dist)
    return maxVal, center



@numba.jit(forceobj = True)
def getRadiusCenterCircle3(raw_dist):
    dist_transform = cv2.distanceTransform(raw_dist, cv2.DIST_L2, 5)
    result = cv2.normalize(dist_transform, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)
    return result



# @numba.jit(forceobj = True)
def setColorNumberFromContours(img, thresh, contours, hierarchy, img_lab, lab, colorNames):

    k = -1

    # 컨투어 별로 체크
    for idx in trange(len(contours), file=sys.stdout, desc='Set Numbering'):
    # for idx in range(len(contours)):
        # print(f'contours..... {idx} / {len(contours)} \t {round(idx / len(contours)*100, 1)}%', end='\r')
        contour = contours[idx]

        # 면적 
        if cv2.contourArea(contour) < 10: continue

        # 둘레
        # if cv2.arcLength(contour)
        # if contour.shape[0] < 20 : continue

        contour_org = contour.copy()

        child_idx = hierarchy[0, idx, 2]
        # next_idx = hierarchy[0, idx, 0]
        
        
        raw_dist = np.empty(thresh.shape, dtype=np.float32)
        cv2.drawContours(raw_dist, contour_org, -1, (255, 255, 255), 1)
        cv2.fillPoly(raw_dist, pts =[contour_org], color=(255, 255, 255))
        ret, raw_dist = cv2.threshold(raw_dist, 0, 255, cv2.THRESH_BINARY)

        # 자식 contour 있으면 걔랑 합침 (도넛모양)
        if child_idx != -1:
            child = contours[child_idx]
            # cv2.drawContours(raw_dist, child, -1, (255, 255, 255), 1)
            cv2.fillPoly(raw_dist, pts =[child], color=(0, 0, 0))

        center = getRadiusCenterCircle3(raw_dist)
        
        cv2.imshow('draw_contour', center)
        cv2.waitKey(0)
        continue

        #     c_list = [contour]

        #     if next_idx != -1:
        #         for i in range(idx, next_idx):
        #             c_list.append(contours[i])
                
        #         c_list = tuple(c_list)
        #     else:
        #         c_list.append(child)

        #     # print(f'지금은 {idx}인데, 첫 자식은 {child_idx}이고, 형제는 {next_idx}')

        #     contour = np.concatenate( tuple(c_list) )

        # 내심원 반지름, 좌표 계산
        radius, center = getRadiusCenterCircle(contour, thresh)

        
        if center is not None:
            # 작은 컨투어 무시
            if int(radius) < 3 : continue

            #    컨투어를 그림
            cv2.drawContours(img, contour_org, -1, (0, 0, 0), 1)
            cv2.circle(img, center, int(radius), (0,0,255), 1, cv2.LINE_8, 0)

            # 컨투어 내부에 검출된 색을 표시
            color_text = label(img_lab, contour_org, lab, colorNames)

            center = (center[0]-10, center[1]+4)
            setLabel(img, color_text, contour_org, center)
            cv2.imwrite(f'./web/static/render_image/working_img.png', img)


            # contour 1개씩 그려지는거 확인
            # cv2.imshow('draw_contour', img)
            # cv2.waitKey(0)

    return img