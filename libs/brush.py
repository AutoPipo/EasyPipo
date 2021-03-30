
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
    def __init__ (self, filepath, db_path = "./databases/test.db"):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.__session_id = nowTime + str(random.randint(11 , 999999))
        
        self.imageSetting( filepath )
        self.dbSetting(db_path)
    
    def imageSetting(self, imagepath):
        self.filename = os.path.basename(imagepath)
        self.image = cv2.imread(imagepath)
        self.org_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
        directory="./web/static/org_image/"
        path = os.path.join(directory, self.filename)
        cv2.imwrite(path, self.image)
    
    def dbSetting(self, db_path):
        self.__db = dbControl(db_path)
        self.__db.createTable()

    def drawLine(self, edge, regions=[]):
        regions_ = []
        if regions == []:
            regions_ = [( 0, 0, self.org_image.shape[1], self.org_image.shape[0]), ]
            
        
        for idx, dict in enumerate(regions):
            
            x, y, radius = int(dict["x"]), int(dict["y"]), int(dict["radius"])
            x, y, w, h = x-radius, y-radius, radius*2, radius*2
            regions_.append([x, y, w, h])
            
            
        self.canvas = self.__addLine(edge, regions_)
        self.__db.insertData(self.__session_id, self.org_image, self.canvas)
        
        
        return
        
    def __addLine(self, threshold, regions):
        for region in regions:
            x, y, w, h = region
            self.canvas[y : y + h, x : x + w] = threshold[y : y + h, x : x + w]
        
        # self.showImage()
        return self.canvas
    
    def getEdge(self, line_detail = 8, block_size = 11):
        #          blur_size = 7,     , c = 5
        blur_size, c = self.__calcDetail(line_detail)
        print("line_detail",line_detail)
        print("blur:", blur_size, " c:", c)
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) 
        gray = self.__setBlur( gray, blur_size)
        edge = self.__makeThreshold(gray, block_size = block_size, c=c )
        self.canvas = np.zeros(edge.shape) + 255
        return edge
        
    def __calcDetail(self, value, max=20):
        value = max - int(value)
        # blur = int(10 - value * 0.1 )
        blur = 7
        # c = round( value * 0.6, 1) + (12 - blur)
        c = round(1 + value * 0.8, 1)
        if blur % 2 == 0: blur -= 1
        return blur, c
    
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
        
        image = cv2.resize(self.canvas, dsize=(width, height))
        cv2.imshow(title, image)
        cv2.waitKey(0)
        return

    def save(self, directory="./web/static/render_image/", name = ""):
        # if name == "": path = os.path.join(directory, self.filename)
        # else: path = os.path.join(directory, name+".jpg")
        path = os.path.join(directory, self.filename)
        cv2.imwrite(path, self.canvas)
        # self.__db.dbClose()
        return
    
    def undo(self):
        self.canvas = self.__db.undoCanvas(self.__session_id)
        self.save()
        return
        
    def finish(self):
        self.__db.dbClose()
        return
    
if __name__ == "__main__":
    dirpath = "./test-image/"
    filename = "a7"
    filepath = dirpath + filename + ".jpg"
    
    brush = Brush(filepath, "../databases/test.db")
    for value in range(0, 20, 3):
        edge = brush.getEdge( line_detail = value, block_size = 11)
        canvas = brush.drawLine(edge, regions=[])
        
        # brush.showImage(title="hello")
        brush.save("./result-image/", name = str(value))
    # brush.showImage("check detail")
    brush.finish()
    