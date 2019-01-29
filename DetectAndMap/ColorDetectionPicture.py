import cv2
import numpy as np
import math
from operator import itemgetter

def detectColor(frame, lower, upper, minArea):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower, upper)

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
    #frame = cv2.imread('gold5.jpg')
    #1080*1920*3
    frame = frame[0:1080,160:1520]
    #frameCopy = frame.copy()
    # define range of green color in HSV
    #use gimp for color code: 160, 20, 73 for green robot
    #212,81,66 for blue robot
    #area +- 1100
    #208,66,87 for cells or 208,63,88
    #area +- 70 - 260
    #172,80,60 for save zone
    #values light off
    lower_greenR = np.array([140/2,10*255/100,60*255/100])
    upper_greenR = np.array([170/2,30*255/100,90*255/100])
    lower_blueR = np.array([200/2,70*255/100,60*255/100])
    upper_blueR = np.array([220/2,90*255/100,75*255/100])
    lower_cells = np.array([200/2,40*255/100,70*255/100])
    upper_cells = np.array([215/2,70*255/100,95*255/100])
    lower_safe = np.array([160/2,70*255/100,50*255/100])
    upper_safe = np.array([180/2,90*255/100,70*255/100])

    #values light on
    lower_greenR = np.array([125/2,10*255/100,75*255/100])
    upper_greenR = np.array([155/2,30*255/100,100*255/100])
    lower_blueR = np.array([200/2,30*255/100,70*255/100])
    upper_blueR = np.array([225/2,75*255/100,90*255/100])
    lower_cells = np.array([195/2,30*255/100,65*255/100])
    upper_cells = np.array([215/2,80*255/100,95*255/100])


    #values gold green T
    lower_greenR = np.array([82/2,0*255/100,50*255/100])
    upper_greenR = np.array([135/2,27*255/100,80*255/100])
    lower_goldR = np.array([38/2,30*255/100,94*255/100])
    upper_goldR = np.array([57/2,68*255/100,90102*255/100])
    lower_cells = np.array([195/2,30*255/100,65*255/100])
    upper_cells = np.array([215/2,80*255/100,95*255/100])

    #TODO crop to all except safe zone
    #detect green
    #that s the robot
    #get xy and orientation
    goldF = detectColor(frame, lower_goldR, upper_goldR, 200)
    greenF = detectColor(frame, lower_greenR, upper_greenR, 200)
    if len(goldF)==0 or len(greenF)==0:
        print(str(len(goldF)) + "  " + str(len(greenF)))
        continue
    goldF = goldF[0]
    greenF = greenF[0]
    #print(blueF)
    #print(greenF)
    goldC = (goldF[0]+goldF[2]/2,goldF[1] + goldF[3]/2)
    greenC = (greenF[0]+greenF[2]/2,greenF[1] + greenF[3]/2)

    #angle with respect to horizontal, positive as anticlockwise. Counterintuitive sign in expression bc y axis inverted
    alpha = math.degrees(math.atan2(-goldC[1]+greenC[1],goldC[0]-greenC[0]))
    print("Angle and coordinates of the robot")
    print(alpha)
    print(greenC)
    #crop image to dangerous black zone (only needed if too imprecise)
    #get coordinates of cells
    #crop_img = img[y:y+h, x:x+w]
    #frame2 = frameCopy[20:1060,740:1400];
    rectMines = detectColor(frame, lower_cells, upper_cells,5);
    coordMines=[]
    for rect in rectMines:
        coordMines.append((rect[0]+rect[2]/2,rect[1] + rect[3]/2))
    coordMines = sorted(coordMines,key=lambda x:(x[1],x[0]))

    print("Coordinates of cells")
    print(coordMines)

    cv2.imshow('frame',frame)
    cv2.waitKey(0)

#cap.release()
#cv2.destroyAllWindows()
