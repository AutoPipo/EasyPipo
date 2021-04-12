# test


import time, os
from painting import Painting
from drawLine import DrawLine, imageExpand, leaveOnePixel
import cv2

def imageSave(image, directory = "./result-image/", name = "", id=""):
    path = os.path.join(directory, name+"-"+id)
    print(path)
    cv2.imwrite(path+".jpg", image)
    return
    
# import time
# start = time.time()
# print("비교 시간 :", round((time.time() - start), 3) ,"초.." )

dir = "./test-image/"
file = "lala"
base = ".jpg"
id = "a"

start = time.time()

painting = Painting( dir+file+base )
'''
# org
blurImage = painting.blurring(div = 32, radius = 10, sigmaColor = 30, medianValue=5)
imageSave(blurImage, name = file+"-blur", id=id)

similarMap = painting.getSimilarColorMap(blurImage, value = 10, direction = "h" )
imageSave(similarMap, name = file+"-similar", id=id)
'''

# test
similarMap = painting.getSimilarColorMap( value = 20, direction = "h" )
imageSave(similarMap, name = file+"-similar", id=id)
print("========  Similar Map End  =======")
print("time :", round((time.time() - start), 3) ,"초 정도.." )
start = time.time()
blurImage = painting.blurring(similarMap, div = 20, radius = 20, sigmaColor = 40, medianValue=7)
imageSave(blurImage, name = file+"-blur", id=id)
print("========  Blur Map End  =======")
print("time :", round((time.time() - start), 3) ,"초 정도.." )
# test finish
start = time.time()

print("========  Merge Color Map End  =======")
paintingMap = painting.getPaintingColorMap(blurImage)
# paintingMap = painting.getPaintingColorMap(blurImage)
print("time :", round((time.time() - start), 3) ,"초 정도.." )

imageSave(paintingMap, name = file+"-painting", id=id)


# colorDict = painting.getColorDict(paintingMap)
print("=="*20)
# print("COLOR NUMBER : ", len(colorDict))
print("=="*20)

drawLine = DrawLine(paintingMap)

start = time.time()
print("========  draw Line End  =======")
lineMap = drawLine.getDrawLine()
imageSave(lineMap, name = file+"-line", id=id)

print("time :", round((time.time() - start), 3) ,"초 정도.." )

print("========= Expand Process ========")
start = time.time()
expandImage = imageExpand(lineMap, guessSize = True)
imageSave(expandImage, name = file+"-expand", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )

skImage = leaveOnePixel(expandImage)
imageSave(skImage, name = file+"-skeleton", id=id)

lineImage = drawLine.getLineOnImage()
imageSave(lineImage, name = file+"-line+image", id=id)






