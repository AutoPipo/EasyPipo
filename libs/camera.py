import cv2
# from brush import Brush

cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    
    
    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # canny = cv2.Canny(blur, 10, 70)
    # ret, mask = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
    
    
    
    canny = cv2.medianBlur(img, 7)
    # canny = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(canny, 10, 70)
    _ , mask = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
    
    
    cv2.imshow('Video feed', mask)
    
    if cv2.waitKey(1) == 13:
        break
cap.release()
cv2.destroyAllWindows()