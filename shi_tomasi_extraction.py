import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import time
import csv

dataset_path = "C:/Users/jerri/OneDrive/Desktop/Personal/Interships/A2A/FEATURES"
cap = cv2.VideoCapture(os.path.join(dataset_path, 'vid/dji.mp4'))

frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
iframe = 0;
tof = 0;
maxf = 2000
minf = 0
maxt = 2000
mint = 0
font = cv2.FONT_HERSHEY_PLAIN

size = (frame_width, frame_height) 
   
result = cv2.VideoWriter('vid/shi_tomasi1500.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
filename = "csv/shi-tomasi/shi-tomasioutdoor1500.csv"

while(cap.isOpened()):
    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    start_time = time.time()
    iframe = iframe + 1
    if ret == True:       
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        tpf = (time.time() - start_time)
        corners = cv2.goodFeaturesToTrack(gray,1500,0.01,10)
        corners = np.int0(corners)
        nof = 0
        for i in corners:
            x,y = i.ravel()
            cv2.circle(frame,(x,y),3,255,-1)
            nof = nof + 1; #number of features
            tof = tof + 1; #total number of features

        cv2.putText(frame, "SHI-TOMASI" +"  Features="+ str(round(nof, 2)), (10, 50), font, 2, (0, 0, 255), 2)
        print(iframe, nof, tof, fps, tpf)
        nos = [iframe,nof, tof, fps, tpf]
        #with open(filename, 'a') as f:
        #    writer = csv.writer(f)
        #    writer.writerow(nos)

        result.write(frame)
        
        if (maxf > nof):
            maxf = nof
        elif (minf < nof):
            minf = nof
        if (maxt > tpf):
            maxt = tpf
        elif (mint < tpf):
            mint = tpf

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    prev_frame = frame

print(maxf, minf, maxt, mint)
#GRAY- 258 960 0.0 0.008996725082397461
#GRAY- 258 700 0.0 0.006989240646362305
#GRAY- 100 100 0.0 0.005015134811401367

cap.release()
result.release()
cv2.destroyAllWindows()