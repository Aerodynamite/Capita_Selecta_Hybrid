import cv2
import numpy as np

rectangleReady= False
corner1Selected= False
rectangle= None

def appendRectangle(val1, val2):
    global rectangle
    rectangle.append(val1)
    rectangle.append(val2)

def setRectangleReady(val):
    global rectangleReady
    rectangleReady= val

def setRectangle(val):
    global rectangle
    rectangle= val
    
def setCorner1Selected(val):
    global corner1Selected
    corner1Selected= val
    
def onmouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if(corner1Selected):
            appendRectangle(x, y)
            setRectangleReady(True)
            setCorner1Selected(False)
        else:
            setRectangle([x, y])
            setCorner1Selected(True)
            setRectangleReady(False)

cap = cv2.VideoCapture(0)
cv2.namedWindow('frame',1)
cv2.setMouseCallback('frame', onmouse)

while(1):

    # Take each frame
    _, frame = cap.read()
    if(rectangleReady):
        cv2.rectangle(frame,(rectangle[0],rectangle[1]),(rectangle[2],rectangle[3]), (255,0,0) ,3)
        
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([10,190,170], dtype=np.uint8)
    upper_blue = np.array([25,255,255], dtype=np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('frame',frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
