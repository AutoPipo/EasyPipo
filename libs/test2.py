#python
#opencv test
import matplotlib.pyplot as plt
import cv2
import numpy as np

dirpath = "./test-image/"
# dirpath ="C:\\Users\\구민구\\Desktop\\joljac\\test-image\\"
imagename = "app"
file_ = ".jpg"

the_image = dirpath + imagename + file_ 
size = 600
height = size+200

def nothing():
    pass

def nothing2(paths):
    path = "./line/"+paths+".jpg"
    img_gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    org_img = cv2.imread(path)
    max_value = 400
    
    cv2.namedWindow("Canny Edge")
    cv2.createTrackbar('low threshold', 'Canny Edge', 0, max_value, nothing)
    cv2.createTrackbar('high threshold', 'Canny Edge', 0, max_value, nothing)

    cv2.setTrackbarPos('low threshold', 'Canny Edge', 1)
    cv2.setTrackbarPos('high threshold', 'Canny Edge', 50)
    
    org_img = cv2.resize(org_img, dsize=(size, height))
    cv2.imshow("Original", org_img)
    
    
    while True:
        
        low = cv2.getTrackbarPos('low threshold', 'Canny Edge')
        high = cv2.getTrackbarPos('high threshold', 'Canny Edge')
        
        print(">", low, high)
        
        img_gray_ = cv2.resize(img_gray, dsize=(size, height))
        
        img_canny = cv2.Canny(img_gray_, low, high)
        cv2.imshow("Canny Edge", img_canny)
        # cv2.imwrite(dirpath+"test.jpg", img_canny)
        
        if cv2.waitKey(1)&0xFF == 27:
            break


    cv2.destroyAllWindows()
    save_ = cv2.Canny(img_gray, low, high)
    cv2.imwrite("./line/"+paths+"-line.jpg", save_)
    
    '''
    라인 노이즈 제거 해볼까
    h = 99
    save_ = cv2.imread(dirpath+imagename+"-line.jpg")
    save_ = cv2.cvtColor(save_, cv2.COLOR_BGR2GRAY)
    denoise = cv2.fastNlMeansDenoising(save_,  h, 15, 7, 21)
    cv2.imwrite(dirpath+imagename+"-line-noise.jpg", denoise)
    
    save_ = cv2.imread(dirpath+imagename+"-line.jpg", cv2.IMREAD_GRAYSCALE)
    # kern = np.ones((5,5), np.uint8)
    kern = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    denoise = cv2.morphologyEx(save_, cv2.MORPH_OPEN, kern)
    # denoise = cv2.morphologyEx(save_, cv2.MORPH_CLOSE, kern)
    
    
    
    thres = cv2.adaptiveThreshold(save_, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 2)
    el = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thres = cv2.erode(thres, el)
    denoise = cv2.dilate(thres, el) #오프닝
    
    cv2.imwrite(dirpath+imagename+"-line-noise-erosion.jpg", denoise)

    '''
    


def cartoon1(the_image):
    num_down = 2       # number of downsampling steps
    num_bilateral = 7  # number of bilateral filtering steps

    img_rgb = cv2.imread(the_image)

    # downsample image using Gaussian pyramid
    img_color = img_rgb
    for _ in range(num_down):
        img_color = cv2.pyrDown(img_color)

    # repeatedly apply small bilateral filter instead of
    # applying one large filter
    for _ in range(num_bilateral):
        img_color = cv2.bilateralFilter(img_color, d=9,
                                        sigmaColor=9,
                                        sigmaSpace=7)

    # upsample image to original size
    for _ in range(num_down):
        img_color = cv2.pyrUp(img_color)
        
    # convert to grayscale and apply median blur
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)
    
    img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                 cv2.ADAPTIVE_THRESH_MEAN_C,
                                 cv2.THRESH_BINARY,
                                 blockSize=9,
                                 C=2)
                                 
    # convert back to color, bit-AND with color image
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    img_cartoon = cv2.bitwise_and(img_color, img_edge)

    # display
    size =600
    img_cartoon = cv2.resize(img_cartoon, dsize=(size, size+200))
    cv2.imshow("cartoon", img_cartoon)
    # cv2.imwrite(dirpath+imagename+"-c.jpg", img_cartoon)
    cv2.waitKey(0)

# nnn(the_image)

