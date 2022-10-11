import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
from cvzone.ClassificationModule import Classifier
import tensorflow


cam=cv.VideoCapture(0)
detector=HandDetector(maxHands=1)
classifier=Classifier("Model/keras_model.h5","Model/labels.txt")

offset=20
imgSize=300

folder="data/C"
counter=0
# labels=["A","B","C","D","E","F","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","G","H","1","3","4","5","7","8","10"]
labels=["ip","location","music","news","switchwindow","voldown","volup","weather","heart","end"]

while True:
    success,img=cam.read()
    imgOutput=img.copy()
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
            prediction,index=classifier.getPrediction(imgWhite,draw=False)
            print(prediction,index)

        else:
            k=imgSize/w
            hCal=math.ceil(k*h)   #ceil-to round off the decimal
            imgResize=cv.resize(imgCrop,(imgSize,hCal))
            imgResizeShape=imgResize.shape
            hGap=math.ceil((imgSize-hCal)/2)
            imgWhite[hGap:hCal+hGap,0:imgResizeShape[1]]=imgResize
            prediction,index=classifier.getPrediction(imgWhite,draw=False)


        # cv.rectangle(imgOutput,(x-offset,y-offset-50),(x-offset+90,y-offset-50+50),(255,0,255),cv.FILLED)
        cv.putText(imgOutput,labels[index],(x,y-25),cv.FONT_HERSHEY_COMPLEX,1.7,(255,0,255),2)
        cv.rectangle(imgOutput,(x-offset,y-offset),(x+w+offset,y+h+offset),(255,0,255),4)

        cv.imshow("cropped",imgCrop)
        cv.imshow("White",imgWhite)


    cv.imshow("Image",imgOutput)
    cv.waitKey(1)
     

