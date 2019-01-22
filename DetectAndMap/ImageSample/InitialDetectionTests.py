print("Hello World")
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread('test.jpg',0)
edges = cv.Canny(img,100,200)
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()

'''
# Converts images from BGR to HSV 
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV) 
lower_red = np.array([110,50,50]) 
upper_red = np.array([130,255,255]) 
# Here we are defining range of bluecolor in HSV 
# This creates a mask of blue coloured  
# objects found in the frame. 
mask = cv.inRange(hsv, lower_red, upper_red) 
  
# The bitwise and of the frame and mask is done so  
# that only the blue coloured objects are highlighted  
# and stored in res 
res = cv.bitwise_and(frame,frame, mask= mask) 
cv.imshow('frame',frame) 
cv.imshow('mask',mask) 
cv.imshow('res',res) 
  
# This displays the frame, mask  
# and res which we created in 3 separate windows. 
k = cv.waitKey(5) & 0xFF
  
# Destroys all of the HighGUI windows. 
cv.destroyAllWindows() '''