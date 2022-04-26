# encoding=utf8
from re import T
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import os
import cv2
import numpy as np
zoom_factor = 0.05 # 5% of the original image 
image = cv2.imread("/home/pi/pill_dispenser/serverPastillas/ke.jpg")
l=int(len(image)/8)
#image=image[3*l:7*l,l:4*l]
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
array_alpha = np.array([0.80])
array_beta = np.array([-90.0])
"""
cv2.add(resized, array_beta, resized)       
cv2.imshow("img", resized)
cv2.waitKey(0)
cv2.multiply(resized, array_alpha, resized)
cv2.imshow("luz", resized)
cv2.waitKey(0)
"""
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray", gray)
#cv2.waitKey(0)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
thresh = cv2.threshold(blurred, 125,160, cv2.THRESH_BINARY)[1]
cv2.imshow("thresh", thresh)
cv2.waitKey(0)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()
for c in cnts:
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    shape = sd.detect(c)
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
    cv2.putText(resized, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 255, 255), 2)
    cv2.imshow("Image", resized)
    cv2.waitKey(0)
cv2.destroyAllWindows()
#os.remove('./img/pruebis.jpg')
