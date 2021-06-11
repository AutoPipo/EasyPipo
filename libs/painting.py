'''
# Image to Painting Process

# Start : 21.04.01
# Update : 21.06.12
# Author : Minku Koo
'''

import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from libs.colorCode import HexColorCode
import numba
# from colorCode import HexColorCode

class Painting:
    def __init__(self, imagepath):
        # K-Means 알고리즘 이용한 색상 군집화 이미지
        self.colorClusteredMap = np.array([])
        # 지정된 색상과 매칭한 이미지
        self.paintingMap = np.array([])
        
        self.image = cv2.imread(imagepath) # Original Image
        self.fileBasename = os.path.basename(imagepath) # file base name
        self.filename = self.fileBasename.split(".")[0] # file name
        
        # 지정된 hex color 리스트
        self.hexColorCode =  HexColorCode().hexColorCodeList
        # clustered color list
        self.clusteredColors = np.array([])
    
    # image blurring
    @numba.jit(forceobj = True)
    def blurring(self, 
                div = 8, 
                radius = 10, 
                sigmaColor = 20, 
                medianValue = 5,
                step = 0) :
        """
        Parameters
            div <int> : Reducing numbers of color on Image (default = 8)
            radius <int> : bilateralFilter Parameter (default = 10)
            sigmaColor <int> : bilateralFilter Parameter (default = 20)
            medianValue <int> : medianBlur Parameter (default = 5)
            step <int> : Blurring intensity by step size (0<=step<=5, default = 0)
        returns
            blurring <np.ndarray> : blurred Image
        """
        
        qimg = self.image.copy() # copy original image
        
        step = min(max(0, step), 5) # 1<= step <= 5
        
        imageSize = int( (qimg.shape[1] * qimg.shape[0]) ** 0.5 ) // 100
        # set sigmaColor, radius by imageSize and step
        sigmaColor += min( int(imageSize * 2.5) , 90) + step * 4
        radius += min( int(imageSize * 1.5) , 40) + step * 2
        
        # blurring
        blurring = cv2.bilateralFilter(qimg, radius, sigmaColor, 60)
        blurring = cv2.medianBlur(blurring, medianValue)
        
        # reduce numbers of color
        blurring = blurring // div * div + div // 2
        
        return blurring
   
    # color clustering
    def colorClustering(self, image, cluster = 16, round = 1): 
        self.colorClusteredMap, sse = self.__kmeansColorCluster(image, 
                                                                clusters = cluster, 
                                                                rounds = round)
        return self.colorClusteredMap
   
   # 클러스터 칼라 매칭 + 지정된 색상과 매칭 > 한번에 해결
    def allColorMatcing(self, image):
        hexColors = np.array( [ self.__hex2bgr(hex) for hex in self.hexColorCode ] )
        self.paintingMap = self.__matchColors(image, self.clusteredColors, hexColors)
        #  파라미터 순서 꼭 지켜야함   !!!
        return self.paintingMap
   
    # 여기에 확장한 이미지랑 클러스터 칼라 매칭 
    def expandImageColorMatch(self, expandImage):
        self.colorClusteredMap =  self.__matchColors(expandImage, self.clusteredColors)
        return self.colorClusteredMap
    
    # color on image match with specified hex colors
    def getPaintingColorMap(self, clusteredImage):
        hexColors = np.array( [ self.__hex2bgr(hex) for hex in self.hexColorCode ] )
        self.paintingMap = self.__matchColors(clusteredImage, hexColors)
        return self.paintingMap
    
    # counting numbers of color
    @numba.jit(forceobj = True)
    def getNumberOfColor(self, image):
        """
        Parameters
            image <np.ndarray> : image
        returns
            numbers of color on image <int>
        """
        colorDict = {} # Key : Color Code / Values : Pixel Position
        for y, row in enumerate(image):
            for x, bgr in enumerate(row):
                bgr = tuple(bgr) # np.ndarray convert to tuple
                if colorDict == {}: # if dictionary in empty
                    colorDict[ bgr ] = [ (y, x) ]
                    continue
                
                if bgr in colorDict.keys(): #if pixel color is in dictionary key
                    colorDict[bgr].append( (y, x) )
                else:
                    colorDict[bgr] = [ (y, x) ]
                
        return len(colorDict.keys())
    
    
    # @numba.jit(forceobj = True)
    def __kmeansColorCluster(self, image, clusters, rounds):
        """
        Parameters
            image <np.ndarray> : image
            clusters <int> : number of clustering
            rounds <int> : how many iterate kmeans clustering
        returns
            clustered Image <np.ndarray>
            SSE <float> : Sum of Squared Error
        """
        
        height, width = image.shape[:2]
        samples = np.zeros([ height * width, 3 ], dtype=np.float32)
        
        count = 0
        for x in range(height):
            for y in range(width):
                samples[count] = image[x][y]
                count += 1
        
        '''
        # compactness : SSE
        # labels : array about label, show like 0, 1
        # centers : Cluster centroid Array
        '''
        compactness, labels, centers = cv2.kmeans(
                    samples, # 학습 데이터 정렬, data type = np.float32
                    clusters, # 군집 개수
                    None, # 각 샘플의 군집 번호 정렬
                    
                    
                    # criteria (종료 기준) : 3 element tuple (method, max_iter, epsilon)
                    
                    # method
                    # TERM_CRITERIA_EPS = 특정 정확도에 도달하면 알고리즘 반복 종료
                    # TERM_CRITERIA_MAX_ITER = 특정 반복 횟수 지나면 알고리즘 반복 종료
                    # 두 개 합 = 위 어느 조건이라도 만족하면 종료
                    
                    # max_iter = 최대 반복 횟수 지정
                    # epsilon = 요구되는 특정 정확도
                    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 
                                10000, # max_iter 
                                0.0001), # epsilon 
                    # attempts : 다른 initial centroid 이용해 반복 실행할 횟수
                    attempts = rounds, 
                    
                    # flags : To set the Initial Centroids
                    # cv2.KMEANS_RANDOM_CENTERS > 랜덤 선택
                    # cv2.KMEANS_PP_CENTERS > K-Means++ 알고리즘
                    # cv2.KMEANS_USE_INITIAL_LABELS > 사용자 선택
                    # 중 하나 선택
                    
                    flags = cv2.KMEANS_PP_CENTERS)
        
        centers = np.uint8(centers)
        self.clusteredColors = centers
        res = centers[labels.flatten()]
        
        return res.reshape((image.shape)), round( compactness ** 0.5 // 10, 2 )
    
    # @numba.jit(forceobj = True) 
    def __matchColors(self, colorImage, *matchColors):
        """
        Parameters
            colorImage <np.ndarray> : Image
            matchColors <np.ndarray in tuple> : matching color list (BGR type)
        returns
            img <np.ndarray> : Painted Image
        """
        
        # 여러 색상 리스트중에서 해당 색상과 가장 비슷한 색상을 반환
        def getSimilarColor(color, colors):
            """
            Parameters
                color <np.ndarray> : one color (BGR type)
                colors <np.ndarray> : matching color list
            returns
                similarColor <np.ndarray> : most similar color (BGR type)
            """
            absSum = np.sum( np.square( np.abs(colors - color) ) , axis = 1 )
            indexs = np.where( absSum ==  np.min( absSum ) )[0]
            
            # bgr 색상 거리가 같은 색상이2 개 이상 존재할 경우
            # HSV 거리를 계산해서 판단
            if len(indexs)>1: 
                hsv_distances = []
                nowHSV = self.__bgr_to_hsv(t_color)
                
                for index in indexs:
                    similarColor = colors[ index ]
                    # HSV로 변환
                    hsvValue = self.__bgr_to_hsv(similarColor)
                    # HSV 거리 계산
                    hsvDist = self.__hsvDistance( hsvValue, nowHSV )
                    hsv_distances.append( hsvDist )
                # HSV 거리 최솟값 = 가장 비슷한 색상
                index  = indexs[ hsv_distances.index(min(hsv_distances)) ]
            else:
                index = indexs[0]
                
            return colors[ index ]
        
        img = colorImage.copy()
        
        if len(matchColors)==1:
            oneProcess = False
            clusteredColor = matchColors[0]
        else:
            oneProcess = True
            clusteredColor, paintingColor = matchColors
        
        colorDict = {}
        for y, row in enumerate(colorImage):
            for x, color in enumerate(row):
                t_color = tuple(color)
                if t_color in colorDict:
                    img[y][x] = colorDict[t_color]
                    continue
                
                color = np.array( [int(x) for x in color] )
                
                # clustered color와 매칭
                similarColor = getSimilarColor(color, clusteredColor)
                
                # painting까지 같이하는지
                if oneProcess:
                    # clustered color를 지정된 color와 매칭
                    similarColor = getSimilarColor(similarColor, paintingColor)
                
                img[y][x] = similarColor
                colorDict[t_color] = similarColor
                
        return img
    
    # BGR Color tuple convert to Hex Color String Code
    def __bgr2hex(self, bgr):
        b, g, r = bgr
        return ('%02x%02x%02x' % (b, g, r)).upper()
        
    # Hex Color String Code convert to BGR Color np.array
    def __hex2bgr(self, hex):
        return np.array( [int(hex[i:i+2], 16) for i in (4, 2, 0)] ) 
    
    # convert BGR to HSV
    # https://www.w3resource.com/python-exercises/math/python-math-exercise-77.php
    def __bgr_to_hsv(self, color):
        b, g, r = tuple( color )
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn: h = 0
        elif mx == r: h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g: h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b: h = (60 * ((r-g)/df) + 240) % 360
        if mx == 0: s = 0
        else: s = (df/mx)*100
        
        v = mx*100
        return h, s, v
    
    # calc HSV Color Distatnce
    # https://stackoverflow.com/questions/35113979/calculate-distance-between-colors-in-hsv-space
    def __hsvDistance(self, h1, h2):
        h0, s0, v0 = h1
        h1, s1, v1 = h2
        
        dh = min(abs(h1-h0), 360-abs(h1-h0)) / 180.0
        ds = abs(s1-s0)
        dv = abs(v1-v0) / 255.0
        return (dh*dh+ds*ds+dv*dv) ** 0.5
        

# @numba.jit(forceobj = True)
def imageExpand(image, guessSize=False, size = 3):
    """
    Parameters
        image <np.ndarray> : image
        guessSize <boolean> : expand as appropriate size (default = False)
        size <int> : Size to expand (default = 3)
    returns
        image <np.ndarray> : expanded image
    """
    if guessSize : size = ( 5000 // image.shape[1] ) + 1
    #       INTER_LANCZOS4
    image = cv2.resize(image, None, fx=size, fy=size, interpolation=cv2.INTER_LINEAR)
    
    return  image
    
        
if __name__ == "__main__":
    '''
    * How to Use?
    
    # 클래스 선언
    painting = Painting( "./imagePath/image.jpg")
    
    # Reduce Color and Blurring
    blurImage = painting.blurring(  div = 8, 
                                    radius = 10, 
                                    sigmaColor =20, 
                                    medianValue=7)
    
    # Color Clustering using K-Means
    clusteredImage = painting.colorClustering( blurImage, cluster = 16)
    
    # 이미지 확장, Way 1 or 2 < Select one
    # ===== Way 1 ===== ) 
    expandedImage = imageExpand(clusteredImage, size = 4)
    
    # 확장된 이미지에서 변형된 색상을 군집화된 색상과 매칭
    similarMap = painting.expandImageColorMatch(expandedImage)
    # 군집화된 색상을 지정된 색상과 가장 비슷한 색상으로 매칭
    paintingMap = painting.getPaintingColorMap(similarMap)
    # ==== Way 1 End ==== ) 
    
    
    # ===== Way 2 ===== ) 
    expandedImage = imageExpand(clusteredImage, guessSize = True)
    
    # Way 1의 과정을 하나로 합침
    paintingMap = painting.allColorMatcing(expandedImage)
    # ==== Way 2 End ==== ) 
    
    # 이미지 색상 개수 확인
    number_of_color = painting.getNumberOfColor(paintingMap)
    print("Number of Color :", number_of_color)
    '''
    pass
    
    