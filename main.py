import numpy as np
import cv2
import timeit
import csv

import tracking
import dataset
import detector_vo
import parser_vo
import preprocess

# PARSING PHASES OF VO
a, b, args = parser_vo.parse()

#initialization
ground_truth = dataset.getTruePose()
img_1 = dataset.getImages(0)
img_2 = dataset.getImages(1)

#conversion of RGB frames to Grayscale
if len(img_1) == 3:
    gray_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    gray_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
else:
    gray_1 = img_1
    gray_2 = img_2

img_1 = preprocess.preprocessing(b, img_1) 
img_2 = preprocess.preprocessing(b, img_2) 

#EXTRACTION + DESCRIPTION
detector, filename, pose = detector_vo.detector(a)
kp1 = detector.detect(img_1)
p1 = np.array([ele.pt for ele in kp1],dtype='float32')
#calculating the features of frame i+1 using Optical flow
p1, p2   = tracking.featureTracking(gray_1, gray_2, p1)

#Camera parameters
fc = 718.8560
pp = (607.1928, 185.2157)
K  = dataset.getK()
font = cv2.FONT_HERSHEY_PLAIN

#RANSAC and essential matrix is found
E, mask = cv2.findEssentialMat(p2, p1, fc, pp, cv2.RANSAC,0.999,1.0); 
_, R, t, mask = cv2.recoverPose(E, p2, p1,focal=fc, pp = pp)

#initialize some parameters
MAX_FRAME     = 4540
MIN_NUM_FEAT  = 1500
preFeature = p2
preImage   = gray_2
R_f = R
t_f = t

start = timeit.default_timer()
traj = np.zeros((600, 600, 3), dtype=np.uint8)
maxError = 0

for numFrame in range(2, MAX_FRAME):

    if (len(preFeature) < MIN_NUM_FEAT):
        feature = detector.detect(preImage)
        preFeature = np.array([ele.pt for ele in feature],dtype='float32')
    curImage_c = dataset.getImages(numFrame)

    if len(curImage_c) == 3:
          curImage = cv2.cvtColor(curImage_c, cv2.COLOR_BGR2GRAY)
    else:
          curImage = curImage_c
    
    kp1 = detector.detect(curImage)
    preFeature, curFeature = tracking.featureTracking(preImage, curImage, preFeature)

    E, mask = cv2.findEssentialMat(curFeature, preFeature, fc, pp, cv2.RANSAC,0.999,1.0)
    _, R, t, mask = cv2.recoverPose(E, curFeature, preFeature, focal=fc, pp = pp)
    
    truth_x, truth_y, truth_z, absolute_scale = dataset.getAbsoluteScale(ground_truth, numFrame)

    if absolute_scale > 0.1:  
        t_f = t_f + absolute_scale*R_f.dot(t)
        R_f = R.dot(R_f)
    preImage = curImage
    preFeature = curFeature

    rt = [R_f[0][0],R_f[0][1],R_f[0][2],float(t_f[0]),R_f[1][0],R_f[1][1],R_f[1][2],float(t_f[1]),R_f[2][0],R_f[2][1],R_f[2][2],float(t_f[2])]
    draw_x, draw_y = int(t_f[0])+300, int(t_f[2]) + 100
    draw_tx, draw_ty = int(truth_x)+300, int(truth_z) + 100
    curError = np.sqrt((t_f[0]-truth_x)**2 + (t_f[1]-truth_y)**2 + (t_f[2]-truth_z)**2)

    if (curError > maxError):
        maxError = curError

    cv2.circle(traj, (draw_x, draw_y) ,1, (0,0,255), 2)
    cv2.circle(traj, (draw_tx, draw_ty) ,1, (255,0,0), 2)
    cv2.rectangle(traj, (10, 30), (550, 50), (0,0,0), cv2.FILLED)
    text = "Coordinates: x ={0:02f}m y = {1:02f}m z = {2:02f}m".format(round(float(t_f[0]),2), round(float(t_f[1]),2), round(float(t_f[2]),2))
    cv2.putText(traj, text, (10,50), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)
    cv2.imshow( "Trajectory", traj )

    [a] = curError
    nos = [numFrame, a, len(curFeature), len(preFeature), t_f[0], t_f[1], t_f[2]]

    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(nos)
    with open(pose, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(rt)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

stop = timeit.default_timer()
cv2.imwrite('result/trajectory.png', traj)
cv2.destroyAllWindows()