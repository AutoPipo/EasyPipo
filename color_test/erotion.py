#

import numpy as np
import cv2

def hello():
    dirpath = "./render/"
    filename = "lala-liness"
    image = cv2.imread(dirpath+filename+".jpg", cv2.IMREAD_GRAYSCALE)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    # kernel = np.ones((3,3), np.uint8)
    
    
    dilation = cv2.dilate(image, kernel)
    
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    erosion = cv2.erode(dilation, kernel)
    
    cv2.imwrite(dirpath+filename+"-result.jpg", erosion)

hello()