'''
# Draw Line on Image

# Start : 21.04.01
# Update : 21.04.10
# Author : Minku Koo
'''
import cv2
import numpy as np

class DrawLine:
    def __init__(self, image):
        self.colorImage = image
        self.lineMap = np.array([]) 
    
    def getDrawLine(self):
        return self.__drawLine()
    
    def __drawLines(self):
        self.lineMap = np.zeros(self.colorImage.shape) + 255
        
        for y, row in enumerate(self.colorImage[1:-1]):
            for x, bgr in enumerate(row[1:-1]):
                for c in [-1, 1]:
                    cellColor = self.colorImage[y+c, x]
                    # if np.array_equal(bgr, cellColor): pass
                    
                    if not np.array_equal(bgr, cellColor) and \
                     not np.sum(self.lineMap[y+c][x]) == 0:
                        self.lineMap[y, x ] = np.array([0, 0, 0])
                        break
                        
                    # elif np.sum(self.lineMap[y+c][x]) == 0 : pass
                    # else : 
                        # self.lineMap[y, x ] = np.array([0, 0, 0])
                        # break
                        
                    cellColor = self.colorImage[y, x+c]
                    if not np.array_equal(bgr, cellColor) and \
                     not np.sum(self.lineMap[y+c][x]) == 0:
                        self.lineMap[y, x ] = np.array([0, 0, 0])
                        break
                    
                    # if np.array_equal(bgr, cellColor): pass
                    # elif np.sum(self.lineMap[y][x+c]) == 0 : pass
                    # else : 
                        # self.lineMap[y, x ] = np.array([0, 0, 0])
                        # break
                    
        return self.lineMap
    
    def __drawLine(self):
        self.lineMap = np.zeros(self.colorImage.shape) + 255
        
        false_cell = np.array([False, False, False])
        for y, orgRow in enumerate(self.colorImage[:-1]):
            nextRow = self.colorImage[y+1]
            compareRow = np.array( np.where((orgRow == nextRow) == False))
            number = 1
            for x in np.unique(compareRow[0]):
                # if np.count_nonzero(compareRow[0]==x) ==3:
                
                # if number % 2 == 0:
                    # self.lineMap[y][x-1] = np.array([0, 0, 0])
                # else:
                    # self.lineMap[y][x] = np.array([0, 0, 0])
                # number += 1
                
                # if not np.sum(self.lineMap[y][x-1]) ==0:
                self.lineMap[y][x] = np.array([0, 0, 0])
                            
        width = self.lineMap.shape[1]
        for x in range(width-1):
            compareCol = np.array( np.where((self.colorImage[:,x] == self.colorImage[:,x+1]) == False))
            for y in np.unique(compareCol[0]):
                # if not np.sum(self.lineMap[y-1][x]) ==0:
                self.lineMap[y][x] = np.array([0, 0, 0])
                    
        return self.lineMap
    
    
    def __lineOnImage(self):
        new_map = np.zeros(self.colorImage.shape) + 255
        for y, row in enumerate(self.colorImage):
            if y % 300 == 0: print("line+color processing...", y, "/", self.colorImage.shape[0])
            for x, bgr in enumerate(row):
                if np.sum( self.lineMap[y][x] ) == 0: new_map[y][x] = np.array([0, 0, 0])
                else: new_map[y][x] = bgr
                
        return new_map
        
    def getLineOnImage(self):
        return self.__lineOnImage()
        
def imageExpand(image, guessSize=False ,size = 3):
    if guessSize : size = ( 5000 // image.shape[1] ) +1
    return  cv2.resize(image, None, fx=size, fy=size, interpolation=cv2.INTER_LINEAR)
    
    
    
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
    '''
    pass