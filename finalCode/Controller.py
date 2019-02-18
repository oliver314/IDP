import time
import math
import sys


class Controller(object):
    # class to handle all control signals sent to the robot

    def __init__(self, img, tp, startZone, safeZone):
        # Initialising variables
        self.img = img
        self.tp = tp
        self.errorAngles = [0, 0]
        self.timeOld = 0
        self.deltaT = 1
        self.mineCollectedCount = 0
        self.timeLastCell = time.time()
        self.startZone = startZone
        self.safeZone = safeZone
        self.minePassedCount = 0
        self.targetCoord = None

    def driveLoop(self, robotCoord, targetCoord):
        # Main driving loop
        self.targetCoord = targetCoord
        self.robotCoord = robotCoord
        controlSignal = self.controlLoop()
        self.tp.send(controlSignal)
        time.sleep(0.1)

    def controlLoop(self):
        # PD controller

        kd = 0.0001
        kp = 0.01

        # Determining error angle
        self.orientation = self.img.getOrientation(self.robotCoord)
        orientationRef = self.img.getReferenceAngle(self.robotCoord, self.targetCoord)
        self.errorAngles.append(orientationRef - self.orientation)
        errorAngles = self.errorAngles[-3:]

        PD = 0
        e = errorAngles[-1]

        # turn sharply if error angle is more than 10 degrees
        if e < -10 and e > -350:
            PD = 254

        elif e > 10 and e < 350:
            PD = 255

        else:
            deriv = (errorAngles[-1] - errorAngles[-3]) / (2 * self.deltaT)
            if e > 20:
                e = 360 - e
            if e < -20:
                e = -360 - e
            PD = kd * deriv - kp * e

            # transform value to 0 to 250
            # thus 125 means straight, and above 125 is to left
            PD = 125 + 130 * PD

            # check in range of unused values
            PD = max(PD, 0)
            PD = min(PD, 249)

        # Recalibrate time step
        self.deltaT = time.time() - self.timeOld
        self.timeOld = time.time()

        if self.atTargetCoord():
            PD = 125

        return int(round(PD))

    def checkMineCaptured(self):
        # check to see if a mine has been captured and remove it from the list of coordinates

        # Check for response from robot
        val = self.tp.read()

        # if has been looking for more than 20s, pass to next
        if (time.time() - self.timeLastCell) > 20 and self.targetCoord not in [(517, 440), (535, 80)]:
            print('Failed to collect fuel cell in time')
            self.timeLastCell = time.time()
            self.img.removeMine(self.robotCoord)

        elif val is not None:
            self.img.removeMine(self.robotCoord)
            print("Message from Arduino: " + str(val))
            if val == 0:
                print('Collected fuel cell')
                self.mineCollectedCount += 1

            elif val == 1:
                print('Evaded radioactive cell')

            self.timeLastCell = time.time()

    def atTargetCoord(self):
        # Determines whether robot is within acceptable error margin of target coordinates

        error = 20  # acceptable error margin

        # takes purple part as center
        if math.sqrt((self.robotCoord[0][0] - self.targetCoord[0]) ** 2 + (
                    self.robotCoord[0][1] - self.targetCoord[1]) ** 2) < error:

            if self.targetCoord == self.safeZone:
                print("Dropping off mine")

                # rotate 180 degrees
                self.tp.send(255)
                while abs(self.img.getOrientation(self.robotCoord)) > 5:
                    self.robotCoord = self.img.getRobotCoordinates(self.targetCoord)
                    time.sleep(0.05)

                # trigger drop-off routine
                self.tp.send(253)
                time.sleep(0.1)
                self.mineCollectedCount = 0

            elif self.targetCoord == self.startZone:
                # poweroff routine
                self.tp.send(252)
                time.sleep(1)
                self.img.shutdown()
                sys.exit(0)
            return True

        else:
            return False

    def wallCells(self):
        # drive forward to collide with end wall
        targetCoord = (535, 80)
        
        xR = 0
        while xR < 535:
            robotCoord = self.img.getRobotCoordinates(targetCoord)
            self.driveLoop(robotCoord, targetCoord)
            self.checkMineCaptured()
            xR = robotCoord[0][0]

        # Rotate to align with wall
        self.tp.send(251)

        # the x value is tuned so that we drive parallel to the wall at exactly the right distance
        targetCoord = (517, 440)
        self.targetCoord = targetCoord

        while robotCoord[1][1] < 440:
            # drive towards target coordinates (therefore picking up cells en route) until y coordinate limit reached
            robotCoord = self.img.getRobotCoordinates(targetCoord)
            self.driveLoop(robotCoord, targetCoord)
            self.checkMineCaptured()

        print('Finished collecting wall cells')

        # U turn
        self.tp.send(250)
        time.sleep(3.5)
        # drive straight to re-enter camera visible zone
        self.tp.send(125)
        time.sleep(3)
