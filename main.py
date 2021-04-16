import numpy as np
import cv2
import argparse
import time
import csv

parser = argparse.ArgumentParser(description='Parse the video file and Extractor')
parser.add_argument('video', type=str, help='path to video file')
parser.add_argument('extractor', type=str, help='extractor')
parser.add_argument('smoothening', type=str, help='smoothening')
parser.add_argument('descriptor', type=str, help='descriptor')
args = parser.parse_args()

a = 0
font = cv2.FONT_HERSHEY_PLAIN
i = 0
maxf = 2000
minf = 0
maxt = 2000
mint = 0
prev_frame = 0
matches = []
GOOD_MATCH_PERCENT = 0.15

if(args.extractor == 'ORB'):
    print('Executing ORB feature extractor')
    a = 1
if(args.extractor == 'SURF'):
    print('Executing SURF feature extractor')
    a = 2
if(args.extractor == 'SIFT'):
    print('Executing SIFT feature extractor')
    a = 3

if(args.smoothening == 'Filter2D'):
    print('Executing Filter2D prepocessing')
    b = 1
if(args.smoothening == 'GaussianBlur'):
    print('Executing GaussianBlur prepocessing')
    b = 2
if(args.smoothening == 'bilateralFilter'):
    print('Executing bilateralFilter prepocessing')
    b = 3

if(args.descriptor == 'BFMatcher'):
    print('Executing BFMatcher')
    c = 1
if(args.descriptor == 'FLANN'):
    print('Executing FLANN')
    c = 2

cap = cv2.VideoCapture(args.video)
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
size = (frame_width, frame_height) 

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if (b == 1):    
        kernel = np.ones((5,5),np.float32)/25
        frame = cv2.filter2D(frame,-1,kernel)
    
    if (b == 2):
        frame = cv2.GaussianBlur(frame,(5,5),0)
    
    if (b == 3):
        frame = cv2.bilateralFilter(frame,9,75,75)
    
    #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    start_time = time.time()
    fps = cap.get(cv2.CAP_PROP_FPS)
    i = i + 1
    if ret == True:       
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if (a == 1):
            filename = "orb.csv"
            orb = cv2.ORB_create(nfeatures=1500)
            key_points, description = orb.detectAndCompute(img, None)
            frame_keypoints = cv2.drawKeypoints(img, key_points, img, flags=0)
            cv2.putText(frame_keypoints, "ORB-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            result = cv2.VideoWriter('orb.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
        
        if (a == 2):
            filename = "surf.csv"
            surf = cv2.xfeatures2d.SURF_create()
            key_points, description = surf.detectAndCompute(img,None)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "SURF-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            result = cv2.VideoWriter('surf.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
        
        if (a == 3):
            filename = "sift.csv"
            sift = cv2.xfeatures2d.SIFT_create()
            key_points, description = sift.detectAndCompute(img,None)
            frame_keypoints = cv2.drawKeypoints(img, key_points, None)
            cv2.putText(frame_keypoints, "SIFT-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(key_points), 2)), (10, 50), font, 2, (0, 0, 0), 2)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            result = cv2.VideoWriter('sift.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 

        nos = [i, len(key_points)]
        result.write(frame_keypoints)

    cv2.imshow('frame',frame_keypoints)        
    
    if (i >1):
        if (c == 1):
            matches = bf.match(description,prev_description)
            matches = sorted(matches, key = lambda x:x.distance)
            numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
            best_matches = matches[:numGoodMatches]

        if (c == 2) and (a != 1):
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks=50)   # or pass empty dictionary
            flann = cv2.FlannBasedMatcher(index_params,search_params)
            matches = flann.knnMatch(description,prev_description,k=2)
            matchesMask = [[0,0] for i in range(len(matches))]
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    matchesMask[i]=[1,0]

        if (c == 2) and (a == 1):
            search_params = dict(checks=100)
            index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=2)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(description, prev_description, k=2)
            matchesMask = [[0,0] for i in range(len(matches))]
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    matchesMask[i]=[1,0]

    prev_frame = img#cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    prev_key_point = key_points
    prev_description = description

    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(nos)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
result.release()
cv2.destroyAllWindows()
