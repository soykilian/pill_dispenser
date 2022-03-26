# encoding=utf8
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2
import numpy as np
# construct the argument parse and parse the arguments
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread("./img/pastis4.jpg")
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
# convert the resized image to grayscale, blur it slightly,
# and threshold it
array_alpha = np.array([1.50])
array_beta = np.array([-120.0])
cv2.add(image, array_beta, image)       
cv2.multiply(image, array_alpha, image)
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
thresh = cv2.threshold(blurred, 130,200, cv2.THRESH_BINARY)[1]
# find contours in the thresholded image and initialize the
# shape detector
while (True):
    cv2.imshow('contrast', image)
    cv2.imshow('gray', gray)
    cv2.imshow('threshold', thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()
