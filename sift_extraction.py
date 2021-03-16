import numpy as np
import cv2
import time
import csv

cap = cv2.VideoCapture("dji.mp4")
sift = cv2.xfeatures2d.SIFT_create()
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/vid/SIFT1500.avi', fourcc, 20.0, size)
font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
cont = True
frame_id= 0
rows = [] 
i = 0
prev_frame = 0
matches = []
filename = "/csv/sift/sift1500.csv"

while(cont):
    ret , img = cap.read()
    frame_id += 1
    i = i + 1
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img = cv2.resize(img,(320,240))
    keypoints, descriptors = sift.detectAndCompute(img,None)

    img = cv2.drawKeypoints(img, keypoints, None)
    x=len(keypoints)
    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv2.putText(img, "SIFT-FPS: " + str(round(fps, 2)) +"Nf="+ str(round(x, 2)), (10, 50), font, 2, (0, 0, 0), 2)
    #print(fps)
    cv2.imshow("Image", img)

    if (i >1):
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            #img2 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            key_points1, description1 = orb.detectAndCompute(prev_frame, None)
            matches = bf.match(description,description1)
            #matches = sorted(matches, key = lambda x:x.distance)
            print(len(matches))
        prev_frame = img

        nos = [i, len(matches)]
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(nos)
        #prev_frame = frame
        #prev_key_point = key_points
        #prev_description = description
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#print(maxf, minf, maxt, mint)

cap.release()
result.release()
cv2.destroyAllWindows()