# Import required libraries
import numpy as np
import time
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

# main code
if __name__ == "__main__":
    img = Imaging(lg, ug, lp, up, lc, uc)  # Initialise imaging class
    tp = Transfer('com3')  # Initialise transfer protocol class
    print("Completed initialisation, press space to start")

    # start on space
    while not keyboard.is_pressed(' '):
        pass

    img.updateArena()  # Generate array of target mine coordinates
    ctrl = Controller(img, tp, startZone, safeZone)  # Initialise controller class
    startTime = time.time()

    # run subroutine for collection of cells by the rear wall
    ctrl.wallCells()

    # main loop to collect remaining cells and return to the safe zone
    while img.cap.isOpened() and (not keyboard.is_pressed('q')):

        # update robot coordinates
        robotCoord = img.getRobotCoordinates(ctrl.targetCoord)

        # Return to safe zone condition
        if (ctrl.mineCollectedCount > 8) or (ctrl.mineCollectedCount>0 and len(img.coordMines) == 0) or time.time() - startTime > 300:
            targetCoord = safeZone

        # return to start zone condition
        elif (ctrl.mineCollectedCount == 0 and time.time() - startTime > 300) or len(img.coordMines) == 0:
            targetCoord = startZone

        else:
            # set target coordinates to closest cell
            targetCoord, dist = img.getClosestCell(robotCoord)

            # check whether mine captured this turn and remove it from list if so
            ctrl.checkMineCaptured()

        # run subroutine to determine and send drive commands to the robot
        ctrl.driveLoop(robotCoord, targetCoord)

    # shutdown motors
    tp.send(252)
    time.sleep(1)

    # shutdown OpenCV
    img.shutdown()
