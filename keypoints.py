import numpy as np
import cv2

import duplicates
import parse
import detector
import descriptors
import matcher
import preprocess

a, d, c, b, args = parse.parse()

#Extraction of features and matching using FLANN
def extract_keypoints(img1, img2, K, baseline, refPoints = None):

    img1 = preprocess.preprocessing(b, img1)
    img2 = preprocess.preprocessing(b, img2)
    
    kp1, bf, pose = detector.detector(a, img1)
    kp2, bf, pose = detector.detector(a, img2)

    desc1 = descriptors.descriptor(d, img1)
    desc2 = descriptors.descriptor(d, img2)

    matches = matcher.matching(a, c, bf, desc1, desc2)

    match_points1, match_points2 = [], []
    # As per Lowe's ratio test to filter good matches
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            match_points1.append(kp1[m.queryIdx].pt)
            match_points2.append(kp2[m.trainIdx].pt)
    #Removing Duplicate features after Lowe's test
    p1 = np.array(match_points1).astype(float)
    p2 = np.array(match_points2).astype(float)
    if refPoints is not None:
        mask = duplicates.removeDuplicate(p1, refPoints)
        p1 = p1[mask,:]
        p2 = p2[mask,:]
    print(len(match_points1), len(p1))

    M_left = K.dot(np.hstack((np.eye(3), np.zeros((3,1)))))
    M_rght = K.dot(np.hstack((np.eye(3), np.array([[-baseline,0, 0]]).T)))
    p1_flip = np.vstack((p1.T,np.ones((1,p1.shape[0]))))
    p2_flip = np.vstack((p2.T,np.ones((1,p2.shape[0]))))
    
    P = cv2.triangulatePoints(M_left, M_rght, p1_flip[:2], p2_flip[:2]) 
    P = P/P[3]
    land_points = P[:3]
    
    return land_points.T, p1