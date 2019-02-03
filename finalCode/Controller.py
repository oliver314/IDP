import time

class Controller(object):
    def __init__(self,image):
        # Initialising variables
        self.errorAngles = [0, 0]
        self.timeOld = 0
        self.deltaT = 1
        self.image = image

    def controlLoop(self, frame, robotCoord, targetCoord):
        kd = 0.0001
        kp = 0.01

        # Determining error angle
        alpha = self.image.getOrientation(robotCoord)
        alphaRef = self.image.getReferenceAngle(frame, robotCoord, targetCoord)
        self.errorAngles.append(alphaRef - alpha)
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

        self.deltaT = time.time() - self.timeOld
        self.timeOld = time.time()
        return int(round(PD))