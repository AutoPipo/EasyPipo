# new colortest
'''
21.07.02 여기서 테스트 진행

'''

import time, os
from painting import *
from drawLine import *
from imageProcessing import *
import cv2
from utils import *

def imageSave(image, directory = "./result-image/", name = "", id=""):
    path = os.path.join(directory, name+"-"+id)
    cv2.imwrite(path+".jpg", image)
    return
    


dir = "./test-image/"
file = "notebook"
base = ".jpg"
id = "1"


painting = Painting( dir+file+base )

print("========  blurImage =======")
blurImage = painting.blurring( div = 10, radius = 10, sigmaColor =20, medianValue=5)
imageSave(blurImage, name = file+"-blur", id=id)


print("========  Clustering =======")
start = time.time()
similarMap = painting.colorClustering( blurImage, cluster = 24 )
imageSave(similarMap, name = file+"-kmeans", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )

print("========= Expand Process ========")
start = time.time()
expandedImage = imageExpand(similarMap, guessSize = True) #, size=1)
imageSave(similarMap, name = file+"-expand", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )


print("========= expandImageColorMatch Process ========")
start = time.time()
# 확장된 이미지에서 변형된 색상을 군집화된 색상과 매칭
paintingMap = painting.allColorMatcing(expandedImage)
imageSave(paintingMap, name = file+"-expand-kmeans", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )




drawLine = DrawLine(paintingMap)

print("========  draw Line  =======")
start = time.time()
lineMap = drawLine.getDrawLine()

lined_image = drawLine.drawOutline(lineMap)
lined_image = lined_image.copy()
imageSave(lineMap, name = file+"-line", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )


# get Color(RGB) dictionary, Color index dictionary from Painted image 
colorNames, colors = getColorFromImage(paintingMap)
# Extracts Color label from Painted Image
img_lab, lab = getImgLabelFromImage(colors, paintingMap)

readimg = f'./result-image/{file+"-"+"line-"+id+base}'
print("read", readimg)
lined_image = cv2.imread(readimg)

# Extracts contours, hierarchy, thresh from Image drawn with lines
contours, hierarchy, thresh = getContoursFromImage(lined_image.copy())
# Make White image same size with Image drawn with lines
result_img = makeWhiteFromImage(lined_image.copy())
# Draw contouor borders and Color index on White image
result_img = setColorNumberFromContours(result_img, 
                                          thresh, 
                                          contours, 
                                          hierarchy, 
                                          img_lab, 
                                          lab, 
                                          colorNames)
# Draw Color label index on Result image
# result_img2 = setColorLabel(result_img, colorNames, colors)

print(">>", result_img.shape )
print(">>", paintingMap.shape )
imageSave(result_img, name = file+"-result", id=id)


line = cv2.imread( "./result-image/"+file+"-result-"+id+base )
paint = cv2.imread( "./result-image/"+file+"-expand-kmeans-"+id+base )


result_ = setBackgroundAlpha( paint.copy(), line.copy(), alpha = 0.12 )

imageSave(result_, name = file+"-alpha", id=id)

