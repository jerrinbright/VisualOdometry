import numpy as np
import cv2
#import matplotlib.pyplot as plt

#fig = plt.figure()
#ax = plt.axes(projection='3d')
#Camera calibration parameters
def getK():
    return np.array([[7.188560000000e+02, 0, 6.071928000000e+02], [0, 7.188560000000e+02, 1.852157000000e+02], [0, 0, 1]])

#gGound truth taken from KITTI dataset
def getTruePose():
    file = 'C:/Users/jerri/OneDrive/Desktop/Personal/Interships/A2A/VSLAM/data_odometry_poses/dataset/poses/00.txt'
    return np.genfromtxt(file, delimiter=' ',dtype=None)

#Left camera frame from the stereo setup
def getLeftImage(i):
    return cv2.imread('C:/Users/jerri/OneDrive/Desktop/Personal/Interships/A2A/VSLAM/data_odometry_gray/dataset/sequences/00/image_0/{0:06d}.png'.format(i), 0)

#Right camera frame from the stereo setup
def getRightImage(i):
    return cv2.imread('C:/Users/jerri/OneDrive/Desktop/Personal/Interships/A2A/VSLAM/data_odometry_gray/dataset/sequences/00/image_1/{0:06d}.png'.format(i), 0)

#Remove duplicate points from new query points
def removeDuplicate(queryPoints, refPoints, radius=10):
    for i in range(len(queryPoints)):
        query = queryPoints[i]
        xliml, xlimh = query[0]-radius, query[0]+radius
        yliml, ylimh = query[1]-radius, query[1]+radius
        inside_x_lim_mask = (refPoints[:,0] > xliml) & (refPoints[:,0] < xlimh)
        curr_kps_in_x_lim = refPoints[inside_x_lim_mask]
        if curr_kps_in_x_lim.shape[0] != 0:
            inside_y_lim_mask = (curr_kps_in_x_lim[:,1] > yliml) & (curr_kps_in_x_lim[:,1] < ylimh)
            curr_kps_in_x_lim_and_y_lim = curr_kps_in_x_lim[inside_y_lim_mask,:]
            if curr_kps_in_x_lim_and_y_lim.shape[0] != 0:
                queryPoints[i] =  np.array([0,0])
    return (queryPoints[:, 0]  != 0 )

#Extraction of features and matching using FLANN
def extract_keypoints_orb(img1, img2, K, baseline, refPoints = None):
	#calling orb detectors and assignign the number of features to be 1500
    orb = cv2.ORB_create(nfeatures=500)
    #surf = cv2.xfeatures2d.SURF_create()
    #keypoint address and respective descriptors are stored after computing for left frame
    kp1, desc1 = orb.detectAndCompute(img1, None)
    #kp1, desc1 = surf.detectAndCompute(img1,None)
    #keypoint address and respective descriptors are stored after computing for right frame
    kp2, desc2 = orb.detectAndCompute(img2, None)
    #kp2, desc2 = surf.detectAndCompute(img2,None)
    #search parameters for FLANN
    search_params = dict(checks=100)
    #index parameters for FLANN
    index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=2)
    #Initializing FLANN based matching 
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    #Matching btw the left and right stereo camera
    matches = flann.knnMatch(desc1,desc2,k=2)
    match_points1, match_points2 = [], []
    # As per Lowe's ratio test to filter good matches
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            match_points1.append(kp1[m.queryIdx].pt)
            match_points2.append(kp2[m.trainIdx].pt)
    #Removing Duplicate features after Lowe's test
    p1 = np.array(match_points1).astype(float)
    p2 = np.array(match_points2).astype(float)
    if refPoints is not None:
        mask = removeDuplicate(p1, refPoints)
        p1 = p1[mask,:]
        p2 = p2[mask,:]
    print(len(match_points1), len(p1))
    M_left = K.dot(np.hstack((np.eye(3), np.zeros((3,1)))))
    M_rght = K.dot(np.hstack((np.eye(3), np.array([[-baseline,0, 0]]).T)))
    p1_flip = np.vstack((p1.T,np.ones((1,p1.shape[0]))))
    p2_flip = np.vstack((p2.T,np.ones((1,p2.shape[0]))))
    P = cv2.triangulatePoints(M_left, M_rght, p1_flip[:2], p2_flip[:2]) 
    P = P/P[3]
    land_points = P[:3]
    return land_points.T, p1

