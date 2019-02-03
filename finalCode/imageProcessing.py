# Import required libraries
import cv2
import numpy as np
import math


class Imaging(object):
    def __init__(self, lg, ug, lp, up, lc, uc):
        # Initialising colour boundaries
        self.lg = lg
        self.ug = ug
        self.lp = lp
        self.up = up
        self.lc = lc
        self.uc = uc

        self.coordMines = []

        # Initialise camera
        print('Initialising camera')
        self.cap = cv2.VideoCapture(1)
        print('Camera initialised')

        self.updateArena()

    def updateArena(self):
        # Determine coordinates of cells
        frame = self.capture()
        rectMines = self.detectColor(frame, minArea=5);
        for rect in rectMines:
            self.coordMines.append((rect[0] + rect[2] / 2, rect[1] + rect[3] / 2))

        # starts at lowest y and goes up, ie from top to bottom if image
        self.coordMines = sorted(self.coordMines, key=lambda x: (x[1], x[0]))

        print("Coordinates of cells")
        print(self.coordMines)

    def capture(self):
        _, frame = self.cap.read()
        frame = frame[0:480, 0:560]
        return frame

    def detectColor(self, frame, minArea=120):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only green colors
        mask = cv2.inRange(hsv, self.lc, self.uc)

        kernel = np.ones((5, 5), 'int')
        dilated = cv2.dilate(mask, kernel)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)
        ret, thrshed = cv2.threshold(cv2.cvtColor(res, cv2.COLOR_BGR2GRAY), 3, 255, cv2.THRESH_BINARY)
        contours, hier = cv2.findContours(thrshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        coord = []
        for cnt in contours:
            # Contour area is taken
            area = cv2.contourArea(cnt)
            if area > minArea:
                # draw rectangle around found zones
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                coord.append((x, y, w, h))

        return coord

    def getClosestCell(self, robotCoord, rightLimit=560):
        closest = 490000
        minMin = [0, 0]
        purpleC = robotCoord[0]
        for mine in self.coordMines:
            if (mine[0] > 50) and (mine[0] < rightLimit):
                dist = (mine[0] - purpleC[0]) ** 2 + (mine[1] - purpleC[1]) ** 2
                if dist < closest:
                    minMin = mine
                    closest = dist

        return minMin

    def getCoordinates(self, frame):
        purpleF = self.detectColor(frame)
        greenF = self.detectColor(frame)

        if len(purpleF) == 0 or len(greenF) == 0:
            print(str(len(purpleF)) + "  " + str(len(greenF)))
            ''' Save photo if several frames fail
            count % 5 == 0):
            cv2.imwrite("frame" + str(count/5)+ ".png", frame)
            count += 1 
            '''
            return None

        purpleF = purpleF[0]
        greenF = greenF[0]
        purpleC = (purpleF[0] + purpleF[2] / 2, purpleF[1] + purpleF[3] / 2)
        greenC = (greenF[0] + greenF[2] / 2, greenF[1] + greenF[3] / 2)

        return purpleC, greenC

    def getOrientation(self, robotCoord):
        purpleC, greenC = robotCoord
        # angle with respect to horizontal, positive as anticlockwise. Counterintuitive sign in expression bc y axis inverted
        return math.degrees(math.atan2(-purpleC[1] + greenC[1], purpleC[0] - greenC[0]))

    def getReferenceAngle(self, frame, robotCoord, targetCoord):
        purpleC, greenC = robotCoord
        cv2.circle(frame, (round(targetCoord[0]), round(targetCoord[1])), 10, (0, 0, 255), -1)
        return math.degrees(math.atan2(-targetCoord[1] + greenC[1], targetCoord[0] - greenC[0]))

    def showFrame(self, frame):
        cv2.imshow('frame', frame)

    def shutdown(self):
        self.cap.release()
        cv2.destroyAllWindows()
