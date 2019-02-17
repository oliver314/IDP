# Import required libraries
import cv2
import numpy as np
import math


class Imaging(object):
    # class to handle all functions related to image processing

    def __init__(self, lg, ug, lp, up, lc, uc):
        # Initialising colour boundaries
        self.lg = lg
        self.ug = ug
        self.lp = lp
        self.up = up
        self.lc = lc
        self.uc = uc

        # Initialising other variables
        self.coordMines = []
        self.count = 0

        # Initialise camera
        print('Initialising camera')
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)
        self.cap.set(cv2.CAP_PROP_CONTRAST, 128)
        self.cap.set(cv2.CAP_PROP_SATURATION, 128)
        print('Camera initialised')

    def updateArena(self):
        # Determine coordinates of cells

        frame = self.capture() # capture image
        rectMines = self.detectColor(frame, 'c', minArea=5)
        for rect in rectMines:
            # check whether mine too dangerous to go to since close to camera limit
            candidate = (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2)
            if candidate[1] < 450 and candidate[0] < 525 and candidate[
                1] > 20:
                self.coordMines.append(candidate)
                cv2.circle(frame, (round(candidate[0]), round(candidate[1])), 4, (0, 0, 255), -1)

        cv2.imwrite("frameCells.png", frame) # save initial frame

        # starts at lowest y and goes up, ie from top to bottom if image
        self.coordMines = sorted(self.coordMines, key=lambda x: (x[1], x[0]))

        print("Coordinates of cells")
        print(self.coordMines)

    def capture(self):
        # returns an OpenCV frame of the arena
        _, frame = self.cap.read()
        frame = frame[0:480, 0:560]
        return frame

    def detectColor(self, frame, key, minArea=120):
        # returns the coordinates of the colour specified by the key

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if key == 'c':
            # Threshold the HSV image to get only cell colours
            mask = cv2.inRange(hsv, self.lc, self.uc)
        elif key == 'g':
            # Threshold the HSV image to get only green colours
            mask = cv2.inRange(hsv, self.lg, self.ug)
        elif key == 'p':
            # Threshold the HSV image to get only purple colours
            mask = cv2.inRange(hsv, self.lp, self.up)

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

    def getClosestCell(self, robotCoord, rightLimit=520, leftLimit=50):
        # returns the coordinates of the closest cell to the robot

        # initialising variables
        closest = 490000
        minMine = [0, 0]
        purpleC = robotCoord[0]

        #
        for mine in self.coordMines:
            if (mine[0] > leftLimit) and (mine[0] < rightLimit):
                dist = (mine[0] - purpleC[0]) ** 2 + (mine[1] - purpleC[1]) ** 2
                if dist < closest:
                    minMine = mine
                    closest = dist

        # no mines in field left. Collect back ones now, start from bottom
        if closest == 490000:
            minMine = self.coordMines[-1]
        return minMine, closest

    def getRobotCoordinates(self, targetCoord, depth=0):
        if depth > 50:
            return (480, 540), (480, 520)

        # Returns coordinates of green and purple rectangles on robot
        frame = self.capture()
        purpleF = self.detectColor(frame, 'p')
        greenF = self.detectColor(frame, 'g')

        if targetCoord is not None:
            cv2.circle(frame, (round(targetCoord[0]), round(targetCoord[1])), 10, (0, 0, 255), -1)

        self.showFrame(frame)

        if len(purpleF) == 0 or len(greenF) == 0:
            # saveImage()
            # if at bottom and are facing north but can t see it assume it
            if len(purpleF) > 0:
                purpleF = purpleF[0]
                if purpleF[1] + purpleF[3] / 2 > 500:
                    purpleC = (purpleF[0] + purpleF[2] / 2, purpleF[1] + purpleF[3] / 2)
                    print("Assuming in deadzone with purple sticking out: " + purpleC)
                    return purpleC, (purpleC[0], purpleC[1] + 10)
            return self.getRobotCoordinates(targetCoord, depth=depth + 1)

        purpleF = purpleF[0]
        greenF = greenF[0]
        purpleC = (purpleF[0] + purpleF[2] / 2, purpleF[1] + purpleF[3] / 2)
        greenC = (greenF[0] + greenF[2] / 2, greenF[1] + greenF[3] / 2)

        return purpleC, greenC

    def getOrientation(self, robotCoord):
        purpleC, greenC = robotCoord
        # angle with respect to horizontal, positive as anticlockwise. Counterintuitive sign in expression bc y axis inverted
        return math.degrees(math.atan2(-purpleC[1] + greenC[1], purpleC[0] - greenC[0]))

    def getReferenceAngle(self, robotCoord, targetCoord):
        purpleC, greenC = robotCoord
        return math.degrees(math.atan2(-targetCoord[1] + greenC[1], targetCoord[0] - greenC[0]))

    def showFrame(self, frame):
        cv2.imshow('frame', frame)
        cv2.waitKey(25)

    # remove mine edited so that removes closest one if there is any
    def removeMine(self, robotCoord):
        cell, dist = self.getClosestCell(robotCoord)
        print("The distance to the closest cell is " + str(dist))
        # critical dist value to be adjusted
        if dist < 9000:
            self.coordMines.remove(cell)
        else:
            print("Tried to remove inexistent cell")

    def shutdown(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def saveImage(self):
        # Save photo if several frames fail
        if (self.count % 5 == 0):
            cv2.imwrite("frame" + str(self.count / 5) + ".png", frame)
            self.count += 1