#Tracking of the features using Kanade-Lucas Tomasi Optical flow
def featureTracking(img_1, img_2, p1, world_points):
    lk_params = dict( winSize  = (21,21), maxLevel = 3, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
    p2, st, err = cv2.calcOpticalFlowPyrLK(img_1, img_2, p1, None, **lk_params)
    st = st.reshape(st.shape[0])
    pre = p1[st==1]
    p2 = p2[st==1]
    w_points  = world_points[st==1]
    return w_points, pre,p2

#pose estimation and visualization
def playImageSequence(left_img, right_img, K):
	#feature extraction and matching using FLANN
    points, p1 = extract_keypoints_orb(left_img, right_img, K, baseline)
    p1 = p1.astype('float32')
    z = 0
    pnp_objP = np.expand_dims(points, axis = 2)
    pnp_p1   = np.expand_dims(p1, axis = 2).astype(float)
    reference_img = left_img
    reference_2D  = p1
    landmark_3D   = points
    #storing the true pose values 
    truePose = getTruePose()
    #interface for displaying the trajectory
    traj = np.zeros((600, 600, 3), dtype=np.uint8);
    maxError = 0
    for i in range(0, 5000):
        print('image: ', i)
        curImage =  getLeftImage(i)
        #tracking the left frame features with the right frame
        landmark_3D, reference_2D, tracked_2Dpoints = featureTracking(reference_img, curImage, reference_2D,  landmark_3D)
        pnp_objP = np.expand_dims(landmark_3D, axis = 2)
        pnp_cur  = np.expand_dims(tracked_2Dpoints, axis = 2).astype(float)
        #finding the rotational and translational vectors using perspective-n-points
        _, rvec, tvec, inliers = cv2.solvePnPRansac(pnp_objP , pnp_cur, K, None)
        #update the new reference_2D
        reference_2D = tracked_2Dpoints[inliers[:,0],:]
        landmark_3D  = landmark_3D[inliers[:,0],:]            
        #retrieve the rotation matrix
        rot,_ = cv2.Rodrigues(rvec)
        #coordinate transformation, from camera to world
        tvec = -rot.T.dot(tvec)   
        #inverse transform
        inv_transform = np.hstack((rot.T,tvec)) 
        # the inlier ratio
        inliers_ratio = len(inliers)/len(pnp_objP) 
        print('inliers ratio: ',round(float(inliers_ratio),2))
        # re-obtain the 3 D points if the conditions satisfied
        if (inliers_ratio < 0.9 or len(reference_2D) < 100):
        	#Initiliazation new landmarks
            curImage_R = getRightImage(i)
            z = z + 1
            #extracting the features and matching
            landmark_3D_new, reference_2D_new  = extract_keypoints_orb(curImage, curImage_R, K, baseline, reference_2D)
            reference_2D_new = reference_2D_new.astype('float32')
            landmark_3D_new = inv_transform.dot(np.vstack((landmark_3D_new.T, np.ones((1,landmark_3D_new.shape[0])))))
            valid_matches = landmark_3D_new[2,:] >0
            landmark_3D_new = landmark_3D_new[:,valid_matches]
            reference_2D = np.vstack((reference_2D, reference_2D_new[valid_matches,:]))
            landmark_3D =  np.vstack((landmark_3D, landmark_3D_new.T)) 
            print(z)       
        reference_img = curImage
        #storing the estimated trajectory
        draw_x, draw_y = int(tvec[0]) + 300, int(tvec[2]) + 100;
        #storing the ground truth trajectory
        true_x, true_y = int(truePose[i][3]) + 300, int(truePose[i][11]) + 100
        curError = np.sqrt((tvec[0]-truePose[i][3])**2 + (tvec[1]-truePose[i][7])**2 + (tvec[2]-truePose[i][11])**2)
        #finding the current error between ground truth and estimated trajectory
        print('Current Error: ', round(float(curError),2))
        #saving the maximum error
        if (curError > maxError):
            maxError = curError
        #3D visualization of the point clouds 
        #ax.plot3D(tvec[0], tvec[1], tvec[2], 'gray')
        #text to be put in the interface 
        text = "Coordinates: x ={0:02f}m y = {1:02f}m z = {2:02f}m".format(float(tvec[0]), float(tvec[1]), float(tvec[2]));
        #estimated trajectory
        cv2.circle(traj, (draw_x, draw_y) ,1, (0,0,255), 2);
        #ground truth trajectory
        cv2.circle(traj, (true_x, true_y) ,1, (255,0,0), 2);
        #displaying of the point clouds 
        cv2.rectangle(traj, (10, 30), (550, 50), (0,0,0), cv2.FILLED);
        cv2.putText(traj, text, (10,50), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8);
        cv2.imshow( "Trajectory", traj );
        k = cv2.waitKey(1) & 0xFF
        if k == 27: break
    #printing the maximum error
    print('Maximum Error: ', maxError)
    #saving the map
    cv2.imwrite('smap_orb.png', traj);

if __name__ == '__main__':
	#returning the left frame 
    left_img    = getLeftImage(0)
    #returning the right frame
    right_img   = getRightImage(0)
    baseline = 0.54;
    #calibrating the camera intrinsic and extrinsic parameters
    K =  getK()
    #pose estimation and visualization
    playImageSequence(left_img, right_img, K)