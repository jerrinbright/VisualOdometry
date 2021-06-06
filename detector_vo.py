import numpy as np
import cv2

def detector(a):   
    if (a == 1):
        filename = "orb.csv"
        detector = cv2.ORB_create(nfeatures=1500)
        pose = "orb.txt" 
        
    if (a == 2):
        filename = "surf.csv"
        detector = cv2.xfeatures2d.SURF_create()
        pose = "surf.txt"
        
    if (a == 3):
        filename = "sift.csv"
        detector = cv2.xfeatures2d.SIFT_create()
        pose = "sift.txt"

    if (a == 4):
        filename = "kaze.csv"
        detector = cv2.KAZE_create()
        pose = "kaze.txt"

    if (a == 5):
        filename = "akaze.csv"
        detector = cv2.AKAZE_create()
        pose = "akaze.txt"

    if (a == 6):
        filename = "brisk.csv"
        detector = cv2.BRISK_create()
        pose = "brisk.txt"

    return (detector, filename, pose)