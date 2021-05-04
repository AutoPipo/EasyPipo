'''
# Image to Painting Process

# Start : 21.04.01
# Update : 21.04.12
# Author : Minku Koo
'''

import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from libs.colorCode import HexColorCode
# from colorCode import HexColorCode

class Painting:
    def __init__(self, imagepath):
        self.similarColorMap = np.array([]) # 1차 그림화 이미지
        self.paintingMap = np.array([]) # 2차 그림화 이미지
        
        self.fileBasename = os.path.basename(imagepath) # file name
        self.filename = self.fileBasename.split(".")[0]
        self.image = cv2.imread(imagepath) # Original Image
    
    def blurring(self, div = 32, radius = 20, sigmaColor = 50, medianValue = 5) :
        qimg = self.image.copy()
        # img = image.copy()
        
        
        sigmaColor += (qimg.shape[1] * qimg.shape[0]) // 100000
        radius += (qimg.shape[1] * qimg.shape[0]) // 100000
        
        blurring = cv2.medianBlur(qimg, medianValue)
        blurring = cv2.bilateralFilter(blurring, radius, sigmaColor, 60)
        
        # blurring = blurring // div * div #+ div // 2
        
        return blurring
    
    def __createSimilarColorMap(self, image, value, direction = "h"):
        
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
    
    def getSimilarColorMap(self, image,  value = 15, direction = "h"): #blurImage,
        self.similarColorMap = self.__createSimilarColorMap(image, value = value, direction = direction)
        return self.similarColorMap
        
    def getPaintingColorMap(self, similarImage):
        self.paintingMap = self.__createPaintingMap(similarImage)
        return self.paintingMap
        
    def getColorDict(self, image):
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
                
        return colorDict
    
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
    
    
    
    
    







