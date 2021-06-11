import numpy as np
import cv2

font = cv2.FONT_HERSHEY_PLAIN

def detector(a, frame):
        img = frame#cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     
        if (a == 1):
            filename = "orb.csv"
            orb = cv2.ORB_create(nfeatures=1500)
            key_points = orb.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, img, flags=0)
            cv2.putText(frame_keypoints, "ORB-FPS: " +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            pose = "orb.txt" 
        
        if (a == 2):
            filename = "surf.csv"
            surf = cv2.xfeatures2d.SURF_create()
            key_points = surf.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "SURF-FPS: " +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            pose = "surf.txt"
        
        if (a == 3):
            filename = "sift.csv"
            sift = cv2.xfeatures2d.SIFT_create()
            key_points = sift.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "SIFT-FPS: " +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            pose = "sift.txt"

        if (a == 4):
            filename = "kaze.csv"
            kaze = cv2.KAZE_create()
            key_points = kaze.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "KAZE-FPS: " +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            pose = "kaze.txt"

        if (a == 5):
            filename = "akaze.csv"
            akaze = cv2.AKAZE_create()
            key_points = akaze.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "AKAZE-FPS: " +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            pose = "akaze.txt"

        if (a == 6):
            filename = "brisk.csv"
            brisk = cv2.BRISK_create()
            key_points = brisk.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "BRISK-FPS: " +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            pose = "brisk.txt"

        return (key_points, bf, pose)