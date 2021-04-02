#210401
#minku koo

import matplotlib.pyplot as plt
import cv2
import numpy as np
import random, datetime, os
from colorCode import HexColorCode

'''
# -- 메모 --
# opencv에서 imread는 기본 BGR
'''

class Color:
    def __init__ (self, filepath, job_id = "job123"):
        self.__job_id = job_id
        self.colorDict = {}
        self.colorMap = np.array([])
        self.lineDetected = np.array([])
        
        self.width, self.height = 800, 500
        
        self.__imageSetting( filepath )
        
    def __imageSetting(self, imagepath):
        self.filename = os.path.basename(imagepath)
        self.image = cv2.imread(imagepath) #, cv2.IMREAD_GRAYSCALE
        # self.rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
        # a = [30, 56, 87]
        # hexColor = self.__bgr2hex(a)
        # print(hexColor)
        return
    
    def colorProcess(self, image, direction = "h"):
        def imageMerge(image, map):
            new_map = np.zeros(image.shape) + 255
            for y, row in enumerate(image):
                if y % 300 == 0: print("processing...", y, "/", image.shape[0])
                for x, bgr in enumerate(row):
                    # b, g, r = 
                    if map[y][x].tolist() == [0, 0, 0]:
                        new_map[y][x] = [0, 0, 0]
                    else:
                        new_map[y][x] = bgr.tolist()
                    
            return new_map
            
        print("color process start")
        print(" ======= File Name ======")
        print("file:", self.filename)
        render_file_name = self.filename.split(".")[0]
        # dict = self.__createColorDict(image) # make  self.colorDict
        # print("--------- dict count:", len(dict.keys()))
        images = image.copy()
        # 원래 이거
        self.colorMap = self.__createColorMap(image, direction = "h")
        # 이건 라인 검출 테스트용 
        # self.colorMap = cv2.imread("./render/"+render_file_name+"-merge7.jpg")
        
        
        print(" ======= Convert Image Size ======")
        print("size:",self.colorMap.shape )
        self.imageSave(self.colorMap, name=render_file_name+"-change"  )
        
        
        mergeMap = self.mergeColor(self.colorMap)
        self.imageSave(mergeMap, name=render_file_name+"-merge"  )
        
        # test
        # imagepath = "./render/iron-merge.jpg"
        # mergeMap = cv2.imread(imagepath) 
        
        # 색 넘버 : 포지션 -> 딕셔너리 // 색 개수 파악
        dict =  self.__createColorDict(mergeMap)
        print(" ======= COLOR Numbers ======")
        print("color:", len(dict.keys()))
        
        self.lineByColor(dict)
            
        
        # 달라진 부분 체크 -> 달라지지 않으면 흰색
        # changeMap = self.checkChange(images, self.colorMap)
        # self.imageSave(changeMap, name=render_file_name+"-change_area"  )
        
        # 라인 체크해보자
        print("line detect start")
        self.lineDetected = self.drawLine(mergeMap)
        print("line detect end")
        self.imageSave(self.lineDetected, name=render_file_name+"-line2"  )
        
        
        linecolor = imageMerge(mergeMap, self.lineDetected )
        self.imageSave(linecolor, name=render_file_name+"-linecolor2"  )
        
        return 
    
    def lineByColor(self, dict):
        def getContour(img):
            img = 255-img
            print( type(img) )
            img = cv2.convertScaleAbs(img)
            imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, thresh = cv2.threshold(imgray,127,255,0)
            contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            dot = []
            for i in range(len(contours)):
                if cv2.contourArea(contours[i]) == 0: dot.append(i)
            dot.sort()
            dot.reverse()
            for i in dot:  contours.pop(i)

            result = {}

            for i in range(len(contours)):
                result[str(i)] = [cv2.contourArea(contours[i]), contours[i]]
            return result
            
            
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,1))
            
        for color in dict.keys():
            map = np.zeros(self.image.shape) + 255
            g, b, r = color
            for y, x in dict[color]:
                map[y][x] = [g, b, r]
            for y, row in enumerate(map):
                for x, cell in enumerate(row):
                    try:
                        if map[y][x].tolist() == [ g, b, r] and \
                        (map[y+1][x].tolist() == [255, 255, 255] or \
                        map[y][x+1].tolist() == [255, 255, 255] or \
                        map[y][x-1].tolist() == [255, 255, 255] or \
                        map[y-1][x].tolist() == [255, 255, 255]) :
                            map[y][x] = [0, 0, 0]
                    except: pass
            for y, row in enumerate(map):
                for x, cell in enumerate(row):
                    if map[y][x].tolist() == [255, 255, 255]: continue
                    if map[y][x].tolist() != [0, 0, 0]  :
                        map[y][x] = [255, 255, 255]
            # dilation = cv2.dilate(map, kernel)
            # render = cv2.erode(dilation, kernel)
            
            # print("map.shape",map.shape)
            # print("map type", type(map))
            contours = getContour(map)
            for color_key in contours.keys():
                if contours[color_key][0] < 1.0:
                    continue
                else:
                    new_map =  np.zeros(self.image.shape) + 255
                    print(contours[color_key][1])
                    for cood in contours[color_key][1]:
                        print(cood)
                        # print(contours[color_key][1][0][0])
                        new_map[y][x] = [0, 0, 0]
                        print(">",x, y)
                    
                    import time
                    print("image save")
                    time.sleep(2)
                    self.imageSave(new_map, name="./colorline/color-"+self.filename+"-"+str(color)+"-"+color_key)
                        
    
    def mergeColor(self, colorImage):
        def calcSimilarColor(color, hexColors):
            minColor = {} # key: abs / value : hexColorCode
            blue, green, red = color
            for hex in hexColors:
                b, g, r = self.__hex2bgr(hex)
                value = abs(b-blue)  + abs(r-red)  + abs(g-green) 
                # values = b-blue + r-red + g-green
                # if value == 0:  return [b, g, r]
                minColor[value] = [b, g, r]
                
            return minColor[ min(minColor.keys()) ]
        
        map = colorImage.copy()
        colorCode = HexColorCode().hexColorCodeList
        colorDict = {}
        for y, row in enumerate(colorImage):
            if y % 200 ==0: print("merge color:", y)
            for x, color in enumerate(row):
                if tuple(color) in colorDict.keys():
                    map[y][x] = colorDict[tuple(color) ]
                else:
                    hexColor = calcSimilarColor(color, colorCode)
                    map[y][x] = hexColor
                    colorDict[tuple(color) ] = hexColor
                
        return map
    
    
    def drawLine(self, colorMap, value = 2):
        map = []
        tempMap = np.zeros(colorMap.shape) + 255
        count = 0
        # blacklist = []
        for y, row in enumerate(colorMap):
            line = []
            # if y % 10 ==0: print("line draw:", y)
            if y % 100 ==0: print("line draw:", y)
            # xlist = []
            for x, bgr in enumerate(row):
                colorChange = False
                blue, green, red = bgr
                for c in [-1, 1]:
                    try: 
                        
                        # if tempMap[y+c, x].tolist() == [0, 0, 0]: break
                        # if tempMap[y, x+c].tolist() == [0, 0, 0]: break
                        # if tempMap[y-c, x].tolist() == [0, 0, 0]: break
                        # if tempMap[y, x-c].tolist() == [0, 0, 0]: break
                            
                        b, g, r = colorMap[y+c, x]
                        if b-value< blue <b+value and \
                            g-value< green <g+value and \
                            r-value< red <r+value: pass
                        elif tempMap[y+c][x].tolist() == [0, 0, 0] : pass
                        # elif (y+c, x) in blacklist: break
                        else : 
                            # line.append( [0, 0, 0] )
                            tempMap[y, x ]=[0, 0, 0]
                            # blacklist.append( [y, x] )
                            colorChange = True
                            break
                    except IndexError as e: pass
                    
                    try: 
                        
                        # if colorMap[y, x+c].tolist() == [255, 255, 255]: break
                        b, g, r = colorMap[y, x+c]
                            
                        if b-value< blue <b+value and \
                            g-value< green <g+value and \
                            r-value< red <r+value: pass
                        # elif (y, x+c) in blacklist: break
                        elif tempMap[y][x+c].tolist() == [0, 0, 0] : pass
                        else : 
                            # line.append( [0, 0, 0] )
                            tempMap[y, x ]=[0, 0, 0]
                            # xlist.append( [y, x] )
                            colorChange = True
                            break
                    except IndexError as e: pass
                if not colorChange:
                    count +=1
                    # line.append( [255, 255, 255] )
                    tempMap[y, x ]=[255, 255, 255]
                    
            # map.append( line )
        print("count:", count)
        # print("calc line finish")
        # print(np.array(map).shape)
        # print(type(np.array(map)))
        return tempMap
        return np.array(map)
        
    def checkChange(self, image, map):
        maps = []
        for r1, r2 in zip(image, map):
            line = []
            for i, j in zip(r1, r2):
                i, j = list(i), list(j)
                if i == j:
                    line.append([255, 255, 255])
                else:
                    line.append( i )
            maps.append(line)
        return np.array(maps)
    
    def blurring(self, radius = 15, sigmaColor = 90, sigmaSpace = 60) :
        image = self.image.copy()
        div = 32
        qimg = image // div * div + div // 2
        
        '''
        이미지 크기에 맞추어 블러 사이즈 조절하기
        '''
        sigmaColor += self.image.shape[1] * self.image.shape[0] // 100000
        print(" ======= Blur Size ======")
        print("blur:",sigmaColor )
        blurring = cv2.bilateralFilter(qimg,  radius, sigmaColor, sigmaSpace)
        # cv2.imshow("bilateralFilter", dst)
        return blurring
    
    def __bgr2hex(self, bgr):
        hexColor = ""
        for color in bgr: hexColor+= hex(color).split('x')[-1]
        return hexColor
    
    def __hex2bgr(self, hex):
        return tuple(int(hex[i:i+2], 16) for i in (4, 2, 0))
        
    def __createColorDict(self, image, value = 15):
        for y, row in enumerate(image):
            for x, bgr in enumerate(row):
                bgr = tuple(bgr)
                if self.colorDict == {}: self.colorDict[ bgr ] = [ (y, x) ]
                """
                for key in self.colorDict.keys():
                    b, g, r = key
                    blue, green, red = tuple(bgr)
                    if  b-value< blue <b+value and \
                        g-value< green <g+value and \
                        r-value< red <r+value:
                        
                        self.colorDict[key].append( (x, y) )
                        break
                self.colorDict[tuple(bgr)] = [ (x, y) ]
                    
                """
                # hexColor = self.__bgr2hex(bgr)
                if bgr in self.colorDict.keys():
                    self.colorDict[bgr].append( (y, x) )
                else:
                    self.colorDict[bgr] = [ (y, x) ]
                
        # print(self.colorDict)
        return self.colorDict
    
    def __createColorMap(self, blurImage, value = 15, direction = "h"):
        map = []
        '''
        blurImage = blurImage // 3
        print(blurImage)
        for y, row in enumerate(blurImage):
            for x, cell in enumerate(row):
                b, g, r = cell
                if b <30 : b = 30
                if g <30 : g =30
                if r <30 : r =30
                blurImage[y][x] = [ b, g, r ]
        '''
        image_size_ = blurImage.shape[0]
        for y, row in enumerate(blurImage):
            line = []
            if y % 300 == 0: print("processing...", y, "/", image_size_)
            for x, bgr in enumerate(row):
                colorChange = False
                blue, green, red = bgr
                for c in [-1, 1]:
                    
                    try: 
                        if direction == "v":
                            b, g, r = blurImage[y+c, x]
                        else:
                            b, g, r = blurImage[y, x+c]
                            
                        if b==blue and g==green and r==red: pass
                        elif  b-value< blue <b+value and \
                        g-value< green <g+value and \
                        r-value< red <r+value:
                            line.append( [b, g, r] )
                            blurImage[y][x] = [ b, g, r ]
                            colorChange = True
                            break
                    except IndexError as e: pass
                    
                    try: 
                        if direction == "v":
                            b, g, r = blurImage[y, x+c]
                        else:
                            b, g, r = blurImage[y+c, x]
                            
                        if b==blue and g==green and r==red: pass
                        elif  b-value< blue <b+value and \
                        g-value< green <g+value and \
                        r-value< red <r+value: 
                            line.append( [b, g, r] )
                            blurImage[y][x] = [ b, g, r ]
                            colorChange = True
                            break
                    except IndexError as e: pass
                    
                if not colorChange: line.append( [blue, green, red] )
                
            map.append( line )
        
        return np.array(map)
        
    def imageSave(self, image, directory = "./render/", name = ""):
        if name == "": path = os.path.join(directory, self.filename)
        else: path = os.path.join(directory, name+".jpg")
        
        cv2.imwrite(path, image)
        return
    
    def onChange(self, pos): pass
    
    def showBar(self):
        
        cv2.namedWindow("Trackbar Windows")

        cv2.createTrackbar("t", "Trackbar Windows", 0, 200, self.onChange)
        cv2.createTrackbar("j", "Trackbar Windows", 0, 200, self.onChange)

        cv2.setTrackbarPos("t", "Trackbar Windows", 40)
        cv2.setTrackbarPos("j", "Trackbar Windows", 60)

        while cv2.waitKey(1) != ord('q'):

            t = cv2.getTrackbarPos("t", "Trackbar Windows")
            j = cv2.getTrackbarPos("j", "Trackbar Windows")

            dst = self.blurring(t, j)
            print(t, j)
            # dst_ = cv2.resize(dst, dsize=(self.width, self.height))
            cv2.imshow("Trackbar Windows", dst)

        cv2.destroyAllWindows()




if __name__ == "__main__":
    import time
    start = time.time()
    dirpath = "./test/"
    filename = "iron"
    # for filename in ["about", "lala", "her1"]:
    
    color_class = Color( dirpath + filename + ".png" )
    # color_class.showBar()
    value = 110
    blurImage = color_class.blurring(radius = 40, sigmaColor = 50, sigmaSpace = 80)
    # color_class.imageSave(blurImage, name=filename+"-blur")
    color_class.colorProcess(blurImage, direction = "h")
    
    print(f"===  {'filename'}finish... ===")
    print("time :", time.time() - start)
    
    # color_class.imageSave(blurImage) #, name = filename+str(value)
    
    
    
    
    
    
    
    
    
    
    
    
    
    