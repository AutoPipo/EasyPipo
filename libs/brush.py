
"""
# brush
# Start : 2021.03.26
# Update : 
# Author : Minku Koo
# Line Detection from Image
"""

from sqlite_.sqlite_control import dbControl
import matplotlib.pyplot as plt
import cv2
import numpy as np
import random, datetime, os

class Brush:
    def __init__ (self, filepath, db_path = "../databases/test.db"):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.__session_id = nowTime + str(random.randint(11 , 999999))
        
        self.imageSetting( filepath)
        self.dbSetting(db_path)
    
    def imageSetting(self, filepath):
        self.filename = os.path.basename(filepath)
        self.image = cv2.imread(filepath)
        self.org_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
    
    def dbSetting(self, db_path):
        self.__db = dbControl(db_path)
        self.__db.createTable()

    def drawLine(self, edge, regions=[]):
        if regions == []:
            regions = [( 0,0,self.org_image.shape[1], self.org_image.shape[0]), ]
        self.__addLine(edge, regions)
        self.__db.insertData(self.__session_id, self.org_image, self.canvas)
        
    def __addLine(self, threshold, regions):
        print(self.canvas.shape)
        print(threshold.shape)
        for region in regions:
            x, y, w, h = region
            self.canvas[y : y + h, x : x + w] = threshold[y : y + h, x : x + w]
            
        return self.canvas

    def getEdge(self, blur_size = 7, block_size = 11, c = 5):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) 
        gray = self.__setBlur( gray, blur_size)
        edge = self.__makeThreshold(gray, block_size = block_size, c=c )
        self.canvas = np.zeros(edge.shape) + 255
        return edge
        
    def __setBlur(self, image, blur_size = 7):
        return cv2.medianBlur(image, blur_size)
        
    # make adaptive threshold 
    def __makeThreshold(self, image, block_size = 11, c = 5):
        edges = cv2.adaptiveThreshold(image, 
                                    255, 
                                    cv2.ADAPTIVE_THRESH_MEAN_C, 
                                    cv2.THRESH_BINARY, 
                                    block_size, 
                                    c
                                    )
        return edges

    def showImage(self, title = "Show Image", width = 1000, height = 700):
    
        image = cv2.resize(self.image, dsize=(width, height))
        cv2.imshow(title, image)
        cv2.waitKey(0)
        return

    def save(self, directory="../web/static/line-detect/"):
        path = os.path.join(directory, self.filename)
        cv2.imwrite(path, self.canvas)
    
    def undo(self):
        self.canvas = db.undoCanvas(self.__session_id)
        self.save()
        
    def finish(self):
        self.__db.dbClose()
    
if __name__ == "__main__":
    dirpath = "./test-image/"
    filename = "a3"
    filepath = dirpath + filename + ".jpg"
    
    brush = Brush(filepath, "../databases/test.db")
    edge = brush.getEdge( blur_size = 7, block_size = 11, c = 5)
    canvas = brush.drawLine(edge, regions=[])
    
    brush.showImage(title="hello")
    brush.save()
    
    
    
    