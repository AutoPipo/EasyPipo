'''
# Image to Painting Process

# Start : 21.04.01
# Update : 21.05.04
# Author : Minku Koo
'''

import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
# from libs.colorCode import HexColorCode
from colorCode import HexColorCode

class Painting:
    def __init__(self, imagepath):
        self.colorClusteredMap = np.array([]) # 1차 그림화 이미지
        self.paintingMap = np.array([]) # 2차 그림화 이미지
        
        self.image = cv2.imread(imagepath) # Original Image
        self.fileBasename = os.path.basename(imagepath) # file name
        self.filename = self.fileBasename.split(".")[0]
        
    
    def blurring(self, div = 16, radius = 20, sigmaColor = 50, medianValue = 5) :
        qimg = self.image.copy()
        
        imageSize = qimg.shape[1] * qimg.shape[0]
        sigmaColor += imageSize // 100000
        radius += imageSize // 100000
        
        blurring = cv2.medianBlur(qimg, medianValue)
        blurring = cv2.bilateralFilter(blurring, radius, sigmaColor, 60)
        
        blurring = blurring // div * div + div // 2
        
        return blurring
    '''
    def __createSimilarColorMap_org(self, image, value, direction = "h"):
        
        # image = self.image.copy()
        image = image.copy()
        
        for y, row in enumerate(image[1:-1]):
            for x, bgr in enumerate(row[1:-1]):
                for c in [-1, 1]:
                    if direction == "v": 
                        cellColor = image[y+c, x]
                    else: 
                        cellColor = image[y, x+c]
                    
                    
                    if (cellColor - value < bgr).all() and\
                    ( bgr < cellColor + value).all():
                        # if not np.array_equal(bgr, cellColor) : 
                        image[y][x] = cellColor
                        break
                        
                    if direction == "v": 
                        cellColor = image[y, x+c]
                    else: 
                        cellColor = image[y+c, x]
                        
                    if (cellColor - value < bgr).all() and\
                    ( bgr < cellColor + value).all():
                        # if not np.array_equal(bgr, cellColor) : 
                        image[y][x] = cellColor
                        break
        
        return image
    
    def __createSimilarColorMap_bfs(self, img, value, direction = "h"):
        
        # image = self.image.copy()
        image = img.copy()
        emap = np.zeros((image.shape[0], image.shape[1]))
        width, height = image.shape[1], image.shape[0]
        values = [value*1.0]
        
        def isSimilarColor(cell, other):
            if np.array_equal(cell, other): return True # False
            cell = np.array([ int(x) for x in cell ])
            other = np.array([ int(x) for x in other ])
            
            sub = cell - other
            # print("sum( sub ** 2) ** 0.5>>", sum( sub ** 2) ** 0.5)
            if sum( sub ** 2) ** 0.5 < values[0]:
                return True
            else: return False
        
        
        def bfs(y, x, img):
            cimg = img.copy()
            queue = [(y, x)]
            check = [(y, x)]
            colors = {}
            
            c = 0
            while queue:
                y, x = queue.pop(0)
                c+=1
                if c> width * height // 36: break
                # if y>200: print("y over 200")
                if y>0:
                    y_, x_ = y-1, x
                    if isSimilarColor(cimg[y_][x_], cimg[y][x]) and (y_, x_) not in check:
                        if emap[y_][x_] == 0:
                            check.append( (y_, x_) )
                            queue.append( (y_, x_) )
                            # colors.append( tuple(cimg[y_][x_]) )
                            if tuple(cimg[y_][x_]) in colors.keys():
                                colors[tuple(cimg[y_][x_])] +=1
                            else: colors[tuple(cimg[y_][x_])] = 1
                            emap[y_][x_] = 1
                    
                if x>0:
                    y_, x_ = y, x-1
                    if isSimilarColor(cimg[y_][x_], cimg[y][x]) and (y_, x_) not in check:
                        if emap[y_][x_] == 0:
                            check.append( (y_, x_) )
                            queue.append( (y_, x_) )
                            if tuple(cimg[y_][x_]) in colors.keys():
                                colors[tuple(cimg[y_][x_])] +=1
                            else: colors[tuple(cimg[y_][x_])] = 1
                            emap[y_][x_] = 1
                    
                if y<height-1 :
                    y_, x_ = y+1, x
                    if isSimilarColor(cimg[y_][x_], cimg[y][x]) and (y_, x_) not in check:
                        if emap[y_][x_] == 0:
                            check.append( (y_, x_) )
                            queue.append( (y_, x_) )
                            if tuple(cimg[y_][x_]) in colors.keys():
                                colors[tuple(cimg[y_][x_])] +=1
                            else: colors[tuple(cimg[y_][x_])] = 1
                            emap[y_][x_] = 1
                    
                if x<width-1 :
                    y_, x_ = y, x+1
                    if isSimilarColor(cimg[y_][x_], cimg[y][x]) and (y_, x_) not in check:
                        if emap[y_][x_] == 0:
                            check.append( (y_, x_) )
                            queue.append( (y_, x_) )
                            if tuple(cimg[y_][x_]) in colors.keys():
                                colors[tuple(cimg[y_][x_])] +=1
                            else: colors[tuple(cimg[y_][x_])] = 1
                            emap[y_][x_] = 1
            
            
            # print("while queue end")
            # print("bfs lenght>", len(check))
            
            # 가장 많은 색 선정
            color = np.array([0,0,0])
            
            # 색 가중 평균
            # for col in colors.keys():
                # color_temp = np.array([int(x) for x in col]) * int(colors[col])
                # color += color_temp
            # color = color // len(check)
            
            maxCol = 0
            # mainCol = []
            for col in colors.keys():
                if maxCol < int(colors[col]):
                    color = np.array([int(x) for x in col])
                
            # print("color,", colors)
            # print("colors>", color)
            if len(colors)>0:
                for y, x in check:
                     cimg[y][x] = color
            # print("emap sum", sum([sum(x) for x in emap]))
            return cimg, check
        
        ischeck = []
        b = 0
        for y in range(height):
            # if y%20==1: print("similar", y)
            for x in range(width):
                
                if int(emap[y, x]) == 1: continue
                if (y, x) not in ischeck:
                    print("go bfs", y, x)
                    image, check = bfs(y, x, image)
                    # print("end bfs")
                    # cv2.imwrite("./tt/t"+str(b)+".jpg", image)
                    ischeck.extend( check )
                    b+=1
            if y%100==0:
                cv2.imwrite("./tt/v"+str(b)+".jpg", image)
        
        return image
    '''
    
    def __kmeansColorCluster(self, image, clusters, rounds):
        h, w = image.shape[:2]
        samples = np.zeros([h*w, 3], dtype=np.float32)
        count = 0

        for x in range(h):
            for y in range(w):
                samples[count] = image[x][y]
                count += 1
        
        '''
        compactness : 각 포인트와 군집화를 위한 중심 간의 거리의 제곱의 합
        labes : 라벨에 대한 배열이며, ‘0’, ‘1’ 등으로 표현
        centers : 클러스터의 중심이 저장된 배열
        '''
        compactness, labels, centers = cv2.kmeans(
                    samples, # 학습 데이터 정렬, data type = np.float32
                    clusters, # 군집 개수
                    None, # 각 샘플의 군집 번호 정렬
                    
                    # 종료 기준, tuple 형태 3개 원소
                    # TERM_CRITERIA_EPS = 특정 정확도에 도달하면 알고리즘 반복 종료
                    # TERM_CRITERIA_MAX_ITER = 특정 반복 횟수 지나면 알고리즘 반복 종료
                    # 두 개 합 = 위 어느 조건이라도 만족하면 종료
                    # max iter = 최대 반복 횟수 지정
                    # epsilon 요구되는 특정 정확도
                    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
                    # 다른 초기 레이블을 이용해 반복 실행할 횟수
                    rounds, 
                    # 초기 중앙 설정 방법
                    # cv2.KMEANS_RANDOM_CENTERS
                    # cv2.KMEANS_PP_CENTERS
                    # cv2.KMEANS_USE_INITIAL_LABELS       중 하나.
                    cv2.KMEANS_RANDOM_CENTERS)

        centers = np.uint8(centers)
        res = centers[labels.flatten()]
        # return res.reshape((image.shape)), compactness ** 0.5
    
        # for j in range(2, 7):
            # km_temp, sse = kmeans_color_quantization(img, clusters=j*8)
            # print("클러스터 개수:", j*8, "SSE:", sse)
        
        
        return res.reshape((image.shape)), compactness ** 0.5
    
    def __createPaintingMap(self, colorImage):
        map = colorImage.copy()
        colorCode =  HexColorCode().hexColorCodeList
        HexColor = np.array( [ self.__hex2bgr(hex) for hex in colorCode ] )
        
        colorDict = {}
        for y, row in enumerate(colorImage):
            for x, color in enumerate(row):
                t_color = tuple(color)
                if t_color in colorDict: 
                    map[y][x] = colorDict[t_color]
                    continue
                    
                absSum = np.sum( np.abs(HexColor - color) , axis = 1 )
                index = np.where( absSum ==  np.min( absSum ) )[0]
                # 여기서 더 비슷한 이미지 2~3개중에 결정하는 코드 삽입
                
                map[y][x] = HexColor[index[0] ]
                colorDict[t_color] = HexColor[index[0] ]
                
        return map
    
    def colorClustering(self, image, clusters = 16, round = 1): #blurImage,
        self.colorClusteredMap, sse = self.__kmeansColorCluster(image, 
                                                                clusters = clusters, 
                                                                rounds = round)
        return self.colorClusteredMap
        
    def getPaintingColorMap(self, similarImage):
        self.paintingMap = self.__createPaintingMap(similarImage)
        return self.paintingMap
        
    def getNumberOfColor(self, image):
        colorDict = {} # Key : Color Code / Values : Pixel Position
        for y, row in enumerate(image):
            for x, bgr in enumerate(row):
                bgr = tuple(bgr)
                if colorDict == {}: 
                    colorDict[ bgr ] = [ (y, x) ]
                    continue
                
                if bgr in colorDict.keys():
                    colorDict[bgr].append( (y, x) )
                else:
                    colorDict[bgr] = [ (y, x) ]
                
        return len(colorDict.keys())
    
    def __bgr2hex(self, bgr):
        hexColor = ""
        for color in bgr: hexColor+= hex(color).split('x')[-1]
        return hexColor
    
    def __hex2bgr(self, hex):
        return np.array( [int(hex[i:i+2], 16) for i in (4, 2, 0)] ) 
        
        
if __name__ == "__main__":
    '''
    * How to Use?
    
    painting = Painting( "./imageDir/image.jpg")
    
    similarMap = painting.getSimilarColorMap( value = 3, direction = "h" )
    blurImage = painting.blurring(similarMap, div = 20, radius = 20, sigmaColor = 40, medianValue = 7)
    paintingMap = painting.getPaintingColorMap(similarMap)
    
    colorDict = painting.getColorDict(paintingMap)
    '''
    pass
    
    
    
    
    







