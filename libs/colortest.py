# test


import time, os
from painting import Painting
from drawLine import DrawLine

def imageSave(self, image, directory = "./result-image/", name = "", id=""):
    path = os.path.join(directory, name+"-"+id)
    
    cv2.imwrite(path, image+".jpg")
    return
    
start = time.time()

dir = "./test-image/"
file = "iron"
base = ".png"
id = "1"

painting = Painting( dir+file+base )
blurImage = painting.blurring(radius = 20, sigmaColor = 40, medianValue=5)
imageSave(blurImage, name = file+"blur", id=id)

painting.colorProcess(blurImage, direction = "h")
similarMap = painting.similarColorMap
paintingMap = painting.paintingMap
imageSave(paintingMap, name = file+"painting", id=id)

# colorDict = painting.getColorDict(paintingMap)

drawLine = DrawLine(paintingMap, maergeValue = 1)
lineMap = drawLine.lineMap
# lineOnImage = drawLine.getLineOnImage()
expandImage = drawLine.imageExpand(lineMap, guessSize = True)

imageSave(expandImage, name = file+"expand", id=id)







print("time :", round((time.time() - start)/60, 3) ,"분 정도.." )

