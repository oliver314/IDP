# Import required libraries
import cv2
import numpy as np
import math
import time  # Required to use delay functions
import keyboard
from TransferProtocol import Transfer
from ImageProcessing import Imaging
from Controller import Controller

# Initialise variables


lg = np.array([70 / 2, 0 * 255 / 100, 50 * 255 / 100])
ug = np.array([135 / 2, 27 * 255 / 100, 92 * 255 / 100])
lp = np.array([320 / 2, 10 * 255 / 100, 70 * 255 / 100])
up = np.array([360 / 2, 60 * 255 / 100, 110 * 255 / 100])
lc = np.array([195 / 2, 30 * 255 / 100, 65 * 255 / 100])
uc = np.array([215 / 2, 80 * 255 / 100, 95 * 255 / 100])
startTime = time.time()
timeLastCell = time.time()
mineCount = 0



def mineCaptured():
    # Check for response from robot
    if tp.read() == 0:
        print('Collected fuel cell')
        image.updateArena()
        timeLastCell = time.time()
        mineCount += 1
        return True

    # or if has been looking for ages, pass to next
    elif (time.time() - timeLastCell) > 30:
        print('Failed to collect fuel cell in time')
        image.updateArena()
        timeLastCell = time.time()
        return True

    else:
        return False


while (cap.isOpened()):

    if firstTime:

        firstTime = False

    ''' NOT SURE WHAT THIS IS FOR
    if firstGo:
        rightLimit = 520
    else:
        rightLimit = 560
    
    if (len(coordMines) < 3):
        targetMine = coordMines[0]
    else:
        targetMine = getClosestCell(goldC, rightLimit)
    '''





    # if Arduino detect that it caught the cell



    # check if stuck to wall
    # 251 go back and go right, 250 go left after
    if abs(alpha % 180 < 5) and (goldC[0] % 520 < 20):  # 530 means stuck, 10 also
        if (targetMine[1] > greenC[1]) ^ (goldC[0] > 530):  # XOR
            PD = 251
        else:
            PD = 250
    # returning back to safe zone. Check whether arrived
    if len(coordMines) == 2 and goldC[0] < 20 and abs(goldC[1] - 270) < 20:
        PD = 253
    # returning back to start zone. Check whether arrived
    if len(coordMines) == 1 and abs(goldC[0] - 15) < 15 and abs(goldC[1] - 75) < 30:
        PD = 252
    # for development purposes be able to stop it remotely
    if keyboard.is_pressed('p'):
        PD = 252

    #print("Value passed to Arduino")
    #print(PD)




    cv2.imshow('frame', frame)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q') or PD == 252:
        break

cap.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    image = Imaging(lg,ug,lp,up,lc,uc)
    control = Controller(image)
    tp = Transfer('com5')  # Create transfer protocol object
    print("Capture started")

    # start on space
    while not keyboard.is_pressed(' '):
        pass

    while 1:
        frame = image.capture()
        robotCoord = image.getCoordinates(frame)
        if time.time() - startTime > 270:

        elif mineCount > 3:

        else:
            targetCoord = image.getClosestCell(robotCoord)
            while not mineCaptured(): # May be worth modifying this such that the robot drives forward when within a certain range
                robotCoord = image.getCoordinates(frame)
                controlSignal = control.controlLoop(frame, robotCoord, targetCoord)
                tp.send(controlSignal)
                time.sleep(0.1)

