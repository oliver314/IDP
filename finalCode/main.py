# Import required libraries
import numpy as np
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
startZone = (30, 20)
safeZone = (90, 270)

'''
TODO

if detects mine and is 45 degree scew: runs into wall indefinetely

start with open field or handle mine in way at start correctly

'''


if __name__ == "__main__":
    img = Imaging(lg, ug, lp, up, lc, uc)  # Initialise imaging class
    tp = Transfer('com5')  # Initialise transfer protocol class
    print("Completed initialisation, press space to start")

    # start on space
    while not keyboard.is_pressed(' '):
        pass

    img.updateArena()
    ctrl = Controller(img, tp, startZone, safeZone)  # Initialise controller class
    startTime = time.time()

    ctrl.wallCells()
    while img.cap.isOpened() and (not keyboard.is_pressed('q')):
        robotCoord = img.getRobotCoordinates(ctrl.targetCoord)
        if (ctrl.mineCollectedCount > 7) or (ctrl.mineCollectedCount>0 and len(img.coordMines) == 0) or time.time() - startTime > 300:
            print(str(ctrl.mineCollectedCount) + " " + str(len(img.coordMines))+" " + str(time.time()-startTime))
            targetCoord = safeZone

        elif (ctrl.mineCollectedCount == 0 and time.time() - startTime > 300) or len(img.coordMines)==0:
            targetCoord = startZone

        else:
            targetCoord, dist = img.getClosestCell(robotCoord)
            # check whether mine captured this turn and remove it from list if so
            ctrl.checkMineCaptured()

        #print(targetCoord)
        ctrl.driveLoop(robotCoord, targetCoord)

    # shutdown motors
    tp.send(252)
    time.sleep(1)
    # shutdown OpenCV
    img.shutdown()
