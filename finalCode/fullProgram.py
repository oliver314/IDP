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
startTime = time.time()

if __name__ == "__main__":
    img = Imaging(lg, ug, lp, up, lc, uc)
    tp = Transfer('com5')  # Create transfer protocol object
    ctrl = Controller(img, tp)
    print("Completed initialisation, press space to start")

    # start on space
    while not keyboard.is_pressed(' '):
        pass

    while img.cap.isOpened():
        frame = img.capture()
        img.showFrame(frame)
        robotCoord = img.getCoordinates(frame)

        if time.time() - startTime > 270:
            targetCoord = (15, 75)

        elif ctrl.mineCount > 3:
            targetCoord = (0, 270)

        else:
            targetCoord = img.getClosestCell(robotCoord)
            while not ctrl.mineCaptured():  # May be worth modifying this such that the robot drives forward when within a certain range
                ctrl.driveLoop(targetCoord)
            continue

        while not ctrl.atTargetCoord():
            ctrl.driveLoop(targetCoord)

    img.shutdown()

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