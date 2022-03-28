# encoding=utf8
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import os
import cv2
import numpy as np

image = cv2.imread("./img/pruebis.jpg")
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
array_alpha = np.array([0.8])
array_beta = np.array([-100.0])
cv2.add(image, array_beta, image)       
cv2.multiply(image, array_alpha, image)
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
thresh = cv2.threshold(blurred, 130,200, cv2.THRESH_BINARY)[1]
cv2.imshow("thresh", thresh)
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
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 255, 255), 2)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
cv2.destroyAllWindows()
os.remove('./img/pruebis.jpg')