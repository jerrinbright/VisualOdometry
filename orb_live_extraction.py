#importing neccesary libraries
import numpy as np
import cv2
import os
import time
import csv

#directory in which all the relavent codes are located
#dataset_path = "C:/Users/jerri/OneDrive/Desktop/Personal/Interships/A2A/FEATURES"
#video link in the directory mentioned above
cap = cv2.VideoCapture('videos/live.mp4')
#display frame width and height
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
#font size of the features ditected to be put in the video
font = cv2.FONT_HERSHEY_PLAIN
#size of the above stored frame width and height
size = (frame_width, frame_height) 
#basic declaration of variables
i = 0
maxf = 2000
minf = 0
maxt = 2000
mint = 0
prev_frame = 0
matches = []
GOOD_MATCH_PERCENT = 0.15
   
#rewritten frames are written here after each and every iterations
result = cv2.VideoWriter('orb.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
#the directory for storing the data collected from each frame
filename = "orb.csv"

while(cap.isOpened()):
    #taking one frame per iteration
    ret, frame = cap.read()
        
    #kernel = np.ones((5,5),np.float32)/25
    #frame = cv2.filter2D(frame,-1,kernel)
    #frame = cv2.GaussianBlur(frame,(5,5),0)
    #frame = cv2.bilateralFilter(frame,9,75,75)
    #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    #starting time to find the time taken for feature detection in a particular frame
    start_time = time.time()
    #fps calculation
    fps = cap.get(cv2.CAP_PROP_FPS)
    #incrementing of a variable denoting the frame number
    i = i + 1
    #checking if a frame is present
    if ret == True:       
        #converitng the rgb image to grayscale
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# START OF FEATURE DETEECTION
        #calling orb detectors and assignign the number of features to be 1500
        orb = cv2.ORB_create(nfeatures=1500)
        #keypoint address and respective descriptors are stored after computing
        key_points, description = orb.detectAndCompute(img, None)
        #drawing keypoints in the frame
        frame_keypoints = cv2.drawKeypoints(img, key_points, img, flags=0)
        #finding the time of computing features in one frame
        tpf = (time.time() - start_time)
        #finding the total number of features from the start
        tf = i*len(key_points)
        #printing the number of feeatures into the frame to be displayed in the video
        cv2.putText(frame_keypoints, "ORB" +"  Features="+ str(round(len(key_points), 2)), (10, 50), font, 2, (255, 0, 0), 2)

        #declaring an array of values to be printed in the CSV file
        nos = [i,len(key_points), tf, fps, tpf]

        #writng the frame with features into the video
        result.write(frame_keypoints)
        
        #checking for the maximum and minimum number of features detected in the full video
        if (maxf > len(key_points)):
            maxf = len(key_points)
        elif (minf < len(key_points)):
            minf = len(key_points)

        #checking for the maximum and minimum number of total features in all the frames detected in the full video
        if (maxt > tpf):
            maxt = tpf
        elif (mint < tpf):
            mint = tpf

    #displauying the frame simultaneously when computing is done 
    cv2.imshow('frame',frame_keypoints)        
    
# STARTING MATCHING OF FEATURES
    
    #checking from 2nd frame because the first fram edoesnt have a previous frame to compute
    if (i >1):
        #initializing the BF matcher using NORM_HAMMING
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        #convertion of the previous frame into grayscale
        #img2 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        #finding the descriptors and keypoints of the previous frame 
        #key_points1, description1 = orb.detectAndCompute(prev_frame, None)

        #matching using the descriptors of both the current and preious frame
        matches = bf.match(description,prev_description)
        #matches = sorted(matches, key = lambda x:x.distance)

        numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
        best_matches = matches[:numGoodMatches]

        #printing the number of features matched from the extracted features in the earlier step
        print(len(matches), len(best_matches))
    #storing of the current frame into a variable so that it can be used as prev frame when matching is done
    prev_frame = img#cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    #writing of the data in the CSV file as mentioned above in the 'nos' variable
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(nos)

    prev_key_point = key_points
    prev_description = description

    #printing the frame number, number of features, frames per second and the total features detected till the frame 
    #print(i, len(key_points),tf, fps, tpf, matches)
    
    #will terminate the code if q is presssed or the frame limit is reached
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#printing the maximum, minimum number of total features in the video along with maximum and minimum features detected per frame
#print(maxf, minf, maxt, mint)

#clearing all the windows thereby saving memory
cap.release()
result.release()
cv2.destroyAllWindows()
