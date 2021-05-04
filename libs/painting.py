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
        # K-Means 알고리즘 이용한 색상 군집화 이미지
        self.colorClusteredMap = np.array([]) 
        # 지정된 색상과 매칭한 이미지
        self.paintingMap = np.array([])
        
        self.image = cv2.imread(imagepath) # Original Image
        self.fileBasename = os.path.basename(imagepath) # file name
        self.filename = self.fileBasename.split(".")[0]
    
    
    def blurring(self, 
                div = 8, 
                radius = 10, 
                sigmaColor = 20, 
                medianValue = 5,
                step = 0) :
                
        qimg = self.image.copy()
        
        imageSize = int( (qimg.shape[1] * qimg.shape[0]) ** 0.5 ) // 100
        sigmaColor += min(imageSize * 2, 80) + step * 4
        radius += min( imageSize , 30) + step * 2
        
        blurring = cv2.bilateralFilter(qimg, radius, sigmaColor, 60)
        blurring = cv2.medianBlur(blurring, medianValue)
        
        blurring = blurring // div * div + div // 2
        
        return blurring
   
    def colorClustering(self, image, cluster = 16, round = 1): #blurImage,
        self.colorClusteredMap, sse = self.__kmeansColorCluster(image, 
                                                                clusters = cluster, 
                                                                rounds = round)
        return self.colorClusteredMap
        
    def getPaintingColorMap(self, clusteredImage):
        self.paintingMap = self.__createPaintingMap(clusteredImage)
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
        
        # for j in range(2, 7):
            # km_temp, sse = kmeans_color_quantization(img, clusters=j*8)
            # print("클러스터 개수:", j*8, "SSE:", sse)
        
        return res.reshape((image.shape)), round( compactness ** 0.5 // 10, 2 )
    
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
    
    def __bgr2hex(self, bgr):
        hexColor = ""
        for color in bgr: hexColor+= hex(color).split('x')[-1]
        return hexColor
    
    def __hex2bgr(self, hex):
        return np.array( [int(hex[i:i+2], 16) for i in (4, 2, 0)] ) 


        
def imageExpand(image, guessSize=False, size = 3):
    if guessSize : size = ( 5000 // image.shape[1] ) + 1
    #       INTER_LANCZOS4
    image = cv2.resize(image, None, fx=size, fy=size, interpolation=cv2.INTER_LINEAR)
    # _, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
    return  image
    
        
if __name__ == "__main__":
    '''
    * How to Use?
    
    # 클래스 선언
    painting = Painting( "./imagePath/image.jpg")
    
    # 색 단순화 + 블러 처리
    blurImage = painting.blurring(  div = 8, 
                                    radius = 10, 
                                    sigmaColor =20, 
                                    medianValue=7)
    
    
    # Way 1 )
    expandedImage = imageExpand(blurImage, size = 4)
    # Way 2 )
    expandedImage = imageExpand(blurImage, guessSize = True)
    
    
    # K-means 알고리즘을 활용한 컬러 군집화
    clusteredImage = painting.colorClustering( expandedImage, cluster = 16, round = 1 )
    # 군집화된 색상을 지정된 색상과 가장 비슷한 색상으로 매칭
    paintingMap = painting.getPaintingColorMap(clusteredImage)
    
    # 이미지 색상 개수 확인
    number_of_color = painting.getNumberOfColor(paintingMap)
    print("Number of Color :", number_of_color)
    '''
    pass
    
    