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
    def __init__ (self, filepath, job_id = "job123", file_id = ""):
        self.__job_id = job_id
        self.colorDict = {}
        self.colorMap = np.array([])
        self.lineDetected = np.array([])
        self.file_id = file_id
        
        self.width, self.height = 800, 500
        
        self.__imageSetting( filepath )
        
    def __imageSetting(self, imagepath):
        self.filename = os.path.basename(imagepath)
        self.image = cv2.imread(imagepath) #, cv2.IMREAD_GRAYSCALE
        
        # 확대
        # self.image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        print("======== IMAGE SHAPE   ========")
        print("shape:", self.image.shape)
        
        # self.rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
        # a = [30, 56, 87]
        # hexColor = self.__bgr2hex(a)
        # print(hexColor)
        return
    
    def colorProcess(self, image, direction = "h"):
        def imageMerge(image, map):
            new_map = np.zeros(image.shape) + 255
            for y, row in enumerate(image):
                if y % 300 == 0: print("line+color processing...", y, "/", image.shape[0])
                for x, bgr in enumerate(row):
                    
                    if map[y][x].tolist() == [0, 0, 0]:
                        new_map[y][x] = [0, 0, 0]
                    else:
                        new_map[y][x] = bgr.tolist()
                    
            return new_map
            
        print("color process start")
        print(" ======= File Name ======")
        print("file:", self.filename)
        render_file_name = self.filename.split(".")[0]
        # images = image.copy()
        
        # 원래 이거
        self.colorMap = self.__createColorMap(image, direction = "h")
        # 이건 라인 검출 테스트용 
        # self.colorMap = cv2.imread("./render/"+render_file_name+"-merge7.jpg")
        
        print(" ======= Convert Image Size ======")
        print("size:",self.colorMap.shape )
        self.imageSave(self.colorMap, name=render_file_name+"-change" +self.file_id )
        
        
        mergeMap = self.mergeColor(self.colorMap)
        self.imageSave(mergeMap, name=render_file_name+"-merge"  +self.file_id  )
        
        # test
        # imagepath = "./render/iron-merge.jpg"
        # mergeMap = cv2.imread(imagepath) 
        
        # 색 넘버 : 포지션 -> 딕셔너리 // 색 개수 파악
        dict =  self.__createColorDict(  mergeMap) #self.colorMap) #
        print(" ======= COLOR Numbers ======")
        print("color:", len(dict.keys()))
        
        # self.lineByColor(dict)
            
        
        # 달라진 부분 체크 -> 달라지지 않으면 흰색
        # changeMap = self.checkChange(images, self.colorMap)
        # self.imageSave(changeMap, name=render_file_name+"-change_area"  )
        
        # 라인 체크해보자
        print("line detect start")
        self.lineDetected = self.drawLine(mergeMap)
        
        linecolor = imageMerge(mergeMap, self.lineDetected )
        self.imageSave(linecolor, name=render_file_name+"-linecolor"  +self.file_id  )
        
        # Image 확장
        expandSize = ( 5000 // image.shape[1] ) +1
        print("======== Expand   ========")
        print("expandSize:", expandSize)
        self.lineDetected = cv2.resize(self.lineDetected, None, fx=expandSize, fy=expandSize, interpolation=cv2.INTER_CUBIC)
        
        
        
        print("line detect end")
        self.imageSave(self.lineDetected, name=render_file_name+"-line"  +self.file_id  )
                
        
        #크게
        '''
        
        self.lineDetectedExpand = cv2.cvtColor(self.lineDetected, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))
        zoom1 = cv2.resize(self.lineDetectedExpand, None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC)
        # self.imageSave(zoom1, name=render_file_name+"-size2-cub"  )
        
        render = cv2.dilate(zoom1, kernel)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        render = cv2.erode(render, kernel)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        render = cv2.dilate(render, kernel)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        render = cv2.erode(render, kernel)
        '''
        
        # zoom2 = cv2.resize(self.lineDetected, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
        # self.imageSave(render, name=render_file_name+"-size2-lin"  +self.file_id  )
        
        
        return 
    
    def lineByColor(self, dict):
        #      self.image   <== 원본 이미지 
        def getContour(img):
            img = 255-img
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
            
        result = []
        count, all = 0, len(dict.keys())
        for color in dict.keys():
            count +=1
            if count % 10 ==0: print("color process..",count ,"/",  all)
            
            map = np.zeros(self.image.shape) + 255
            # g, b, r = color
            for y, x in dict[color]:
                map[y][x] = [0, 0, 0]#[g, b, r]
            # for y, row in enumerate(map):
                # for x, cell in enumerate(row):
                    # try:
                        # if map[y][x].tolist() == [ g, b, r] and \
                        # (map[y+1][x].tolist() == [255, 255, 255] or \
                        # map[y][x+1].tolist() == [255, 255, 255] or \
                        # map[y][x-1].tolist() == [255, 255, 255] or \
                        # map[y-1][x].tolist() == [255, 255, 255]) :
                            # map[y][x] = [0, 0, 0]
                    # except: pass
            # for y, row in enumerate(map):
                # for x, cell in enumerate(row):
                    # if map[y][x].tolist() == [255, 255, 255]: continue
                    # if map[y][x].tolist() != [0, 0, 0]  :
                        # map[y][x] = [255, 255, 255]
            
            contours = getContour(map)
            print(color)
            for color_key in contours.keys():
                result = []
                import time
                time.sleep(0.05)
                if contours[color_key][0] <= 1.0:
                    print("pass-")
                    continue
                else:
                    new_map =  np.zeros(self.image.shape) + 255
                    print("forfor")
                    for cood in contours[color_key][1]:
                        y, x = cood[0][1], cood[0][0]
                        new_map[y][x] = [0, 0, 0]
                    yield new_map
                    result.append( new_map )
        print( np.array(result[:10]))
        return np.array(result)
    
    def mergeColor(self, colorImage):
        def calcSimilarColor(color, hexColors):
            minColor = {} # key: abs / value : hexColorCode
            blue, green, red = color
            for hex in hexColors:
                b, g, r = self.__hex2bgr(hex)
                value = abs(b-blue)  + abs(r-red)  + abs(g-green) 
                
                minColor[value] = [b, g, r]
                if value ==0: return [b, g, r]
                
            return minColor[ min(minColor.keys()) ]
        
        map = colorImage.copy()
        colorCode = HexColorCode().hexColorCodeList
        colorDict = {}
        for y, row in enumerate(colorImage):
            if y % 200 ==0: print("merge color process..:", y)
            for x, color in enumerate(row):
                if tuple(color) in colorDict.keys():
                    map[y][x] = colorDict[tuple(color) ]
                else:
                    hexColor = calcSimilarColor(color, colorCode)
                    map[y][x] = hexColor
                    colorDict[tuple(color) ] = hexColor
                
        return map
    
    
    def drawLine(self, colorMap, value = 1):
        #          여기서 이제 라인 빈공간 없애기
        map = []
        tempMap = np.zeros(colorMap.shape) + 255
        
        image_size_ = blurImage.shape[0]
        # blacklist = []
        for y, row in enumerate(colorMap):
            line = []
            # if y % 10 ==0: print("line draw:", y)
            if y % 200 ==0: print("line draw process:", y,"/", image_size_ )
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
                    # line.append( [255, 255, 255] )
                    tempMap[y, x ]=[255, 255, 255]
                    
            # map.append( line )
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
    
    def blurring(self, radius = 40, sigmaColor = 70, sigmaSpace = 60) :
        image = self.image.copy()
        div = 32
        qimg = image // div * div + div // 2
        
        '''
        이미지 크기에 맞추어 블러 사이즈 조절하기
        '''
        sigmaColor += (self.image.shape[1] * self.image.shape[0]) // 100000
        radius += (self.image.shape[1] * self.image.shape[0]) // 100000
        
        print(" ======= Blur Size ======")
        print("blur:",sigmaColor )
        print(" ======= radius Size ======")
        print("radius:",radius )
        
        blurring = cv2.bilateralFilter(qimg,  radius, sigmaColor, sigmaSpace)
        blurring = cv2.medianBlur(blurring, 5)
        blurring = cv2.resize(blurring, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        print("Blur Over..")
        # cv2.imshow("bilateralFilter", dst)
        return blurring
    
    def __bgr2hex(self, bgr):
        hexColor = ""
        for color in bgr: hexColor+= hex(color).split('x')[-1]
        return hexColor
    
    def __hex2bgr(self, hex):
        return tuple(int(hex[i:i+2], 16) for i in (4, 2, 0))
        
    def __createColorDict(self, image):
        for y, row in enumerate(image):
            for x, bgr in enumerate(row):
                bgr = tuple(bgr)
                if self.colorDict == {}: 
                    self.colorDict[ bgr ] = [ (y, x) ]
                    continue
                
                if bgr in self.colorDict.keys():
                    self.colorDict[bgr].append( (y, x) )
                else:
                    self.colorDict[bgr] = [ (y, x) ]
                
        return self.colorDict
    
    def __createColorMap(self, blurImage, value = 15, direction = "h"):
        map = []
        
        image_size_ = blurImage.shape[0]
        for y, row in enumerate(blurImage):
            line = []
            if y % 300 == 0: print("similar color processing...", y, "/", image_size_)
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
    filename = "lala"
    # for filename in ["about", "lala", "her1"]:
    
    color_class = Color( dirpath + filename + ".jpg", file_id = "-0" )
    
    blurImage = color_class.blurring(radius = 20, sigmaColor = 40, sigmaSpace = 80)
    color_class.imageSave(blurImage, name=filename+"-blur")
    color_class.colorProcess(blurImage, direction = "h")
    
    print(f"===  {'filename'}finish... ===")
    print("time :", round((time.time() - start)/60, 3) ,"분 정도.." )
    
    # color_class.imageSave(blurImage) #, name = filename+str(value)
    
    
    
    
    
    
    
    
    
    
    
    
    
    