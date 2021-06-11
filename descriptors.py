import numpy as np
import cv2

def descriptor(d, frame):
    if (d == 1):
        orb = cv2.ORB_create(nfeatures=1500)
        descriptor = orb.compute(frame)
    if (d == 2):
        surf = cv2.xfeatures2d.SURF_create()
        descriptor = surf.compute(frame)
    if (d == 3):
        sift = cv2.xfeatures2d.SIFT_create()
        descriptor = sift.compute(frame)
    if (d == 4):
        brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
        descriptor = brief.compute(frame)
    if (d == 5):
        akaze = cv2.AKAZE_create()
        descriptor = akaze.compute(frame)
    if (d == 6):
        brisk = cv2.BRISK_create()
        descriptor = brisk.compute(frame)
    if (d == 7):
        kaze = cv2.KAZE_create()
        descriptor = kaze.compute(frame)
    
    return(descriptor)
