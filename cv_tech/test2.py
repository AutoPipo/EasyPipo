#cvtest

import cv2
import numpy as np

dirpath = "./dirr/"
filename = "t2"

def hello():
    #image 지정
    filename = "aa"

    #image 읽기 + 비율 유지하며 resize
    img = cv2.imread("./test-image/"+filename+".jpg")
    
    # ratio = 700.0 / img.shape[1]
    # dim = (700, int(img.shape[0] * ratio))
    # img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    #가우스 필터 +Canny edge, 사진별 threshold 지정 필요
    img = cv2.GaussianBlur(img, (5, 5), 0)
    #edge = cv2.Canny(img, 50, 70)
    edge = cv2.Canny(img, 80, 200)

    #이미지 병합하기 + 편지지 붙여넣기
    # size_image= np.shape(edge)
    # blank_image = np.zeros((size_image[0],size_image[1]), np.uint8)
    # i = 150
    # cv2.line(blank_image, (50, i-60), (size_image[1]-50, i-60), (255, 255, 255))
    # while size_image[0]>i:
        # cv2.line(blank_image, (20, i), (size_image[1]-20, i), (255, 255, 255))
        # i=i+50

    #이미지의 가로크기, 세로크기를 확인, 합칠 방향 결정
    # if img.shape[0]>img.shape[1]:
        # black = np.hstack((edge, blank_image))
    # else:
        # black = np.vstack((edge, blank_image))
    white = cv2.bitwise_not(edge)
    #이미지 보여주기 + 저장
    filename1 = "./test-image/"+filename+"1.jpg"
    filename2 = "./test-image/"+filename+"2.jpg"
    # cv2.imshow('black_version', black)
    # cv2.imshow('white_version', white)
    # cv2.imwrite(filename1, black)
    cv2.imwrite(filename2, white)

    #이미지 창 닫기
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def hello2():
    #image 지정
    
    
    #image 읽기 + 비율 유지하며 resize
    img = cv2.imread(dirpath+filename+".jpg")
    
    #가우스 필터 +Canny edge, 사진별 threshold 지정 필요
    ksize = 5
    img = cv2.GaussianBlur(img, (ksize, ksize), 0)
    #edge = cv2.Canny(img, 50, 70)
    edge = cv2.Canny(img, 80, 200)

    white = cv2.bitwise_not(edge)
    
    #이미지 보여주기 + 저장
    filename2 = dirpath+filename+"-1.jpg"
    cv2.imwrite(filename2, white)

    #이미지 창 닫기
    cv2.waitKey(0)
    cv2.destroyAllWindows()

size = 600
height = size+200

def nothing():
    pass

def nothing2():
    path = dirpath+filename+".jpg"
    img_gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    org_img = cv2.imread(path)
    max_value = 400
    
    cv2.namedWindow("Canny Edge")
    cv2.createTrackbar('low threshold', 'Canny Edge', 0, max_value, nothing)
    cv2.createTrackbar('high threshold', 'Canny Edge', 0, max_value, nothing)

    cv2.setTrackbarPos('low threshold', 'Canny Edge', 50)
    cv2.setTrackbarPos('high threshold', 'Canny Edge', 150)
    
    org_img = cv2.resize(org_img, dsize=(size, height))
    cv2.imshow("Original", org_img)
    
    ksize = 5
    img_gray = cv2.GaussianBlur(img_gray, (ksize, ksize), 0)
    
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
    print(">>>", low, high)
    save_ = cv2.Canny(img_gray, low, high)
    save_ = cv2.bitwise_not(save_)
    cv2.imwrite(dirpath+filename+"-line.jpg", save_)


hello2()
nothing2()








