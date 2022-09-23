'''
Title : To detect hand in webcam and finding a particuler point of plam.
Author: Mohd Raza Shaikh
date  : 29 of August, 2022.
'''
import cv2 as cv
import mediapipe as mp
import time


class handDetector():
    '''This class is useful if you want to track your hand in webcam'''
    def __init__(self, mode = False, maxHands = 2,complx=0, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complx = complx
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.complx,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        '''This method is used for finding hand in camera.'''
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)   #this will print the coordinates of each point of palm.
    
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
                
        return img

    def findPosition(self,img,handNo=0,draw=True):
        '''This method is created for finding position of a point of palm.'''
        """
        img - This is for image.
        handNo - This is for Number of hands.
        draw - This is for whether you want to darw circles around each points or not.
        """
        lmList = [] #This is for storing landmarks
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                #print(id,lms)   # This wil print the point number and its coordinates.
                h, w, c = img.shape
                # h,w and c are for riz. height,width and channel.
                cx, cy = int(lm.x * w), int(lm.y * h)   # cx,cy are coordinates of points in pixcel
                # print(id,cx,cy)
                lmList.append([id,cx,cy])
                if draw:
                    cv.circle(img,(cx,cy),6,(255,0,0),cv.FILLED)
                    # Here you can change the size and color of circle maked on every points.
                
        return lmList



def main():
# ==============================================================================================
# You have to add this block of codes in your program if you want to use this module.
    pTime = 0   # previous time
    cTime = 0   # current time

    cap = cv.VideoCapture(2)

    detector = handDetector()
    point_no = int(input('enter the point number which you want to track:'))
    while True:
        success, img = cap.read()
        
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[point_no])

        
        cTime = time.time()
        fps = 1//(cTime-pTime)
        pTime = cTime

        cv.putText(img,"fps:"+str(fps),(10,50),cv.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
        # if img1:
        cv.imshow("images",img)
            # break
        cv.waitKey(1)
# ==============================================================================================

if __name__ == '__main__':
    main()



# Time : 43:48