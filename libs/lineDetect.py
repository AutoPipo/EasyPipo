"""
2021.03.26
"""
# __init__.py
from sqlite_.sqlite_control import *
import matplotlib.pyplot as plt
import cv2
import numpy as np
import sqlite3 as sqlite


def showImage(image, title = "Show Image", width = 1000, height = 700):
    
    image = cv2.resize(image, dsize=(width, height))
    cv2.imshow(title, image)
    cv2.waitKey(0)
    return

# make adaptive threshold 
def makeThreshold(image, block_size = 11, c = 5):
    edges = cv2.adaptiveThreshold(image, 
                                255, 
                                cv2.ADAPTIVE_THRESH_MEAN_C, 
                                cv2.THRESH_BINARY, 
                                block_size, 
                                c
                                )
    return edges

def createCanvas(threshold):
    canvas = np.zeros(threshold.shape) + 255
    return canvas

def setBlur(image, blur_size = 7):
    return cv2.medianBlur(image, blur_size)

def readImage(filepath):
    return cv2.imread(filepath)


def getEdge(image, blur_size = 7, block_size = 11, c = 5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    gray = setBlur( gray, blur_size)
    edge =  makeThreshold(gray, block_size = block_size, c=c )
    return edge

def addLine(threshold, canvas, regions):
    '''
    region_mask = np.zeros(threshold.shape)
    #showImage(region_mask, "erase")
    for region in regions:
        x, y, w, h = region
        region_mask[y : y + h, x : x + w] = 1
        
    threshold = np.multiply(threshold, region_mask)
    '''
    # 흑백 반전용
    # threshold += 255
    # threshold[threshold == 510] = 0
    
    for region in regions:
        x, y, w, h = region
        canvas[y : y + h, x : x + w] = threshold[y : y + h, x : x + w]
        
    
    
    return canvas

def makePipo(org_threshold, threshold):
    return org_threshold + threshold


if __name__ == "__main__":
    import random, datetime
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    sessions = nowTime + str(random.randint(11 , 999999))
    print("session:",sessions)
    dirpath = "./test-image/"
    filename = "a1"
    filepath = dirpath + filename + ".jpg"
    # x, y, w, h
    regions = [[1512,1512,230,140], [1212,912,100,100]]
    regionss = [[2212,1612,130,160], [212,1612,30,100]]
    
    
    image = readImage(filepath) 
    org_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    '''
    # 흑백 처리 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    showImage(gray, "rgb to gray")
    
    # 블러 처리
    gray = setBlur( gray, 7)
    showImage(gray, "median blur")
    '''
    conn = get_db_query("../databases/test.db")
    createTable(conn)
    
    # edge
    edge = getEdge(image, blur_size = 7, block_size = 11, c = 5)
    showImage(edge, "edge")
    
    canvas = createCanvas(edge)
    insertData(conn, sessions, org_image, canvas)
    
    #showImage(edge, "edges")
    # pipo = np.zeros(edge.shape)
    print("session:",sessions)
    # 영역 선택 / 이외 부분 제거
    canvas = addLine(edge, canvas, regions)
    #showImage(addThreshold, "erase1")
    updateCanvas(conn, sessions, canvas)
    # canvas = makePipo(canvas, addThreshold)
    showImage(canvas, "pipo1")
    
    
    
    print("session:",sessions)
    canvas = addLine(edge, canvas, regionss)
    #showImage(addThreshold, "erase2")
    updateCanvas(conn, sessions, canvas)
    # canvas = makePipo(canvas, addThreshold)
    showImage(canvas, "pipo2")
    print("session:",sessions)
    a = getCanvas(conn, sessions, index = -1)
    # print(a)
    print( type(a)   )
    showImage(a, "dbdb")
    
    conn.close()
    # test
    

