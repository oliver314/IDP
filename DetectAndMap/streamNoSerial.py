import cv2
import numpy as np
import math
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
print("Imports done")
cap = cv2.VideoCapture(1)
#ArduinoSerial = serial.Serial('com3', 9600)  # Create Serial port object called arduinoSerialData
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

#values gold green T
lower_greenR = np.array([70/2,0*255/100,50*255/100])
upper_greenR = np.array([135/2,27*255/100,92*255/100])
lower_goldR = np.array([320/2,10*255/100,70*255/100])
upper_goldR = np.array([360/2,60*255/100,110*255/100])
#lower_goldR = np.array([38/2,30*255/100,94*255/100])
#upper_goldR = np.array([57/2,68*255/100,102*255/100])
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
            coord.append((x,y,w,h))
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
timeLastCell = time.time()

count = 0
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
        #cropping needed because of choice of blue rectangle on robot not anymore #[0:480,100:560]
        rectMines = detectColor(frame, lower_cells, upper_cells,5);
        for rect in rectMines:
            coordMines.append((rect[0]+rect[2]/2,rect[1] + rect[3]/2))

        #starts at lowest y and goes up
        coordMines = sorted(coordMines,key=lambda x:(x[1],x[0]))

        print("Coordinates of cells")
        print(coordMines)
        if(len(coordMines)==0):
            continue
        coordMines.append((0,270))
        coordMines.append((30,60))
        firstTime = False

    #crop to all except safe zone
    #detect green
    #that s the robot
    #get xy and orientation
    goldF = detectColor(frame, lower_goldR, upper_goldR, 120)
    greenF = detectColor(frame, lower_greenR, upper_greenR, 120)
    
    if len(goldF)==0 or len(greenF)==0:
        print(str(len(goldF)) + "  " + str(len(greenF)))
        if(count % 5 == 0):
            cv2.imwrite("frame" + str(count/5)+ ".png", frame)
        count+=1
        continue
    goldF = goldF[0]
    greenF = greenF[0]
    #print(goldF)
    #print(greenF)
    goldC = (goldF[0]+goldF[2]/2,goldF[1] + goldF[3]/2)
    greenC = (greenF[0]+greenF[2]/2,greenF[1] + greenF[3]/2)

    #angle with respect to horizontal, positive as anticlockwise. Counterintuitive sign in expression bc y axis inverted
    alpha = math.degrees(math.atan2(-goldC[1]+greenC[1],goldC[0]-greenC[0]))
    print("Angle and coordinates of the robot")
    print(alpha)
    print(greenC)

    targetMine = coordMines[cellsChecked]

    cv2.circle(frame,(round(targetMine[0]),round(targetMine[1])), 10, (0,0,255), -1)
    alphaRef = math.degrees(math.atan2(-targetMine[1]+greenC[1],targetMine[0]-greenC[0]))

    errorAngleOldOld = errorAngleOld
    errorAngleOld = errorAngle
    errorAngle = alphaRef-alpha
    print("ErrorAngle")
    print(errorAngle)


    PD = 0
    #makes no sense to try and correct course while driving
    if errorAngle > 45:
        print("Turn left")
        PD = 254
        #ArduinoSerial.write((254).to_bytes(1, 'big'))
    elif errorAngle < -45:
        print("Turn right")
        PD = 255
        #ArduinoSerial.write((255).to_bytes(1, 'big'))
    else:
        deriv = (errorAngle-errorAngleOldOld)/(2*deltaT)
        PD = kd * deriv + kp * errorAngle 
        #transform value to 0 to 200
        print("Value passed to Arduino")
        print(100 + 200*PD) #thus 100 means straight, and above 100 is to left
        PD = 100 + 200*PD

    if PD < 0:
        PD = 0
    elif PD > 255:
        PD = 251

    #if Arduino detect that it caught the cell
    #if ArduinoSerial.in_waiting:
     #   if ArduinoSerial.readline().decode('utf-8') == 0:
    #        cellsChecked += 1
    #        timeLastCell = time.time()

    #or if has been looking for ages, pass to next
    if (time.time() - timeLastCell) > 30:
        timeLastCell = time.time()
        cellsChecked += 1

    #returning back to safe zone. Check whether arrived
    if cellsChecked == (len(coordMines)-2) and goldC[0] < 20 and abs(goldC[1] -270) < 20:
        PD = 253
    #returning back to start zone. Check whether arrived
    if cellsChecked == (len(coordMines)-1) and abs(goldC[0]-30) < 30 and abs(goldC[1] -60) < 30:
        PD = 252
        PD = 252
    #ArduinoSerial.write(round(PD).to_bytes(1, 'big'))
    time.sleep(0.2)

    deltaT = time.time()-timeOld
    timeOld = time.time()


    cv2.imshow('frame',frame)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
