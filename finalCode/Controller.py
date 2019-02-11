import time
import math


class Controller(object):
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

    def driveLoop(self, robotCoord, targetCoord):
        # Main driving loop
        self.targetCoord = targetCoord
        self.robotCoord = robotCoord
        controlSignal = self.controlLoop()
        self.tp.send(controlSignal)
        time.sleep(0.1)

    def controlLoop(self):
        kd = 0.0001
        kp = 0.01

        # Determining error angle
        self.orientation = self.img.getOrientation(self.robotCoord)
        orientationRef = self.img.getReferenceAngle(self.robotCoord, self.targetCoord)
        self.errorAngles.append(orientationRef - self.orientation)
        errorAngles = self.errorAngles[-3:]

        # PD controller
        PD = 0
        e = errorAngles[-1]
        #print(e)
        # makes no sense to try and correct course while driving
        if e < -10 and e > -350:
            # print("Turn left")
            PD = 254
        elif e > 10 and e < 350:
            # print("Turn right")
            PD = 255

        else:
            deriv = (errorAngles[-1] - errorAngles[-3]) / (2 * self.deltaT)
            if e > 20:
                e = 360 - e
            if e < -20:
                e = -360 - e
            PD = kd * deriv - kp * e
            # transform value to 0 to 200
            # thus 100 means straight, and above 100 is to left
            PD = 125 + 130 * PD
            # check in range of unused values
            PD = max(PD, 0)
            PD = min(PD, 249)

        # Recalibrate time step
        self.deltaT = time.time() - self.timeOld
        self.timeOld = time.time()

        if self.atTargetCoord():
            PD = 100

        return int(round(PD))

    def checkMineCaptured(self):
        # Check for response from robot
        val = self.tp.read()

        # if has been looking for ages, pass to next
        if (time.time() - self.timeLastCell) > 30:
            print('Failed to collect fuel cell in time')
            self.timeLastCell = time.time()
            self.img.removeMine(self.targetCoord)

        elif val is not None:
            self.img.removeMine(self.targetCoord)
            print("Message from Arduino: " + str(val))
            if val == 0:
                print('Collected fuel cell')
                self.mineCollectedCount += 1
                self.minePassedCount += 1

            elif val == 1:
                print('Evaded radioactive cell')
                self.mineCollectedCount += 1

            self.timeLastCell = time.time()

    def atTargetCoord(self):
        # Determines whether robot is within acceptable error margin of target coordinates
        error = 20  # acceptable error margin
        # returning back to safe zone. Check whether arrived
        # takes purple part as center
        if math.sqrt((self.robotCoord[0][0] - self.targetCoord[0]) ** 2 + (
                    self.robotCoord[0][1] - self.targetCoord[1]) ** 2) < error:
            if self.targetCoord == self.safeZone:
                print("Dropping off mine")
                time.sleep(2)
                self.tp.send(255)
                while abs(self.img.getOrientation(self.robotCoord)) > 5:
                    self.robotCoord = self.img.getRobotCoordinates()
                    # print(abs(self.img.getOrientation(self.robotCoord)))
                    time.sleep(0.05)
                self.tp.send(253)
                time.sleep(0.1)

                self.mineCollectedCount = 0
            elif self.targetCoord == self.startZone:
                self.tp.send(252)
                time.sleep(300)
            return True
        else:
            return False

    def wallCells(self):
        targetCoord = (535,80)
        val = self.tp.read()
        while val != 2:
            robotCoord = self.img.getRobotCoordinates()
            self.driveLoop(robotCoord, targetCoord)
            val = self.tp.read()
            print(val)
        self.tp.send(251)
        targetCoord = self.img.getClosestCell(robotCoord, rightLimit=600, leftLimit=500)
        targetCoord = (targetCoord[0] - 10, targetCoord[1])
        while self.mineCollectedCount == 0: # May need to change
            robotCoord = self.img.getRobotCoordinates()
            self.driveLoop(robotCoord, targetCoord)
            self.checkMineCaptured()

        while self.mineCollectedCount < 5:
            targetCoord = self.img.getClosestCell(robotCoord, rightLimit=600, leftLimit=500)
            targetCoord = (targetCoord[0] - 10, targetCoord[1])
            robotCoord = self.img.getRobotCoordinates()
            self.driveLoop(robotCoord, targetCoord)
            self.checkMineCaptured()

            while self.img.getOrientation(self.robotCoord) + 90 > 5:
                # TURN RIGHT
                self.tp.send(100)
                self.robotCoord = self.img.getRobotCoordinates()
                print(abs(self.img.getOrientation(self.robotCoord)))
                time.sleep(0.05)

            while self.img.getOrientation(self.robotCoord) + 90 < -5:
                # TURN LEFT
                self.tp.send(150)
                self.robotCoord = self.img.getRobotCoordinates()
                print(abs(self.img.getOrientation(self.robotCoord)))
                time.sleep(0.05)


