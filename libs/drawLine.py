'''
# Draw Line on Image

# Start : 21.04.01
# Update : 21.04.16
# Author : Minku Koo
'''
import cv2
import numpy as np

from skimage.morphology import skeletonize
from skimage import data
import matplotlib.pyplot as plt
from skimage.util import invert

class DrawLine:
    def __init__(self, image):
        self.colorImage = image
        self.lineMap = np.zeros(image.shape) + 255
    
    def getDrawLine(self):
        return self.__drawLine()
    
    def getLineOnImage(self):
        return self.__lineOnImage()
    
    
    def __drawLine(self):
        
        for y, orgRow in enumerate(self.colorImage[:-1]):
            nextRow = self.colorImage[y+1]
            compareRow = np.array( np.where((orgRow == nextRow) == False))
            for x in np.unique(compareRow[0]):
                self.lineMap[y][x] = np.array([0, 0, 0])
                            
        width = self.lineMap.shape[1]
        for x in range(width-1):
            compareCol = np.array( np.where((self.colorImage[:,x] == self.colorImage[:,x+1]) == False))
            for y in np.unique(compareCol[0]):
                self.lineMap[y][x] = np.array([0, 0, 0])
        
        return self.lineMap
    
    
    def __lineOnImage(self):
        new_map = self.colorImage.copy()
        lineMap = self.lineMap // 255
        return np.multiply(new_map, lineMap) 
        
    
        
def imageExpand(image, guessSize=False ,size = 3):
    if guessSize : size = ( 5000 // image.shape[1] ) +1
    #       INTER_LANCZOS4
    image = cv2.resize(image, None, fx=size, fy=size, interpolation=cv2.INTER_LINEAR)
    # _, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
    return  image
    

def leaveOnePixel(lineImage):
    image = lineImage.copy()
    
    _, image = cv2.threshold(image, 200, 1, cv2.THRESH_BINARY_INV)
    skeleton = skeletonize(image)
    # skeleton_lee = skeletonize(blobs, method='lee')
    skeleton = cv2.cvtColor(skeleton, cv2.COLOR_BGR2GRAY)
    
    canvas = np.zeros(skeleton.shape) + 1
    
    return 255 - np.multiply( canvas, skeleton )
    
if __name__ == "__main__":
    '''
    * How to Use?
    
    drawLine = DrawLine(image)
    lineMap = drawLine.getDrawLine()
    lineOnImage = drawLine.getLineOnImage()
    
    # Way 1 )
    expandImage = drawLine.imageExpand(lineMap, size = 4)
    # Way 2 )
    expandImage = drawLine.imageExpand(lineMap, guessSize = True)
    
    onePixelMap = leaveOnePixel(expandImage)
    
    '''
    pass
    