import cv2
import numpy as np
import math
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
print("Imports done")
cap = cv2.VideoCapture(1)
print("Capture started")
time.sleep(2)  # wait for 2 secounds for the communication to get established

# define range of green color in HSV
#use gimp for color code: 160, 20, 73 for green robot
#212,81,66 for blue robot
#area +- 1100
#208,66,87 for cells or 208,63,88
#area +- 70 - 260
#172,80,60 for save zone
#values light on(light off is more accurate, values in ColorDetectionPicture.py)

firstTime = True
coordMines=[]
cellsChecked = 0
errorAngle = 0
errorAngleOld = 0
errorAngleOldOld = 0
timeOld = 0
deltaT = 1
kd = 0.01
kp = 0.01

count = 0
while(1):
    # Take each frame
    _, frame = cap.read()
    #1080*1920*3
    frame = frame[0:480, 0:560]
    cv2.circle(frame,(0,275), 10, (0,0,255), -1)
    cv2.circle(frame,(30,60), 10, (0,0,255), -1)
    

    cv2.imshow('frame',frame)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
