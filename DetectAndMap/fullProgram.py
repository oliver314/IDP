import cv2
import numpy as np
import math
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
print("Imports done")
cap = cv2.VideoCapture(1)
#ArduinoSerial = serial.Serial('com5', 9600)  # Create Serial port object called arduinoSerialData
print("Capture started")
time.sleep(2)  # wait for 2 secounds for the communication to get established

# define range of green color in HSV
#use gimp for color code: 160, 20, 73 for green robot
#212,81,66 for blue robot
#area +- 1100
#208,66,87 for cells or 208,63,88
#area +- 70 - 260
#172,80,60 for save zone
#values light on(light off is more accurate, values in ColorDetectionPicture.py)
lower_greenR = np.array([120/2,10*255/100,75*255/100])
upper_greenR = np.array([155/2,30*255/100,100*255/100])
lower_blueR = np.array([200/2,30*255/100,70*255/100])
upper_blueR = np.array([225/2,75*255/100,90*255/100])
lower_cells = np.array([195/2,30*255/100,65*255/100])
upper_cells = np.array([215/2,80*255/100,95*255/100])

def detectColor(frame, lower, upper, minArea):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower, upper)

    #cv2.imshow('frame',mask)
    #cv2.waitKey(0)
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
            coord.append((100+x,y,w,h))
    return coord

firstTime = True
coordMines=[]
cellsChecked = 0
errorAngle = 0
errorAngleOld = 0
errorAngleOldOld = 0
timeOld = 0
deltaT = 1
kd = 0.01
kp = 0.01

while(1):
    # Take each frame
    _, frame = cap.read()
    #1080*1920*3
    frame = frame[0:480, 0:560]
    #frameCopy = frame.copy()

    if firstTime:
        #crop image to dangerous black zone (only needed if too imprecise)
        #get coordinates of cells
        #crop_img = img[y:y+h, x:x+w]
        #frame2 = frameCopy[20:1060,740:1400];
        #cropping needed because of choice of blue rectangle on robot
        rectMines = detectColor(frame[0:480,100:560], lower_cells, upper_cells,5);
        for rect in rectMines:
            coordMines.append((rect[0]+rect[2]/2,rect[1] + rect[3]/2))

        coordMines = sorted(coordMines,key=lambda x:(x[1],x[0]))

        print("Coordinates of cells")
        print(coordMines)
        firstTime = False

    #crop to all except safe zone
    #detect green
    #that s the robot
    #get xy and orientation
    blueF = detectColor(frame, lower_blueR, upper_blueR, 200)
    greenF = detectColor(frame, lower_greenR, upper_greenR, 200)
    if len(blueF)==0 or len(greenF)==0:
        print(len(blueF)  + " " + len(greenF))
        continue
    blueF = blueF[0]
    greenF = greenF[0]
    #print(blueF)
    #print(greenF)
    blueC = (blueF[0]+blueF[2]/2,blueF[1] + blueF[3]/2)
    greenC = (greenF[0]+greenF[2]/2,greenF[1] + greenF[3]/2)

    #angle with respect to horizontal, positive as anticlockwise. Counterintuitive sign in expression bc y axis inverted
    alpha = math.degrees(math.atan2(-blueC[1]+greenC[1],blueC[0]-greenC[0]))
    print("Angle and coordinates of the robot")
    print(alpha)
    print(greenC)

    targetMine = coordMines[cellsChecked]
    alphaRef = math.degrees(math.atan2(-targetMine[1]+greenC[1],targetMine[0]-greenC[0]))

    errorAngleOldOld = errorAngleOld
    errorAngleOld = errorAngle
    errorAngle = alphaRef-alpha
    print("ErrorAngle")
    print(errorAngle)

    #makes no sense to try and correct course while driving
    if errorAngle > 45:
        print("Turn left")
        #ArduinoSerial.write(254)
    elif errorAngle < -45:
        print("Turn right")
        #ArduinoSerial.write(255)
    else:
        deriv = (errorAngle-errorAngleOldOld)/(2*deltaT)
        PD = kd * deriv + kp * errorAngle 
        #transform value to 0 to 200
        print("Value passed to Arduino")
        print(PD)
        #ArduinoSerial.write(PD)
    time.sleep(0.2)


    #if ArduinoSerial.readline().decode('utf-8') == 0:
    #cellsChecked += 1

    #cv2.imshow('frame',frame)
    #cv2.waitKey(0)
    deltaT = time.time()-timeOld
    timeOld = time.time()

cap.release()
cv2.destroyAllWindows()
