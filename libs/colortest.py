# test
'''
21.07.02 >> ctest로 변경

'''



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
file = "dog"
base = ".jpg"
id = "2"



painting = Painting( dir+file+base )
'''
# org
blurImage = painting.blurring(div = 32, radius = 10, sigmaColor = 30, medianValue=5)
imageSave(blurImage, name = file+"-blur", id=id)

similarMap = painting.getSimilarColorMap(blurImage, value = 10, direction = "h" )
imageSave(similarMap, name = file+"-similar", id=id)
'''

# test
print("========  blurImage =======")
blurImage = painting.blurring( div = 8, radius = 10, sigmaColor =20, medianValue=5)
imageSave(blurImage, name = file+"-blur", id=id)


'''
# 이게 원래 로트
start = time.time()
similarMap = painting.getSimilarColorMap( blurImage, value = 19, direction = "h" )
imageSave(similarMap, name = file+"-similar", id=id)
print("========  Similar Map End  =======")
print("time :", round((time.time() - start), 3) ,"초 정도.." )
'''

# time.sleep(5)

# start = time.time()
# similarMap = painting.getSimilarColorMap( value = 10, direction = "h" )
# imageSave(blurImage, name = file+"-blur", id=id)
# print("========  Blur Map End  =======")
# print("time :", round((time.time() - start), 3) ,"초 정도.." )
# test finish


# print("========  Painting Color Map  =======")
# start = time.time()
# paintingMap = painting.getPaintingColorMap(blurImage) # similarMap
# imageSave(paintingMap, name = file+"-painting", id=id)
# print("time :", round((time.time() - start), 3) ,"초 정도.." )


print("========= Expand Process ========")
start = time.time()
similarMap = imageExpand(blurImage, guessSize = False, size=1)
imageSave(similarMap, name = file+"-expand", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )



# 바뀐 위치
print("========  Similar Map =======")
start = time.time()
similarMap = painting.colorClustering( similarMap, cluster = 24 )
imageSave(similarMap, name = file+"-kmeans", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )

# print("------ color count after cluster -----")
# color_count = painting.getNumberOfColor(similarMap)
# print(color_count, "개")


print("type of similar", type(similarMap))
# print(similarMap)
print("========  Painting Color Map  =======")
start = time.time()
paintingMap = painting.getPaintingColorMap(similarMap)
imageSave(paintingMap, name = file+"-paintings", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )

'''

'''
# colorDict = painting.getColorDict(paintingMap)
# print("=="*20)
# print("COLOR NUMBER : ", len(colorDict))


# print("------ color count -----")
# color_count = painting.getNumberOfColor(paintingMap)
# print(color_count, "개")



drawLine = DrawLine(paintingMap)


print("========  draw Line  =======")
start = time.time()
lineMap = drawLine.getDrawLine()
imageSave(lineMap, name = file+"-line", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )



# print("========= skeleton ========")
# skImage = leaveOnePixel(lineMap)
# imageSave(skImage, name = file+"-skeleton", id=id)

# lineImage = drawLine.getLineOnImage()
# imageSave(lineImage, name = file+"-line+image", id=id)



