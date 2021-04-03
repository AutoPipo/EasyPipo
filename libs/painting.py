'''
# Image to Painting Process

# Start : 21.04.01
# Update : 21.04.03
# Author : Minku Koo
'''

import matplotlib.pyplot as plt
import cv2
import numpy as np
from colorCode import HexColorCode

class Painting:
    def __init__(self, imagepath):
        self.similarColorMap = np.array([]) # 1차 그림화 이미지
        self.paintingMap = np.array([]) # 2차 그림화 이미지
        
        self.fileBasename = os.path.basename(imagepath) # file name
        self.filename = self.fileBasename.split(".")[0]
        self.image = cv2.imread(imagepath) # Original Image
    
    def blurring(self, radius = 40, sigmaColor = 70, sigmaSpace = 60, medianValue = 5) :
        image = self.image.copy()
        div = 32
        qimg = image // div * div + div // 2
        
        sigmaColor += (qimg.shape[1] * qimg.shape[0]) // 100000
        radius += (qimg.shape[1] * qimg.shape[0]) // 100000
        
        blurring = cv2.bilateralFilter(qimg,  radius, sigmaColor, sigmaSpace)
        blurring = cv2.medianBlur(blurring, medianValue)
        blurring = cv2.resize(blurring, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        return blurring
    
    def __createSimilarColorMap(self, blurImage, value = 15, direction = "h"):
        map = []
        image_size_ = blurImage.shape[0]
        for y, row in enumerate(blurImage):
            line = []
            if y % 300 == 0: print("similar color processing...", y, "/", image_size_)
            for x, bgr in enumerate(row):
                colorChange = False
                blue, green, red = bgr
                for c in [-1, 1]:
                    try: 
                        if direction == "v": b, g, r = blurImage[y+c, x]
                        else: b, g, r = blurImage[y, x+c]
                            
                        if b==blue and g==green and r==red: pass
                        elif  b-value< blue <b+value and \
                        g-value< green <g+value and \
                        r-value< red <r+value:
                            line.append( [b, g, r] )
                            blurImage[y][x] = [ b, g, r ]
                            colorChange = True
                            break
                    except IndexError as e: pass
                    
                    try: 
                        if direction == "v": b, g, r = blurImage[y, x+c]
                        else: b, g, r = blurImage[y+c, x]
                            
                        if b==blue and g==green and r==red: pass
                        elif  b-value< blue <b+value and \
                        g-value< green <g+value and \
                        r-value< red <r+value: 
                            line.append( [b, g, r] )
                            blurImage[y][x] = [ b, g, r ]
                            colorChange = True
                            break
                    except IndexError as e: pass
                    
                if not colorChange: line.append( [blue, green, red] )
                
            map.append( line )
        
        return np.array(map)
    
    def __createPaintingMap(self, colorImage):
        def calcSimilarColor(color, hexColors):
            minColor = {} # key: abs / value : hexColorCode
            blue, green, red = color
            for hex in hexColors:
                b, g, r = self.__hex2bgr(hex)
                value = abs(b-blue)  + abs(r-red)  + abs(g-green) 
                
                minColor[value] = [b, g, r]
                if value ==0: return [b, g, r]
                
            return minColor[ min(minColor.keys()) ]
        
        map = colorImage.copy()
        colorCode = HexColorCode().hexColorCodeList
        colorDict = {}
        for y, row in enumerate(colorImage):
            if y % 200 ==0: print("merge color process..:", y)
            for x, color in enumerate(row):
                if tuple(color) in colorDict.keys():
                    map[y][x] = colorDict[tuple(color) ]
                else:
                    hexColor = calcSimilarColor(color, colorCode)
                    map[y][x] = hexColor
                    colorDict[tuple(color) ] = hexColor
                
        return map
    
    def colorProcess(self, image, direction = "h"):
        self.similarColorMap = self.__createSimilarColorMap(image, direction = direction)
        self.paintingMap = self.__createPaintingMap(self.similarColorMap)
        return 
    
    def getColorDict(self, image):
        colorDict = {} # Key : Color Code / Values : Pixel Position
        for y, row in enumerate(image):
            for x, bgr in enumerate(row):
                bgr = tuple(bgr)
                if colorDict == {}: 
                    colorDict[ bgr ] = [ (y, x) ]
                    continue
                
                if bgr in self.colorDict.keys():
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
    
    painting.colorProcess(blurImage, direction = "h")
    similarMap = painting.similarColorMap
    paintingMap = painting.paintingMap
    
    colorDict = painting.getColorDict(paintingMap)
    '''
    pass
    
    
    
    
    







