import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # define range of blue color in HSV
    lower_blue = np.array([110,50,130])
    upper_blue = np.array([150,255,255])

    # define range of green color in HSV
    lower_green = np.array([55,60,100])
    upper_green = np.array([80,255,255])
    #lower_green = np.array([0,100,100])
    #upper_green = np.array([179,255,255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    kernel = np.ones((5,5),'int')
    dilated = cv2.dilate(mask,kernel)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask=mask)
    ret,thrshed = cv2.threshold(cv2.cvtColor(res,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
    contours,hier = cv2.findContours(thrshed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        #Contour area is taken
        area = cv2.contourArea(cnt)

        if area >1000:

           #draw rectangle around found zones
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    #the same for blue

    # Threshold the HSV image to get only green colors
    mask2 = cv2.inRange(hsv, lower_blue, upper_blue)

    #cv2.imshow('frame',mask2)
    
    kernel2 = np.ones((5,5),'int')
    dilated2 = cv2.dilate(mask2,kernel2)
    # Bitwise-AND mask and original image
    res2 = cv2.bitwise_and(frame,frame, mask=mask2)
    ret2,thrshed2 = cv2.threshold(cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
    contours2,hier2 = cv2.findContours(thrshed2,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours2:
        #Contour area is taken
        area = cv2.contourArea(cnt)

        if area >1000:

           #draw rectangle around found zones
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

    cv2.imshow('frame',frame)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        cv2.imwrite('Table.png',frame)
        break
cap.release()
cv2.destroyAllWindows()
