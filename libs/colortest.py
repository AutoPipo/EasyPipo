# test


import time, os
from painting import Painting
from drawLine import DrawLine, imageExpand
import cv2

def imageSave(image, directory = "./result-image/", name = "", id=""):
    path = os.path.join(directory, name+"-"+id)
    print(path)
    cv2.imwrite(path+".jpg", image)
    return
    
start = time.time()

dir = "./test-image/"
file = "lala"
base = ".jpg"
id = "0"

painting = Painting( dir+file+base )
'''
# org
blurImage = painting.blurring(div = 32, radius = 10, sigmaColor = 30, medianValue=5)
imageSave(blurImage, name = file+"-blur", id=id)

similarMap = painting.getSimilarColorMap(blurImage, value = 10, direction = "h" )
imageSave(similarMap, name = file+"-similar", id=id)
'''

# test
similarMap = painting.getSimilarColorMap( value = 12, direction = "h" )
imageSave(similarMap, name = file+"-similar", id=id)
print("========  Similar Map End  =======")
blurImage = painting.blurring(similarMap, div = 50, radius = 10, sigmaColor = 30, medianValue=7)
imageSave(blurImage, name = file+"-blur", id=id)
print("========  Blur Map End  =======")
# test finish

paintingMap = painting.getPaintingColorMap(blurImage)
# paintingMap = painting.getPaintingColorMap(blurImage)

imageSave(paintingMap, name = file+"-painting", id=id)


# colorDict = painting.getColorDict(paintingMap)
print("=="*20)
# print("COLOR NUMBER : ", len(colorDict))
print("=="*20)

drawLine = DrawLine(paintingMap)
lineMap = drawLine.getDrawLine(value = 1)
imageSave(lineMap, name = file+"-line", id=id)

expandImage = imageExpand(lineMap, guessSize = True)
imageSave(expandImage, name = file+"-expand", id=id)

print("========= Expand Process ========")


print("time :", round((time.time() - start)/60, 3) ,"분 정도.." )


