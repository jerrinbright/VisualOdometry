import numpy as np
import cv2
import time
import csv

import detector
import parse
import preprocess
import matcher
import descriptors

i = 0
prev_frame = 0

a, b, c, d, args = parse.parse()

cap = cv2.VideoCapture(args.video)
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
size = (frame_width, frame_height) 

while(cap.isOpened()):
    ret, frame = cap.read()
    
    frame = preprocess.preprocessing(b, frame)
    
    start_time = time.time()
    fps = cap.get(cv2.CAP_PROP_FPS)
    i = i + 1
    if ret == True:       
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        frame_keypoints, bf, result, key_points, img, filename, pose = detector.detector(a, frame, fps, size)
        description = descriptors.descriptor(d, frame, fps, size)

        nos = [i, len(key_points)]
        result.write(frame_keypoints)

    cv2.imshow('frame',frame_keypoints)        
    
    if (i >1):
        matcher.matching(a, c, bf, description, prev_description)

    prev_frame = img
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