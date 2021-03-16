#importing neccesary libraries
import numpy as np
import cv2
import os
import time
import csv

#directory in which all the relavent codes are located
dataset_path = "C:/Users/jerri/OneDrive/Desktop/Personal/Interships/A2A/VSLAM"
#video link in the directory mentioned above
cap = cv2.VideoCapture(os.path.join(dataset_path, 'vid/dji.mp4'))
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
MIN_MATCHES = 50
   
#rewritten frames are written here after each and every iterations
result = cv2.VideoWriter('orb.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
#the directory for storing the data collected from each frame
filename = "orb.csv"

while(cap.isOpened()):
	#taking one frame per iteration
    ret, frame = cap.read()
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
    
    #checking from 2nd frame because the first frame doesnt have a previous frame to compute
    if (i > 1 and i < 305):
        search_params = dict(checks=100)
        index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=2)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(description, prev_description, k=2)

        # As per Lowe's ratio test to filter good matches
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        if len(good_matches) > MIN_MATCHES:
            src_points = np.float32([key_points[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_points = np.float32([prev_key_point[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            m, mask = cv2.findHomography(src_points, dst_points, cv2.RANSAC, 5.0)
            corrected_img = cv2.warpPerspective(img, m, (prev_frame.shape[1], prev_frame.shape[0]))

            #declaring an array of values to be printed in the CSV file
            nos = [i, len(key_points), len(matches), len(good_matches), tpf]
            #writing of the data in the CSV file as mentioned above in the 'nos' variable
            with open(filename, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(nos)
            #writng the frame with features into the video
            result.write(frame_keypoints)   

        print(i, len(key_points), len(matches), len(good_matches), tpf)

    #storing of the current frame into a variable so that it can be used as prev frame when matching is done
    prev_frame = img
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