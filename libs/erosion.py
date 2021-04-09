
import time, os
from painting import Painting
from drawLine import DrawLine, imageExpand
import cv2
import numpy as np

dir = "./result-image/"
file = "about-expand-c"
base = ".jpg"

filepath = dir+file+base 




img = cv2.imread(filepath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


ret, immmg = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
kernel = np.ones((3, 3), np.uint8)
immmg = cv2.erode(immmg, kernel, iterations=3)
kernel = np.ones((3, 3), np.uint8)
immmg = cv2.dilate(immmg, kernel, iterations=3)


# def eraser(img):
    


cv2.imwrite(dir+file+"-results.jpg", immmg)

'''

# 감산
img = cv2.imread(filepath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, img1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)


filepath = dir+"av-line-0-inv-results"+base 
img = cv2.imread(filepath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img2 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

# print( "+", np.count_nonzero(img1-img2== 0) )
mins = img1 - img2

for y, rows in enumerate(mins):
    for x, n in enumerate(rows):
        if n==1: mins[y][x] = 0
        
cv2.imwrite(dir+file+"-minus.jpg", mins)
'''





