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
prevX = 0
prevY = 0  # Previous coordinates
currX = 0
currY = 0  # Current coordinates
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
        success, cameraFeedImg = cap.read()
        cameraFeedImg = cv2.flip(cameraFeedImg, 1)

        # Detect hand in cameraFeedImg
        hands, cameraFeedImg = detector.findHands(cameraFeedImg, flipType=False)
    
        if hands:
            # Hand 1
            hand1 = hands[0]
            lmList = hand1["lmList"]  # List of 21 Landmark points
            bbox = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint = hand1['center']  # center of the hand cx,cy
            handType = hand1["type"]  # Handtype Left or Right
            fingers = detector.fingersUp(hand1)
            
            if len(lmList)>0:
                x1 = lmList[8][0]
                y1 = lmList[8][1]

                # Checking if fingers are upwards
                print(fingers)
            
                if fingers[1] == 1 and fingers[2] == 0:     # If fore finger is up and middle finger is down
                   
                    x3 = np.interp(x1, (frameR,width-frameR), (0,screenWidth))
                    y3 = np.interp(y1, (frameR, height-frameR), (0, screenHeight))

                    currX = prevX + (x3 - prevX)/smoothening
                    currY = prevY + (y3 - prevY) / smoothening

                    pyautogui.moveTo(currX, currY)    # Moving the cursor
                    cv2.circle(cameraFeedImg, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
                    prevX, prevY = currX, currY

                if fingers[1] == 1 and fingers[2] == 1:     # If fore finger & middle finger both are up
                    length = math.dist(lmList[8], lmList[12])
 
                    x1 = lmList[8][0]
                    y1 = lmList[8][1]
                    x2 = lmList[12][0]
                    y2 = lmList[12][1]
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                    cv2.line(cameraFeedImg, (x1, y1), (x2, y2), (255, 0, 255), 2)

                    if length < 20:     # If both fingers are really close to each other
                        print(length)
                        cv2.circle(cameraFeedImg, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()    # Perform Click


                if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    # Thumb is down and other fingers are down
                    screenshotPath = f'screenshots/screenshot_{screenshotNum}.png'
                    pyautogui.screenshot(screenshotPath)
                    screenshotNum += 1
                    print(f'Screenshot saved at {screenshotPath}')
                    time.sleep(1)


                if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    # Thumb is down and other fingers are up
                    # putText(mode = 'U', loc=(200, 455), color = (0, 255, 0))
                    time.sleep(.1)
                    pyautogui.scroll(300)

                if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    # Thumb is up and other fingers are down
                    # putText(mode = 'U', loc=(200, 455), color = (0, 255, 0))
                    time.sleep(.1)
                    pyautogui.scroll(-300)
    
               
    except Exception as e:
        print(e)


    # Show final image
    cv2.imshow("Image", cameraFeedImg)
    cv2.waitKey(1)