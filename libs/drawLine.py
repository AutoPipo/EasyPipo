'''
# Draw Line on Image

# Start : 21.04.01
# Update : 21.05.11
# Author : Minku Koo
'''

import cv2
import numpy as np
from skimage.morphology import skeletonize

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
                
        _, self.lineMap = cv2.threshold(self.lineMap, 199, 255, cv2.THRESH_BINARY)
        
        return self.lineMap
    
    
    def __lineOnImage(self):
        new_map = self.colorImage.copy()
        lineMap = self.lineMap // 255
        return np.multiply(new_map, lineMap) 
    
    def drawOutline(self, image):
        # image[0], image[-1], image[:,0], image[:,-1] = 0, 0, 0, 0
        image[0:2], image[-3:-1], image[:,0:2], image[:,-3:-1] = 0, 0, 0, 0
        return image
    

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
    outlines = drawLine.drawOutline(lineMap)
    lineOnImage = drawLine.getLineOnImage()
    
    onePixelMap = leaveOnePixel(expandImage)
    
    
    '''
    pass
    