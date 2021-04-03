# test


import time, os
from painting import Painting
from drawLine import DrawLine
import cv2

def imageSave(image, directory = "./result-image/", name = "", id=""):
    path = os.path.join(directory, name+"-"+id)
    # print(path)
    cv2.imwrite(path+".jpg", image)
    return
    
start = time.time()

dir = "./test-image/"
file = "iron"
base = ".png"
id = "1"

painting = Painting( dir+file+base )
blurImage = painting.blurring(div = 32, radius = 20, sigmaColor = 30, medianValue=7)
imageSave(blurImage, name = file+"-blur", id=id)

# painting.colorProcess(blurImage, direction = "h")
similarMap = painting.getSimilarColorMap(blurImage, value = 15, direction = "h" )
imageSave(similarMap, name = file+"-similar", id=id)

paintingMap = painting.getPaintingColorMap(similarMap)
imageSave(paintingMap, name = file+"-painting", id=id)


# colorDict = painting.getColorDict(paintingMap)

drawLine = DrawLine(paintingMap, mergeValue = 1)
lineMap = drawLine.lineMap
# lineOnImage = drawLine.getLineOnImage()
expandImage = drawLine.imageExpand(lineMap, guessSize = True)

imageSave(expandImage, name = file+"-expand", id=id)

print("time :", round((time.time() - start)/60, 3) ,"분 정도.." )





print("time :", round((time.time() - start)/60, 3) ,"분 정도.." )

