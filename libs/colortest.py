# test


import time, os
from painting import Painting
from drawLine import DrawLine
import cv2

def imageSave(image, directory = "./result-image/", name = "", id=""):
    path = os.path.join(directory, name+"-"+id)
    print(path)
    cv2.imwrite(path+".jpg", image)
    return
    
start = time.time()

dir = "./test-image/"
file = "her1"
base = ".jpg"
id = "nosiminal"

painting = Painting( dir+file+base )
blurImage = painting.blurring(div = 32, radius = 10, sigmaColor = 30, medianValue=3)
imageSave(blurImage, name = file+"-blur", id=id)


# similarMap = painting.getSimilarColorMap(blurImage, value = 15, direction = "h" )
# imageSave(similarMap, name = file+"-similar", id=id)
# paintingMap = painting.getPaintingColorMap(similarMap)

paintingMap = painting.getPaintingColorMap(blurImage)
imageSave(paintingMap, name = file+"-painting", id=id)


colorDict = painting.getColorDict(paintingMap)
print("=="*20)
print("COLOR NUMBER : ", len(colorDict))
print("=="*20)

drawLine = DrawLine(paintingMap, mergeValue = 1)
lineMap = drawLine.lineMap
# lineOnImage = drawLine.getLineOnImage()
expandImage = drawLine.imageExpand(lineMap, guessSize = True)

imageSave(expandImage, name = file+"-expand", id=id)

print("time :", round((time.time() - start)/60, 3) ,"분 정도.." )


