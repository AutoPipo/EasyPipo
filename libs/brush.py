
"""
# brush
# Start : 2021.03.26
# Update : 
# Author : Minku Koo
# Line Detection from Image
"""
#libs
from libs.sqlite_.sqlite_control import dbControl
import matplotlib.pyplot as plt
import cv2
import numpy as np
import random, datetime, os

class Brush:
    def __init__ (self, filepath, job_id, db_path = "./databases/test.db"):
        self.__job_id = job_id
        
        self.__db = self.dbSetting(db_path)
        self.isNewJob = self.__db.checkJobID(self.__job_id)
        self.imageSetting( filepath )
        self.max_width = 800
        
    def imageSetting(self, imagepath):
        self.filename = os.path.basename(imagepath)
        self.image = cv2.imread(imagepath)
        self.org_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
        if not self.isNewJob:
            directory="./web/static/org_image/"
            path = os.path.join(directory, self.filename)
            cv2.imwrite(path, self.image)
    
    def dbSetting(self, db_path):
        db = dbControl(db_path)
        db.createTable()
        return db

    def drawLine(self, edge, regions=[]):
        regions_ = []
        if regions == []:
            regions_ = [( 0, 0, self.org_image.shape[1], self.org_image.shape[0]), ]
            
        for dict in regions:
            
            x, y, radius = int(dict["x"]), int(dict["y"]), int(dict["radius"])
            
            x, y, w, h = x-radius, y-radius, radius*2, radius*2
            regions_.append( (x, y, w, h) )
            
        self.__addLine(edge, regions_)
        self.__db.insertData(self.__job_id, self.org_image, self.canvas)
        
        
        return
        
    def __addLine(self, threshold, regions):
        for region in regions:
            x, y, w, h = region
            self.canvas[y : y + h, x : x + w] = threshold[y : y + h, x : x + w]
        
        return self.canvas
    
    def getEdge(
            self, 
            line_detail = 8, 
            threshold_value= 80
            ):
        #          blur_size = 7,     , c = 5
        canny_value1, canny_value2 = self.__calcDetail(line_detail)
        print("line_detail",line_detail)
        print("canny:", canny_value1, canny_value2 )
        # canny_value1, canny_value2 = 70, 100
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) 
        
        '''
        gray_h, gray_w = gray.shape
        max_width = self.max_width
        max_height = int(max_width*(gray_h/gray_w))
        gray = cv2.resize(gray, (max_width, max_height))
        '''
        gray_h, gray_w = gray.shape
        blurSize = 3 + (gray_w // 1000)
        if blurSize % 2 == 0: blurSize += 1
        print("blurSize",blurSize)
        # gray = self.__setBlur( gray, blur_size)
        # edge = self.__makeThreshold(gray, block_size = block_size, c=c )
        
        # blur = cv2.GaussianBlur(self.image, (5, 5), 0)
        blur = self.__setBlur( gray, blur_size = blurSize)
        canny = cv2.Canny(
                    blur, 
                    canny_value1, 
                    canny_value2
                    ) #  --> 비교
                    
        edge = self.__makeThreshold( canny, threshold_value )
        
        if not self.isNewJob:
            self.canvas = np.zeros(edge.shape) + 255
        else:
            self.canvas = self.__db.getCanvas(self.__job_id)
        # cv2.imshow("eg", edge)
        # cv2.waitKey(0)
        return edge
        
    def __calcDetail(self, value, max=20):
        value = int(value)
        canny1 = 50 - value
        canny2 = 5 + canny1 + (max - value) * 4
        # blur = int(10 - value * 0.1 )
        # blur = 5
        # c = round( value * 0.6, 1) + (12 - blur)
        # c = round(1 + value * 0.8, 1)
        # if blur % 2 == 0: blur -= 1
        return canny1, canny2
    
    def __setBlur(self, image, blur_size = 5):
        return cv2.GaussianBlur(image, (blur_size, blur_size), 0)
        # return cv2.medianBlur(image, blur_size)
        
    # make adaptive threshold 
    def __makeThreshold(self, image, threshold_ = 70):
        
        ret, edges = cv2.threshold(
                    image, 
                    threshold_, 
                    255, 
                    cv2.THRESH_BINARY_INV
                    )
        # edges = cv2.adaptiveThreshold(
            # image, 
            # 255, 
            # cv2.ADAPTIVE_THRESH_MEAN_C, 
            # cv2.THRESH_BINARY, 
            # block_size, 
            # c
        # )
        return edges

    def showImage(self, title = "Show Image", width = 1000, height = 700):
        
        image = cv2.resize(self.canvas, dsize=(width, height))
        cv2.imshow(title, image)
        cv2.waitKey(0)
        return

    def save(self, directory="./web/static/render_image/", name = ""):
        if name == "": path = os.path.join(directory, self.filename)
        else: path = os.path.join(directory, name+".jpg")
        # path = os.path.join(directory, self.filename)
        
        cv2.imwrite(path, self.canvas)
        
        # self.__db.dbClose()
        return
    
    def undo(self):
        self.canvas = self.__db.undoCanvas(self.__job_id)
        self.save()
        return
        
    def finish(self):
        self.__db.dbClose()
        return
    
if __name__ == "__main__":
    dirpath = "./test-image/"
    filename = "a5"
    filepath = dirpath + filename + ".jpg"
    
    brush = Brush(filepath, "123123123",db_path = "../databases/test.db")
    for value in range(50, 190, 30):
        edge = brush.getEdge(line_detail = 8, threshold_value=value)
        canvas = brush.drawLine(edge, regions=[])
        
        # brush.showImage(title="hello")
        brush.save("./result-image/", name = "canny1-"+str(value))
    # brush.showImage("check detail")
    brush.finish()
    