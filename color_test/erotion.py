#

import numpy as np
import cv2

def erode():
    dirpath = "./render/"
    filename = "iron-line-1"
    image = cv2.imread(dirpath+filename+".jpg", cv2.IMREAD_GRAYSCALE)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    render = cv2.dilate(image, kernel, iterations=1)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    render = cv2.erode(render, kernel)
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    render = cv2.dilate(render, kernel)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    render = cv2.erode(render, kernel, iterations=1)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    render = cv2.dilate(render, kernel, iterations=2)
    '''
    
    cv2.imwrite(dirpath+filename+"-opening.jpg", render)
    
def hello():
    pass

erode()