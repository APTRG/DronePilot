#!/usr/bin/env python

"""vision.py: Computer vision algorithms and functions needed in the DronePilot ecosystem."""

""" Color tracking algorithm from https://github.com/alduxvm/rpi-opencv """

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2015 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

import numpy as np
import cv2
import time


class ColorTracker:

    """Class initialization"""
    def __init__(self, targetColor):
        self.position = {'color':targetColor,'found':False,'x':0,'y':0,'elapsed':0.0}
        self.cam = cv2.VideoCapture(0)

    def findColor(self):
        while True:
            t1 = time.time()
            ret, frame = self.cam.read()

            hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            if self.position['color'] is 'red':
                color = cv2.inRange(hsv,np.array([0,150,0]),np.array([5,255,255]))
            elif self.position['color'] is 'blue':
                color=cv2.inRange(hsv,np.array([100,50,50]),np.array([140,255,255]))
            elif self.position['color'] is 'green':
                color=cv2.inRange(hsv,np.array([40,50,50]),np.array([80,255,255]))
            else: # white is default
                sensitivity = 10
                color = cv2.inRange(hsv,np.array([0,0,255-sensitivity]),np.array([255,sensitivity,255]))
            # Change to select color
            image_mask=color

            element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
            image_mask = cv2.erode(image_mask,element, iterations=2)
            image_mask = cv2.dilate(image_mask,element,iterations=2)
            image_mask = cv2.erode(image_mask,element)

            contours, hierarchy = cv2.findContours(image_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            maximumArea = 0
            bestContour = None
            for contour in contours:
                currentArea = cv2.contourArea(contour)
                if currentArea > maximumArea:
                    bestContour = contour
                    maximumArea = currentArea
            #Create a bounding box around the biggest color object
            if bestContour is not None:
                x,y,w,h = cv2.boundingRect(bestContour)
                cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
                t2 = time.time()
                self.position['found']=True
                self.position['x']=x
                self.position['y']=y
                self.position['elapsed']=round(t2-t1,3)
                #print "detection time = %gs x=%d,y=%d" % ( round(t2-t1,3) , x, y)
            else:
                self.position['found']=False

            #output=cv2.bitwise_and(frame,frame,mask=image_mask)
            #cv2.imshow('Original',frame)

            if cv2.waitKey(1) == 27:
                break

