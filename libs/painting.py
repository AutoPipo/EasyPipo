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
# from libs.colorCode import HexColorCode
from colorCode import HexColorCode

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
        
        
        blurring = blurring // div * div #+ div // 2
        
        return blurring
    
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
    
    def __createSimilarColorMap(self, img, value, direction = "h"):
        
        # image = self.image.copy()
        image = img.copy()
        emap = np.zeros((image.shape[0], image.shape[1]))
        width, height = image.shape[1], image.shape[0]
        values = [value*1.0]
        
        def isSimilarColor(cell, other):
            if np.array_equal(cell, other): return False
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
    
    
    
    
    







