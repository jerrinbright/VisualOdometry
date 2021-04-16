import numpy as np
import cv2
import argparse
import time
import csv

parser = argparse.ArgumentParser(description='Parse the video file and Extractor')
parser.add_argument('image', type=str, help='path to image file')
parser.add_argument('echo', type=str, help='extractor')
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

if(args.echo == 'ORB'):
	print('Executing ORB feature extractor')
	a = 1
elif(args.echo == 'SIFT'):
	print('Executing SIFT feature extractor')
	a = 2
elif(args.echo == 'SURF'):
	print('Executing SURF feature extractor')
	a = 3

cap = cv2.VideoCapture(args.image)
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
size = (frame_width, frame_height) 

result = cv2.VideoWriter('orb.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 

while(cap.isOpened()):
    ret, frame = cap.read()
        
    #kernel = np.ones((5,5),np.float32)/25
    #frame = cv2.filter2D(frame,-1,kernel)
    #frame = cv2.GaussianBlur(frame,(5,5),0)
    #frame = cv2.bilateralFilter(frame,9,75,75)
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
	    
	    if (a == 2):
	    	filename = "surf.csv"
	    	surf = cv2.xfeatures2d.SURF_create()
	    	keypoints, descriptors = surf.detectAndCompute(img,None)
		    frame_keypoints = cv2.drawKeypoints(img, keypoints, None)
		    cv2.putText(frame_keypoints, "SURF-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(keypoints), 2)), (10, 50), font, 2, (0, 0, 0), 2)
		
		if (a == 3):
			filename = "sift.csv"
			sift = cv2.xfeatures2d.SIFT_create()
			keypoints, descriptors = sift.detectAndCompute(img,None)
		    frame_keypoints = cv2.drawKeypoints(img, keypoints, None)
		    cv2.putText(frame_keypoints, "SIFT-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(len(keypoints), 2)), (10, 50), font, 2, (0, 0, 0), 2)

        nos = [i, len(key_points), fps, elapsed_time]
        result.write(frame_keypoints)

    cv2.imshow('frame',frame_keypoints)        
    
    if (i >1):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(description,prev_description)
        #matches = sorted(matches, key = lambda x:x.distance)
        numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
        best_matches = matches[:numGoodMatches]
        print(len(matches), len(best_matches))
    prev_frame = img#cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(nos)

    prev_key_point = key_points
    prev_description = description

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
result.release()
cv2.destroyAllWindows()