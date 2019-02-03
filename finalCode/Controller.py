import time
import keyboard

class Controller(object):
    def __init__(self, img, tp):
        # Initialising variables
        self.img = img
        self.tp = tp
        self.errorAngles = [0, 0]
        self.timeOld = 0
        self.deltaT = 1
        self.mineCount = 0
        self.timeLastCell = time.time()

    def driveLoop(self, targetCoord):
        # Main driving loop
        self.targetCoord = targetCoord
        frame = self.img.capture()
        self.img.showFrame(frame)
        self.robotCoord = self.img.getCoordinates(frame)
        controlSignal = self.controlLoop(frame)
        self.tp.send(controlSignal)
        time.sleep(0.1)

        # for development purposes be able to stop it remotely
        if keyboard.is_pressed('p'):
            PD = 252

    def controlLoop(self, frame):
        kd = 0.0001
        kp = 0.01

        # Determining error angle
        self.orientation = self.img.getOrientation(self.robotCoord)
        orientationRef = self.img.getReferenceAngle(frame, self.robotCoord, self.targetCoord)
        self.errorAngles.append(orientationRef - self.orientation)
        errorAngles = self.errorAngles[-3:]

        # PD controller
        PD = 0
        # makes no sense to try and correct course while driving
        if errorAngles[-1] > 20:
            # print("Turn left")
            PD = 254
        elif errorAngles[-1] < -20:
            # print("Turn right")
            PD = 255
        else:
            deriv = (errorAngles[-1] - errorAngles[-3]) / (2 * self.deltaT)
            PD = kd * deriv + kp * errorAngles[-1]
            # transform value to 0 to 200
            # thus 100 means straight, and above 100 is to left
            PD = 100 + 120 * PD
            # check in range of unused values
            PD = max(PD, 0)
            PD = min(PD, 249)

        # Recalibrate time step
        self.deltaT = time.time() - self.timeOld
        self.timeOld = time.time()

        # Check if robot has collided with arena wall
        wallCheck = self.checkWall()
        if wallCheck != None:
            PD = wallCheck

        return int(round(PD))

    def mineCaptured(self):
        # Check for response from robot
        if self.tp.read() == 0:
            print('Collected fuel cell')
            self.img.updateArena()
            self.timeLastCell = time.time()
            self.mineCount += 1
            return True

        # or if has been looking for ages, pass to next
        elif (time.time() - self.timeLastCell) > 30:
            print('Failed to collect fuel cell in time')
            self.img.updateArena()
            self.timeLastCell = time.time()
            return True

        else:
            return False

    def checkWall(self):
        # check if stuck to wall
        # 251 go back and go right, 250 go left after
        if abs(self.orientation % 180 < 5) and (self.robotCoord[0][0] % 520 < 20):  # 530 means stuck, 10 also
            if (self.targetCoord[1] > self.robotCoord[1][1]) ^ (self.robotCoord[0][0] > 530):  # XOR
                return 251
            else:
                return 250
        else:
            return None

    def atTargetCoord(self):
        error = 20  # acceptable error margin
        # returning back to safe zone. Check whether arrived
        if abs(self.robotCoord[0][0] - self.targetCoord[0]) < error and abs(
                        self.robotCoord[0][1] - self.targetCoord[1]) < error:
            return True
        else:
            return False
