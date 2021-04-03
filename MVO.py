import numpy as np
import cv2
import timeit
import csv

#sift- 869.40s, max error- 318.23 
#fast- 246.79s, total error- 298.23
#surf- 738.30s, total error- 219.80

#returning the absolute scale 
def getAbsoluteScale(f, frame_id):
      #acquiring the previous frame ground truth from the KITTI dataset
      x_pre, y_pre, z_pre = f[frame_id-1][3], f[frame_id-1][7], f[frame_id-1][11]
      #acquiring the current frame ground truth from the KITTI dataset
      x    , y    , z     = f[frame_id][3], f[frame_id][7], f[frame_id][11]
      #finding the root mean square (RMS) error that's the scaling factor
      scale = np.sqrt((x-x_pre)**2 + (y-y_pre)**2 + (z-z_pre)**2)
      #returning the calculated scaling factor value
      return x, y, z, scale

#feature tracking 
def featureTracking(img_1, img_2, p1):
    #basic parameter definition
    lk_params = dict( winSize  = (21,21), maxLevel = 3, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
    #finding current frame features from the previous frame features using Optical Flow instead of using Matching technique
    p2, st, err = cv2.calcOpticalFlowPyrLK(img_1, img_2, p1, None, **lk_params)
    st = st.reshape(st.shape[0])
    ##finding good matches only
    p1 = p1[st==1]
    p2 = p2[st==1]
    #returning the good matches
    return p1,p2

#feature detection
def featureDetection():
    #setting the thresholds
    thresh = dict(threshold=25, nonmaxSuppression=True);
    #defining FAST based feature extraction technique
    fast = cv2.FastFeatureDetector_create(**thresh)
    #returning the fast extractors
    return fast

#Ground truth from KITTI dataset
def getTruePose():
    file = '00.txt'
    return np.genfromtxt(file, delimiter=' ',dtype=None)

#Frames of Left camera from KITTI dataset 
def getImages(i):
    return cv2.imread('image_1/{0:06d}.png'.format(i), 0)

#Declaring the camera parameters
def getK():
    return   np.array([[7.188560000000e+02, 0, 6.071928000000e+02], [0, 7.188560000000e+02, 1.852157000000e+02], [0, 0, 1]])

#initialization
ground_truth =getTruePose()
#taking in a frame i
img_1 = getImages(0)
#taking in frame i+1
img_2 = getImages(1)
#conversion of RGB frames to Grayscale
if len(img_1) == 3:
    #conversion of frame i to grayscale
    gray_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    #conversion of frame i+1 to grayscale
    gray_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
#if already in Grayscale
else:
    #copy frame i simply to gray_1
    gray_1 = img_1
    #copy frame i+1 simply to gray_2
    gray_2 = img_2

# Resolutions for the video
size = img_1.shape[:2]
frame_width = size[1]
frame_height = size[0]
size = (frame_width, frame_height)

#printing the frame to the video
res_vid = cv2.VideoWriter('vid_fast.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
res_traj = cv2.VideoWriter('traj_fast.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)

#CSV to save the data
filename = "mvo_fast.csv"

#find the detector
detector = featureDetection()
#storing the features from fast of frame i
kp1      = detector.detect(img_1)
p1       = np.array([ele.pt for ele in kp1],dtype='float32')
#calculating the features of frame i+1 using Optical flow
p1, p2   = featureTracking(gray_1, gray_2, p1)

#Camera parameters
fc = 718.8560
pp = (607.1928, 185.2157)
K  = getK()
font = cv2.FONT_HERSHEY_PLAIN

#RANSAC and essential matrix is found
E, mask = cv2.findEssentialMat(p2, p1, fc, pp, cv2.RANSAC,0.999,1.0); 
#finding the Rotational and Translational Vectors using the Essentiak matrics and camera parameters 
_, R, t, mask = cv2.recoverPose(E, p2, p1,focal=fc, pp = pp);

#initialize some parameters
MAX_FRAME     = 4540
MIN_NUM_FEAT  = 1500
preFeature = p2
preImage   = gray_2
R_f = R
t_f = t

#start the timer to calculate the total execution time
start = timeit.default_timer()
#interface to display the trajectory
traj = np.zeros((600, 600, 3), dtype=np.uint8)
maxError = 0

#play image sequences
for numFrame in range(2, MAX_FRAME):
    #printing the frame number
    print(numFrame)
    #condition to do extraction again if the number of features less than a particular value
    if (len(preFeature) < MIN_NUM_FEAT):
        feature   = detector.detect(preImage)
        preFeature = np.array([ele.pt for ele in feature],dtype='float32')
    curImage_c = getImages(numFrame)
    #checking if the frame is Grayscale else convert from RGB to grayscale
    if len(curImage_c) == 3:
          curImage = cv2.cvtColor(currImage_c, cv2.COLOR_BGR2GRAY)
    else:
          curImage = curImage_c
    
    #storing the current frame features 
    kp1 = detector.detect(curImage);
    #doing matching using Optical flow
    preFeature, curFeature = featureTracking(preImage, curImage, preFeature)
    #RANSAC and essential matrix is found
    E, mask = cv2.findEssentialMat(curFeature, preFeature, fc, pp, cv2.RANSAC,0.999,1.0); 
    #finding the Rotational and Translational Vectors using the Essentiak matrics and camera parameters 
    _, R, t, mask = cv2.recoverPose(E, curFeature, preFeature, focal=fc, pp = pp);
    #absolute scale is computed and called here
    truth_x, truth_y, truth_z, absolute_scale = getAbsoluteScale(ground_truth, numFrame)
    #finding the world co-ordinates of the rotational and translational vectors 
    if absolute_scale > 0.1:  
        t_f = t_f + absolute_scale*R_f.dot(t)
        R_f = R.dot(R_f)
    #storing previous frame into a dummy
    preImage = curImage
    #storing previous frame features into a dummy
    preFeature = curFeature

    #Visualization of the trajectory
    #estimated pose is initialized
    draw_x, draw_y = int(t_f[0])+300, int(t_f[2]) + 100;
    #true pose is initialized
    draw_tx, draw_ty = int(truth_x)+300, int(truth_z) + 100
    #current error using the previous and current pose is calculated using RMSE
    curError = np.sqrt((t_f[0]-truth_x)**2 + (t_f[1]-truth_y)**2 + (t_f[2]-truth_z)**2)
    #printing the current error
    print('Current Error: ', curError)
    #printing the maximum error into a dynamic dummy variable
    if (curError > maxError):
        maxError = curError
    #drawing the estimated pose into the trajectory interface
    cv2.circle(traj, (draw_x, draw_y) ,1, (0,0,255), 2);
    #drawing the ground pose into the trajectory interface
    cv2.circle(traj, (draw_tx, draw_ty) ,1, (255,0,0), 2);
    #drawing rectangle to display the camera co-ordinates
    cv2.rectangle(traj, (10, 30), (550, 50), (0,0,0), cv2.FILLED);
    #initializing the x,y,z of the camera to be printed
    text = "Coordinates: x ={0:02f}m y = {1:02f}m z = {2:02f}m".format(round(float(t_f[0]),2), round(float(t_f[1]),2), round(float(t_f[2]),2));
    #printing the co-ordinates in the trajectory interface
    cv2.putText(traj, text, (10,50), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8);
    #showing the results of the trajectory interface
    res_traj.write(traj)
    cv2.imshow( "Trajectory", traj );
    #parameters to be displayed in csv
    [a] = curError
    nos = [numFrame, a, len(curFeature), len(preFeature), t_f[0], t_f[1], t_f[2]]
    #writing of the data in the CSV file as mentioned above in the 'nos' variable
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(nos)
    f_img = cv2.drawKeypoints(curImage, kp1, curImage, flags=0)
    cv2.putText(f_img, "FAST" +" Frame: "+ str(numFrame)+ "  Features="+ str(round(len(curFeature), 2)), (10, 50), font, 2, (0, 0, 255), 3)
	#res_vid.write(f_img)
    cv2.imshow("Result", f_img);
    #shortcut to terminate the code in mid-wa
    k = cv2.waitKey(1) & 0xFF
    #ESC key to terminate the trjectory interface
    if k == 27:
        break

#printing the maximum error
print('Maximum Error: ', maxError)
#saving the map/ trajectory image 
cv2.imwrite('map_fast.png', traj);
#stoping the timer
stop = timeit.default_timer()
#printing the total time of execution
print(stop - start)
#destroying the memory thereby saving space
cv2.destroyAllWindows()
