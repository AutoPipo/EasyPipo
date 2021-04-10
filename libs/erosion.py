from skimage.morphology import skeletonize
from skimage import data
import matplotlib.pyplot as plt
from skimage.util import invert

import time, os
from painting import Painting
from drawLine import DrawLine, imageExpand
import cv2
import numpy as np

dir = "./result-image/"
file = "tli-expand-qb"
base = ".jpg"

filepath = dir+file+base 



'''
img = cv2.imread(filepath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


ret, immmg = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
kernel = np.ones((3, 3), np.uint8)
immmg = cv2.erode(immmg, kernel, iterations=2)
immmg = cv2.dilate(immmg, kernel, iterations=2)

kernel = np.ones((2, 2), np.uint8)
immmg = cv2.erode(immmg, kernel, iterations=2)
immmg = cv2.dilate(immmg, kernel, iterations=2)

# def eraser(img):
   

cv2.imwrite(dir+file+"-results.jpg", immmg)
'''
# -------

# Invert the horse image
# image = invert(data.horse())

# perform skeletonization
imge = cv2.imread(filepath)
imge = cv2.cvtColor(imge, cv2.COLOR_BGR2GRAY)


ret, imge = cv2.threshold(imge, 200, 1, cv2.THRESH_BINARY_INV)
skeleton = skeletonize(imge)

# display results
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),
                         sharex=True, sharey=True)

ax = axes.ravel()

ax[0].imshow(imge, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)

ax[1].imshow(skeleton, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('skeleton', fontsize=20)

fig.tight_layout()
plt.show()

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





