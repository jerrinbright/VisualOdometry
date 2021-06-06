import numpy as np
import cv2

def preprocessing(b, frame):
    if (b == 1):
        kernel = np.ones((5,5),np.float32)/25
        frame = cv2.filter2D(frame,-1,kernel)
    
    if (b == 2):
        frame = cv2.GaussianBlur(frame,(5,5),0)
    
    if (b == 3):
        frame = cv2.bilateralFilter(frame,9,75,75)

    if (b == 4):
        frame = frame
    
    #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    
    return(frame)