def cartoon2(img_path):
    #Importing required libraries
    
    # from google.colab.patches import cv2_imshow

    #Reading image 
    img = cv2.imread(img_path)
    print(img_path)
    # from skimage import io 
    # io.imshow(img)

    #Converting to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.resize(img, dsize=(size, height))
    # cv2.imshow("org",img)

    #Detecting edges of the input image
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    median_blur_size = 3
    gray = cv2.medianBlur(gray, median_blur_size)
    # gray = cv2.bilateralFilter(gray, d=10, sigmaColor=20, sigmaSpace=20)

    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 11)
    edges_ = cv2.resize(edges, dsize=(size, height))
    # cv2.imshow("edges",edges_)
    
    # import time
    # time.sleep(3)
    #Cartoonifying the image
    sigma = 500
    d_value = 9
    color = cv2.bilateralFilter(img, d=d_value, sigmaColor=sigma, sigmaSpace=sigma)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    
    cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    cartoon_ = cv2.resize(cartoon, dsize=(size, height))

    # cv2.imshow("cartoon",cartoon_)
    # cv2.imwrite(dirpath+imagename+"-d-"+str(d_value)+"-c.jpg", cartoon)
    cv2.imwrite(dirpath+imagename+"-c.jpg", cartoon)
    cv2.waitKey(0)

def cartoon3(path):
    img = cv2.imread(path)
    cartoon_img = cv2.stylization(img, sigma_s=100, sigma_r=0.7) 
    
    cartoon_img_ = cv2.resize(cartoon_img, dsize=(size, height))
    cv2.imshow("cartoon",cartoon_img_)
    cv2.imwrite(dirpath+imagename+"-cc.jpg", cartoon_img)
    cv2.waitKey(0)

def saving(path, s, r, way):
    img = cv2.imread(path)
    cartoon_img = cv2.stylization(img, sigma_s=s, sigma_r=r) 
    if way == "s":
        cv2.imwrite(dirpath+imagename+"-cc"+"-"+way+"-"+str(s)+".jpg", cartoon_img)
    else:
        cv2.imwrite(dirpath+imagename+"-cc"+"-"+way+"-"+str(r)+".jpg", cartoon_img)

def R(path):
    for s in range(1,5):
        saving(path, s*50, 0.5,"s")
    for r in range(1,5):
        saving(path, 100, r*0.2,"r") 

def cartoon4(path):
    # Reading the Image 
    image = cv2.imread(path)
    # Finding the Edges of Image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    gray = cv2.medianBlur(gray, 9) 
    # gray = cv2.resize(gray, dsize=(size, height))
    # cv2.imshow("cartoon",gray)
    # cv2.waitKey(0)
    
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 10)
    # Making a Cartoon of the image
    color = cv2.bilateralFilter(image, 3, 300, 300) 
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    #Visualize the cartoon image 
    # cartoon_img_ = cv2.resize(cartoon, dsize=(size, height))
    # cv2.imshow("cartoon",cartoon_img_)
    
    save_path = "./setting/"+imagename+"-ccc-w"
    cv2.imwrite(save_path + ".jpg", cartoon)
    
    # cv2.waitKey(0) # "0" is Used to close the image window
    # cv2.destroyAllWindows()
    
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cv2.imwrite(save_path+"-line.jpg", cartoon)
    

def ttest(path, s, r, way):
    image = cv2.imread(path)
    # Finding the Edges of Image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    gray = cv2.medianBlur(gray, 7) 
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)
    # Making a Cartoon of the image
    color = cv2.bilateralFilter(image, 10, s, r) 
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    print(path)
    #Visualize the cartoon image 
    if way == "s":
        cv2.imwrite("./setting/"+imagename+"-ccc-"+way+"-"+str(s)+".jpg", cartoon)
    else:
        cv2.imwrite("./setting/"+imagename+"-ccc-"+way+"-"+str(r)+".jpg", cartoon)

def ssss():
    for s in range(1,5):
        ttest(the_image, s*120, 250, "s")
    for r in range(1,5):
        ttest(the_image, 250, r*120, "r")

def ftest():
    dirpath = "./test-image/"
    filename = "a1"
    image = cv2.imread(dirpath + filename    +".jpg")
    
    size = 1000
    height = 700
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    gray = cv2.medianBlur(gray, 7) 
    edges = cv2.adaptiveThreshold(gray, 
                                255, 
                                cv2.ADAPTIVE_THRESH_MEAN_C, 
                                cv2.THRESH_BINARY, 
                                11, 
                                5
                                )
    
    edgess = cv2.resize(edges, dsize=(size, height))
    cv2.imshow("cartooon", edgess)
    cv2.waitKey(0) 
    
    color = cv2.bilateralFilter(image, 10, 200, 250) 
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cartoon = cv2.resize(cartoon, dsize=(size, height))
    cv2.imshow("cartooon", cartoon)
    cv2.waitKey(0) 
    
    # cv2.imwrite("./result-image/"+filename+"-result-"+".jpg", cartoon)
    
# cartoon2(the_image)
# cartoon4(the_image)
# ssss()
# R(the_image)
ftest()






