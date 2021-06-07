import numpy as np
import cv2

font = cv2.FONT_HERSHEY_PLAIN

def detector(a, frame, fps, size):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     
        if (a == 1):
            filename = "orb.csv"
            orb = cv2.ORB_create(nfeatures=1500)
            key_points = orb.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, img, flags=0)
            cv2.putText(frame_keypoints, "ORB-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            result = cv2.VideoWriter('orb.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
            pose = "orb.txt" 
        
        if (a == 2):
            filename = "surf.csv"
            surf = cv2.xfeatures2d.SURF_create()
            key_points = surf.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "SURF-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            result = cv2.VideoWriter('surf.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
            pose = "surf.txt"
        
        if (a == 3):
            filename = "sift.csv"
            sift = cv2.xfeatures2d.SIFT_create()
            key_points = sift.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "SIFT-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            result = cv2.VideoWriter('sift.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
            pose = "sift.txt"

        if (a == 4):
            filename = "kaze.csv"
            kaze = cv2.KAZE_create()
            key_points = kaze.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "KAZE-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            result = cv2.VideoWriter('kaze.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
            pose = "kaze.txt"

        if (a == 5):
            filename = "akaze.csv"
            akaze = cv2.AKAZE_create()
            key_points = akaze.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "AKAZE-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            result = cv2.VideoWriter('akaze.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
            pose = "akaze.txt"

        if (a == 6):
            filename = "brisk.csv"
            brisk = cv2.BRISK_create()
            key_points = brisk.detect(img)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "BRISK-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            result = cv2.VideoWriter('brisk.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
            pose = "brisk.txt"

        result.write(frame_keypoints)

        return (frame_keypoints, bf, result, key_points, img, filename, pose)