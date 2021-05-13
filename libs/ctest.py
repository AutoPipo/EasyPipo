# new colortest


import time, os
from painting import *
from drawLine import *
import cv2

def imageSave(image, directory = "./result-image/", name = "", id=""):
    path = os.path.join(directory, name+"-"+id)
    print(path)
    cv2.imwrite(path+".jpg", image)
    return
    


dir = "./test-image/"
file = "a5"
base = ".jpg"
id = "colorcount32"


painting = Painting( dir+file+base )

print("========  blurImage =======")
blurImage = painting.blurring( div = 8, radius = 10, sigmaColor =20, medianValue=5)
imageSave(blurImage, name = file+"-blur", id=id)


print("========  Clustering =======")
start = time.time()
similarMap = painting.colorClustering( similarMap, cluster = 32 )
imageSave(similarMap, name = file+"-kmeans", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )

print("========= Expand Process ========")
start = time.time()
similarMap = imageExpand(blurImage, guessSize = False, size=1)
imageSave(similarMap, name = file+"-expand", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )

print("------ color count after expand -----")
color_count = painting.getNumberOfColor(paintingMap)
print(color_count, "개")

'''
여기에 확장한 이미지 색상 매칭 시켜야함

'''
















