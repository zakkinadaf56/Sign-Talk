from operator import and_
import cv2 as cv
import os
import time
import handtracking as htm
import math
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
import numpy as np

Wcam,Hcam=640,480

cam=cv.VideoCapture(0)
cam.set(3,Wcam)
cam.set(4,Hcam)
pTime=0

detector=htm.handDetector(dectCon=0.75)

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]

vol=0
volBar=400
volPer=0


tipIds=[4,8,12,16,20]


while True:
    success,img=cam.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    # print(lmList)

    if len(lmList)!=0:

        

        if lmList[20][2]>lmList[18][2] and lmList[4][1]<lmList[3][1] and lmList[8][2]<lmList[6][2] and lmList[12][2]<lmList[10][2] and lmList[16][2]<lmList[14][2]  :
            # print("Showing Weather")
            cv.putText(img,f'Showing weather',(40,450),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
        
        # elif lmList[4][1]<lmList[3][1]  and lmList[8][2]>lmList[6][2] and lmList[12][2]>lmList[10][2] and lmList[16][2]>lmList[14][2] and lmList[20][2]<lmList[18][2] :
        #     print("Showing ip address of your device") 
        
        # elif lmList[20][2]>lmList[18][2] and lmList[16][2]<lmList[14][2] and lmList[12][2]<lmList[10][2] and lmList[8][2]<lmList[6][2] and lmList[4][1]<lmList[3][1] and  lmList[18][2] < lmList[19][2]:
        #     print("Switching window")
        
        # elif lmList[4][1] > lmList[3][1]  and lmList[8][2] < lmList[7][2] and lmList[10][2] < lmList[12][2] and lmList[14][2] < lmList[15][2] and lmList[18][2] < lmList[19][2] and lmList[5][1] < lmList[10][1]:
        #     print("Showing news.")
        
        # elif lmList[4][2]<lmList[2][2] and lmList[8][2]>lmList[6][2] and lmList[12][2]>lmList[10][2] and lmList[16][2]>lmList[14][2] and lmList[20][2]>lmList[18][2] :
        #     print('Location')
        elif (lmList[4][1] < lmList[3][1] and lmList[8][2] > lmList[5][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[19][2]) or(lmList[4][1] > lmList[3][1] and lmList[8][2] > lmList[5][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[19][2] < lmList[18][2]):
            # print("Showing ip address of your device")
            cv.putText(img,f'Showing IP Address',(40,450),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

        elif (lmList[4][1] < lmList[3][1] and lmList[8][2] < lmList[7][2] < lmList[6][2] and lmList[10][2] < lmList[12][2] and lmList[14][2] < lmList[15][2] and lmList[18][2] < lmList[19][2] and lmList[5][1] < lmList[10][1]) or (lmList[4][1] > lmList[3][1] and lmList and lmList[8][2] < lmList[7][2] < lmList[6][2] and lmList[10][2] < lmList[12][2] and lmList[14][2] < lmList[15][2] and lmList[18][2] < lmList[19][2] and lmList[5][1] < lmList[10][1]):
            # print("Showing news.")
            cv.putText(img,f'Showing News %',(40,450),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

        elif (lmList[4][2] < lmList[3][2] < lmList[2][2] < lmList[1][2] < lmList[0][2] and lmList[5][1] > lmList[7][1] > lmList[6][1] and lmList[9][1] > lmList[11][1] > lmList[10][1] and lmList[17][1] > lmList[19][1] > lmList[18][1]) or (lmList[4][2] < lmList[3][2] < lmList[2][2] < lmList[1][2] < lmList[0][2] and lmList[5][1] < lmList[7][1] < lmList[6][1] and lmList[9][1] < lmList[11][1] < lmList[10][1] and lmList[17][1] < lmList[19][1] < lmList[18][1]):
            # print("Showing location.")
            cv.putText(img,f'Showing location',(40,450),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv.putText(img,f'FPS: {int(fps)}',(40,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv.imshow("Image",img)
    cv.waitKey(1)