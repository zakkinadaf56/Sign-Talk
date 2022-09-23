import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
from cvzone.ClassificationModule import Classifier
import tensorflow


cam=cv.VideoCapture(0)
detector=HandDetector(maxHands=1)
classifier=Classifier("Model/keras_model.h5","Model/label.txt")

offset=20
imgSize=300

folder="data/C"
counter=0
labels=["A","B","C"]

while True:
    success,img=cam.read()
    hands,img=detector.findHands(img)
    if hands:
        hand=hands[0]
        x,y,w,h=hand['bbox']
        imgWhite=np.ones((imgSize,imgSize,3),np.uint8)*255   #uint8--Unsigned integers of 8 bits

        imgCrop=img[y-offset:y+h+offset,x-offset:x+w+offset]
        imgCropShape=imgCrop.shape


        aspectRatio=h/w
        if aspectRatio>1:
            k=imgSize/h
            wCal=math.ceil(k*w)   #ceil-to round off the decimal
            imgResize=cv.resize(imgCrop,(wCal,imgSize))
            imgResizeShape=imgResize.shape
            wGap=math.ceil((imgSize-wCal)/2)
            imgWhite[0:imgResizeShape[0],wGap:wCal+wGap]=imgResize
            prediction,index=classifier.getPrediction(img)
            print(prediction,index)

        else:
            k=imgSize/w
            hCal=math.ceil(k*h)   #ceil-to round off the decimal
            imgResize=cv.resize(imgCrop,(imgSize,hCal))
            imgResizeShape=imgResize.shape
            hGap=math.ceil((imgSize-hCal)/2)
            imgWhite[hGap:hCal+hGap,0:imgResizeShape[1]]=imgResize


        cv.imshow("cropped",imgCrop)
        cv.imshow("White",imgWhite)


    cv.imshow("Image",img)
    cv.waitKey(1)
     

