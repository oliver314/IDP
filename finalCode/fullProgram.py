import cv2
import numpy as np
import math
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
import keyboard
print("Imports done")
cap = cv2.VideoCapture(1)
tp = serial.Serial('com7', 9600)  # Create Serial port object called arduinoSerialData
print("Capture started")
time.sleep(2)  # wait for 2 secounds for the communication to get established

#values gold green T
lower_greenR = np.array([70/2,0*255/100,50*255/100])
upper_greenR = np.array([135/2,27*255/100,92*255/100])
lower_goldR = np.array([320/2,10*255/100,70*255/100])
upper_goldR = np.array([360/2,60*255/100,110*255/100])
lower_cells = np.array([195/2,30*255/100,65*255/100])
upper_cells = np.array([215/2,80*255/100,95*255/100])

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

def getClosestCell(goldC , rigthLimit):
    closest = 490000
    minMin = [0,0]
    for mine in coordMines:
        if (mine[0] > 50) and (mine[0] < rightLimit):
            if((mine[0]-goldC[0])**2 + (mine[1] - goldC[1])**2) < closest:
                minMin = mine
                closest = (mine[0]-goldC[0])**2 + (mine[1] - goldC[1])**2

    return minMin

firstTime = True
coordMines=[]
#cellsChecked = 0
errorAngle = 0
errorAngleOld = 0
errorAngleOldOld = 0
timeOld = 0
deltaT = 1
kd = 0.0001
kp = 0.01
timeLastCell = time.time()
count = 0
firstGo = True

#start on space
while not keyboard.is_pressed(' '):
    pass

while(cap.isOpened()):
    # Take each frame
    _, frame = cap.read()
    print()
    #1080*1920*3
    frame = frame[0:480, 0:560]
    #frameCopy = frame.copy()

    if firstTime:
        rectMines = detectColor(frame, lower_cells, upper_cells,5);
        for rect in rectMines:
            coordMines.append((rect[0]+rect[2]/2,rect[1] + rect[3]/2))
        #starts at lowest y and goes up, ie from top to bottom if image 
        coordMines = sorted(coordMines,key=lambda x:(x[1],x[0]))

        print("Coordinates of cells")
        print(coordMines)
        if(len(coordMines)==0):
            continue
        coordMines.append((0,270))
        coordMines.append((15,75))
        firstTime = False

    #crop to all except safe zone
    #detect green
    #that s the robot
    #get xy and orientation
    goldF = detectColor(frame, lower_goldR, upper_goldR, 120)
    greenF = detectColor(frame, lower_greenR, upper_greenR, 120)
    
    if len(goldF)==0 or len(greenF)==0:
        print(str(len(goldF)) + "  " + str(len(greenF)))
        #(count % 5 == 0):
            #cv2.imwrite("frame" + str(count/5)+ ".png", frame)
        count+=1
        continue
    goldF = goldF[0]
    greenF = greenF[0]
    goldC = (goldF[0]+goldF[2]/2,goldF[1] + goldF[3]/2)
    greenC = (greenF[0]+greenF[2]/2,greenF[1] + greenF[3]/2)

    #angle with respect to horizontal, positive as anticlockwise. Counterintuitive sign in expression bc y axis inverted
    alpha = math.degrees(math.atan2(-goldC[1]+greenC[1],goldC[0]-greenC[0]))
    #print("Angle and coordinates of the robot")
    #print(alpha)
    #print(greenC)

    #targetMine = coordMines[cellsChecked]
    if firstGo:
        rightLimit = 520
    else:
        rightLimit = 560
    if(len(coordMines)<3):
        targetMine = coordMines[0]
    else:
        targetMine = getClosestCell(goldC, rightLimit)

    cv2.circle(frame,(round(targetMine[0]),round(targetMine[1])), 10, (0,0,255), -1)
    alphaRef = math.degrees(math.atan2(-targetMine[1]+greenC[1],targetMine[0]-greenC[0]))

    errorAngleOldOld = errorAngleOld
    errorAngleOld = errorAngle
    errorAngle = alphaRef-alpha
    print("ErrorAngle")
    print(errorAngle)




    PD = 0
    #makes no sense to try and correct course while driving
    if errorAngle > 20:
        print("Turn left")
        PD = 254
        #ArduinoSerial.write((254).to_bytes(1, 'big'))
    elif errorAngle < -20:
        print("Turn right")
        PD = 255
        #ArduinoSerial.write((255).to_bytes(1, 'big'))
    else:
        deriv = (errorAngle-errorAngleOldOld)/(2*deltaT)
        PD = kd * deriv + kp * errorAngle 
        #transform value to 0 to 200
        #thus 100 means straight, and above 100 is to left
        PD = 100 + 120*PD
        #check in range of unused values
        PD = max(PD,0)
        PD = min(PD,249)


    #if Arduino detect that it caught the cell
    if ArduinoSerial.in_waiting:
        if ArduinoSerial.readline().decode('utf-8') == 0:
            if len(coordMines)<3:
                coordMines.remove(coordMines[0])
            else:
                coordMines.remove(getClosestCell(goldC,560))
            #cellsChecked += 1
            timeLastCell = time.time()
    #or if has been looking for ages, pass to next
    if (time.time() - timeLastCell) > 30:
        if len(coordMines)<3:
            coordMines.remove(coordMines[0])
        else:
            coordMines.remove(getClosestCell(goldC,560))
        timeLastCell = time.time()
        #if cellsChecked < len(coordMines)-1:
        #    cellsChecked += 1


    #check if stuck to wall
    #251 go back and go right, 250 go left after
    if abs(alpha % 180 < 5) and (goldC[0] % 520 < 20):#530 means stuck, 10 also
        if (targetMine[1] > greenC[1]) ^ (goldC[0] > 530):#XOR
            PD = 251
        else:
            PD = 250
    #returning back to safe zone. Check whether arrived
    if len(coordMines)==2 and goldC[0] < 20 and abs(goldC[1] -270) < 20:
        PD = 253
    #returning back to start zone. Check whether arrived
    if len(coordMines) == 1 and abs(goldC[0]-15) < 15 and abs(goldC[1] -75) < 30:
        PD = 252
    #for development purposes be able to stop it remotely
    if keyboard.is_pressed('p'):
        PD = 252

    print("Value passed to Arduino")
    print(PD) 
    ArduinoSerial.write(round(PD).to_bytes(1, 'big'))

    time.sleep(0.1)

    deltaT = time.time()-timeOld
    timeOld = time.time()


    cv2.imshow('frame',frame)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q') or PD == 252:
      break

cap.release()
cv2.destroyAllWindows()
