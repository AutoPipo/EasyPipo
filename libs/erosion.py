
import time, os
from painting import Painting
from drawLine import DrawLine, imageExpand
import cv2
import numpy as np

dir = "./result-image/"
file = "av-line-0-inv"
base = ".jpg"

filepath = dir+file+base 

img = cv2.imread(filepath)

'''
ret, lineimage = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
kernel = np.ones((2, 2), np.uint8)
erosion = cv2.erode(lineimage, kernel, iterations=2)
dilate = cv2.dilate(erosion, kernel, iterations=2)
erosion = cv2.erode(dilate, kernel, iterations=2)

cv2.imwrite(dir+file+"-results.jpg", erosion)

'''
import collections
# 감산
img = cv2.imread(filepath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img.shape)
ret, img1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
print(img1.shape)


filepath = dir+"av-line-0-inv-results"+base 
img = cv2.imread(filepath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img2 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

# print( "+", np.count_nonzero(img1-img2== 0) )
mins = img1 - img2
print( "+", np.count_nonzero(mins== 0) + np.count_nonzero(mins== 255)  )
print(  collections.Counter(mins[0])[255] )

for y, rows in enumerate(mins):
    for x, n in enumerate(rows):
        if n==1: mins[y][x] = 0


cv2.imwrite(dir+file+"-minus.jpg", mins)



