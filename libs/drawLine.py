'''
# Draw Line on Image

# Start : 21.04.01
# Update : 21.04.03
# Author : Minku Koo
'''
import cv2
import numpy as np

class DrawLine:
    def __init__(self, image):
        self.colorImage = image
        self.lineMap = np.array([]) #self.__drawLine(value = mergeValue)
    
    def getDrawLine(self, value = 1):
        return self.__drawLine(value = value)
    
    def __drawLine(self, value):
        #          여기서 이제 라인 빈공간 없애기
        self.lineMap = np.zeros(self.colorImage.shape) + 255
        # print("Expand Image Size:", self.linemap.shape)
        image_size_ = self.colorImage.shape[0]
        for y, row in enumerate(self.colorImage):
            line = []
            if y % 200 ==0: print("line draw process:", y,"/", image_size_ )
            
            for x, bgr in enumerate(row):
                colorChange = False
                blue, green, red = bgr
                for c in [-1, 1]:
                    try: 
                        b, g, r = self.colorImage[y+c, x]
                        if b-value< blue <b+value and \
                            g-value< green <g+value and \
                            r-value< red <r+value: pass
                        elif self.lineMap[y+c][x].tolist() == [0, 0, 0] : pass
                        else : 
                            self.lineMap[y, x ]=[0, 0, 0]
                            colorChange = True
                            break
                    except IndexError as e: pass
                    
                    try: 
                        
                        b, g, r = self.colorImage[y, x+c]
                            
                        if b-value< blue <b+value and \
                            g-value< green <g+value and \
                            r-value< red <r+value: pass
                        elif self.lineMap[y][x+c].tolist() == [0, 0, 0] : pass
                        else : 
                            self.lineMap[y, x ]=[0, 0, 0]
                            colorChange = True
                            break
                    except IndexError as e: pass
                if not colorChange:
                    self.lineMap[y, x ]=[255, 255, 255]
                    
        return self.lineMap
        
    def __lineOnImage(self):
        new_map = np.zeros(self.colorImage.shape) + 255
        for y, row in enumerate(self.colorImage):
            if y % 300 == 0: print("line+color processing...", y, "/", self.colorImage.shape[0])
            for x, bgr in enumerate(row):
                if self.lineMap[y][x].tolist() == [0, 0, 0]: new_map[y][x] = [0, 0, 0]
                else: new_map[y][x] = bgr.tolist()
                
        return new_map
        
    def getLineOnImage(self):
        return self.__lineOnImage()
        
def imageExpand(image, guessSize=False ,size = 3):
    if guessSize : size = ( 5000 // image.shape[1] ) +1
    return  cv2.resize(image, None, fx=size, fy=size, interpolation=cv2.INTER_CUBIC)
    
    
    
if __name__ == "__main__":
    '''
    * How to Use?
    
    drawLine = DrawLine(image, maergeValue = 3)
    lineMap = drawLine.lineMap
    lineOnImage = drawLine.getLineOnImage()
    
    expandImage = drawLine.imageExpand(lineMap, size = 4)
    expandImage = drawLine.imageExpand(lineMap, guessSize = True)
    '''
    pass