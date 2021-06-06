import numpy as np
import cv2

#feature tracking 
def featureTracking(img_1, img_2, p1):
    #basic parameter definition
    lk_params = dict( winSize  = (21,21), maxLevel = 3, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
    #finding current frame features from the previous frame features using Optical Flow instead of using Matching technique
    p2, st, err = cv2.calcOpticalFlowPyrLK(img_1, img_2, p1, None, **lk_params)
    st = st.reshape(st.shape[0])
    ##finding good matches only
    p1 = p1[st==1]
    p2 = p2[st==1]
    #returning the good matches
    return p1,p2