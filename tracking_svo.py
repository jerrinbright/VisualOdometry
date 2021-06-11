import cv2

#Tracking of the features using Kanade-Lucas Tomasi Optical flow
def featureTracking(img_1, img_2, p1, world_points):
    lk_params = dict( winSize  = (21,21), maxLevel = 3, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
    p2, st, err = cv2.calcOpticalFlowPyrLK(img_1, img_2, p1, None, **lk_params)
    st = st.reshape(st.shape[0])
    pre = p1[st==1]
    p2 = p2[st==1]
    w_points  = world_points[st==1]
    return w_points, pre,p2