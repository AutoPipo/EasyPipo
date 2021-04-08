'''
# Image to Painting Process

# Start : 21.04.01
# Update : 21.04.08
# Author : Minku Koo
'''

import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from colorCode import HexColorCode

class Painting:
    def __init__(self, imagepath):
        self.similarColorMap = np.array([]) # 1차 그림화 이미지
        self.paintingMap = np.array([]) # 2차 그림화 이미지
        
        self.fileBasename = os.path.basename(imagepath) # file name
        self.filename = self.fileBasename.split(".")[0]
        self.image = cv2.imread(imagepath) # Original Image
    
    def blurring(self, image, div = 32, radius = 40, sigmaColor = 70, medianValue = 5) :
        # image = self.image.copy()
        # img = image.copy()
        # qimg = img // div * div + div // 2
        
        qimg = image.copy()
        
        sigmaColor += (qimg.shape[1] * qimg.shape[0]) // 100000
        radius += (qimg.shape[1] * qimg.shape[0]) // 100000
        
        blurring = cv2.bilateralFilter(qimg,  radius, sigmaColor, 60)
        blurring = cv2.medianBlur(blurring, medianValue)
        
        # blurring = cv2.resize(blurring, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        return blurring
    
    def __createSimilarColorMap(self, value = 15, direction = "h"):
        div = 32
        img = self.image.copy()
        image = img // div * div + div // 2
        
        # image = self.image.copy()
        
        # map = []
        # image_size_ = image.shape[0]
        
        # colorCode = HexColorCode().hexColorCodeList
        # colorDict = {}
        c = 2
        for y, row in enumerate(image[:-1*c+1]):
            for x, bgr in enumerate(row[:-1*c+1]):
                if y%c==0 and x%c==0 : 
                    sum1 = np.sum(self.image[y:y+c, x:x+c], axis=0)
                    sum_ =np.sum(sum1, axis=0)
                    
                    b, g, r = sum_ // (c*c)
                    image[y:y+c, x:x+c] = np.array([b, g, r])
                    
        '''
        for y, row in enumerate(image[1:-1]):
            # if y % 300 == 0: print("similar color processing...", y, "/", image_size_)
            for x, bgr in enumerate(row[1:-1]):
                blue, green, red = bgr
                
                for c in [-1, 1]:
                    if direction == "v": 
                        b, g, r = image[y+c, x]
                        cellColor = image[y+c, x]
                    else: 
                        b, g, r = image[y, x+c]
                        cellColor = image[y, x+c]
                        
                    if b==blue and g==green and r==red: pass
                    
                    elif  b-value< blue <b+value and \
                    g-value< green <g+value and \
                    r-value< red <r+value:
                        image[y][x] = cellColor
                        break
                    
                    if direction == "v": 
                        b, g, r = image[y, x+c]
                        cellColor = image[y, x+c]
                    else: 
                        b, g, r = image[y+c, x]
                        cellColor = image[y+c, x]
                        
                    if b==blue and g==green and r==red: pass
                    
                    elif  b-value< blue <b+value and \
                    g-value< green <g+value and \
                    r-value< red <r+value: 
                        # line.append( [b, g, r] )
                        image[y][x] = cellColor#np.array([ b, g, r ])
                        # colorChange = True
                        break
        '''      
        return image
    
    def __createPaintingMap(self, colorImage):
        def calcSimilarColor(color, hexColors):
            
            minColor = {} # key: abs / value : hexColorCode
            blue, green, red = color
            for hex in hexColors :
                b, g, r = self.__hex2bgr(hex)
                if abs( sum( color ) - sum([b, g, r]) ) >100: continue
                value = abs(b-blue)  + abs(r-red)  + abs(g-green)
                
                minColor[value] = np.array([b, g, r])
                if value ==0: return np.array([b, g, r])
            return np.array( minColor[ min(minColor.keys()) ] )
        
        import time
        start = time.time()
        
        map = colorImage.copy()
        colorCode = HexColorCode().hexColorCodeList
        colorDict = {}
        c = 2
        for y, row in enumerate(colorImage[:-1*c+1]):
            # if y % 200 ==0: print("merge color process..:", y)
            for x, color in enumerate(row[:-1*c+1]):
                if y%c==0 and x%c==0 : 
                    color = tuple(color)
                    if color in colorDict.keys():
                        # map[y][x] = np.asarray(colorDict[ color ])
                        map[y:y+c, x:x+c] = colorDict[ color ]
                    else:
                        hexColor = calcSimilarColor(color, colorCode)
                        # map[y][x] = np.asarray(hexColor)
                        map[y:y+c, x:x+c] = hexColor
                        colorDict[ color ] = hexColor
        print("Merge Color Map End//")
        print("비교 시간 :", round((time.time() - start), 3) ,"초.." )
        return map
    
    def getSimilarColorMap(self,  value = 15, direction = "h"): #blurImage,
        self.similarColorMap = self.__createSimilarColorMap(value = value, direction = direction)
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
        return tuple(int(hex[i:i+2], 16) for i in (4, 2, 0))
        
        
if __name__ == "__main__":
    '''
    * How to Use?
    
    painting = Painting( "./imageDir/image.jpg")
    blurImage = painting.blurring(radius = 20, sigmaColor = 40, medianValue=5)
    
    similarMap = painting.getSimilarColorMap(blurImage, value = 15, direction = "h" )
    paintingMap = painting.getPaintingColorMap(similarMap)
    
    colorDict = painting.getColorDict(paintingMap)
    '''
    pass
    
    
    
    
    







