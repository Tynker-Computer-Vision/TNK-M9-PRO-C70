import cv2
import math
from cvzone.HandTrackingModule import HandDetector

import pyautogui
import time
import numpy as np

### Variables Declaration
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 100            # Frame Rate
smoothening = 1         # Smoothening Factor

# Previous coordinates
prevX = 0
prevY = 0  

# Current coordinates
currX = 0
currY = 0  

screenshotNum = 1

screenSize = pyautogui.size()
screenWidth =screenSize[0]
screenHeight =screenSize[1]

# Capture the camera feed and set the resolution
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Creating object to detect hand 
detector = HandDetector(detectionCon=0.8)


# Loop to display video
while True:
    
    try:
        # Get a single capture from the camera
        readVideo = cap.read()
        check = readVideo[0]
        cameraFeedImg= readVideo[1]

        cameraFeedImg = cv2.flip(cameraFeedImg, 1)

        # Detect hand in cameraFeedImg
        handsDetector = detector.findHands(cameraFeedImg, flipType=False)
        hands = handsDetector[0]
        cameraFeedImg = handsDetector[1]
    
        if hands:
            # Hand 1
            hand1 = hands[0]
            lmList = hand1["lmList"]  # List of 21 Landmark points
            handType = hand1["type"]  # Handtype Left or Right
            fingers = detector.fingersUp(hand1)
            bbox = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint = hand1['center']  # center of the hand cx,cy
            
            
            if len(lmList)>0:
                indexFingerTipX = lmList[8][0]
                indexFingerTipY = lmList[8][1]

                # Checking if fingers are upwards
                print(fingers)
            
                if fingers[1] == 1 and fingers[2] == 0:     # If index finger is up and middle finger is down
                   
                    x3 = np.interp(indexFingerTipX, (frameR,width-frameR), (0,screenWidth))
                    y3 = np.interp(indexFingerTipY, (frameR, height-frameR), (0, screenHeight))

                    currX = prevX + (x3 - prevX)/smoothening
                    currY = prevY + (y3 - prevY) / smoothening

                    pyautogui.moveTo(currX, currY)    # Moving the cursor
                    cv2.circle(cameraFeedImg, (indexFingerTipX, indexFingerTipY), 7, (255, 0, 255), cv2.FILLED)
                    prevX, prevY = currX, currY

                if fingers[1] == 1 and fingers[2] == 1:     # If index finger & middle finger both are up
                    distance = math.dist(lmList[8], lmList[12])
                
                    indexFingerTipX = lmList[8][0]
                    indexFingerTipY = lmList[8][1]
                    middleFingerTipX = lmList[12][0]
                    middleFingerTipY = lmList[12][1]

                    # Get the center point of the two fingers
                    cx = (indexFingerTipX + middleFingerTipX) // 2 
                    cy = (indexFingerTipY + middleFingerTipY) // 2

                    cv2.line(cameraFeedImg, (indexFingerTipX, indexFingerTipY), (middleFingerTipX, middleFingerTipY), (255, 0, 255), 2)
                    
                    # If both fingers are really close to each other
                    if distance < 20:    
                        print(distance)
                        cv2.circle(cameraFeedImg, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()    # Perform Click

                 # Thumb is down and other fingers are down
                if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    screenshotPath = f'screenshots/screenshot_{screenshotNum}.png'
                    pyautogui.screenshot(screenshotPath)
                    screenshotNum += 1
                    print(f'Screenshot saved at {screenshotPath}')
                    time.sleep(1)

                # Thumb is down and other fingers are up
                if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    time.sleep(.1)
                    pyautogui.scroll(300)

                # Thumb is up and other fingers are down
                if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    time.sleep(.1)
                    pyautogui.scroll(-300)
    
               
    except Exception as e:
        print(e)


    # Show final image
    cv2.imshow("Image", cameraFeedImg)
    cv2.waitKey(1)