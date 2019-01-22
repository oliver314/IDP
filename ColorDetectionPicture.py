import cv2
import numpy as np


def detectColor(frame, lower, upper, minArea):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



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
    
    coord = []
    for cnt in contours:
        #Contour area is taken
        area = cv2.contourArea(cnt)

        if area >minArea:

           #draw rectangle around found zones
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            coord.append((x,y,w,h))
    return coord

fool=True
while(fool):
    fool=False
    # Take one
    frame = cv2.imread('test2.jpg')
    

    # define range of green color in HSV
    lower_green = np.array([55,60,100])
    upper_green = np.array([80,255,255])

    #TODO crop to all except safe zone
    #detect green
    #that s the robot
    #get xy and orientation
    detectColor(frame, lower_green, upper_green, 1000);


    # define range of blue color in HSV
    lower_blue = np.array([110,50,130])
    upper_blue = np.array([170,255,255])
    #crop image to dangerous black zone
    #get coordinates of cells
    #crop_img = img[y:y+h, x:x+w]
    frame2 = frame[50:900,130:450];
    detectColor(frame2, lower_blue, upper_blue,100);

    cv2.imshow('frame',frame2)
    cv2.waitKey(0)
    
    cv2.imshow('frame',frame)
    cv2.waitKey(0)
#cap.release()
#cv2.destroyAllWindows()
