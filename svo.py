import numpy as np
import cv2

import dataset_svo
import tracking_svo
import keypoints

#pose estimation and visualization
def playImageSequence(left_img, right_img, K):

	#feature extraction and matching using FLANN
    points, p1 = keypoints.extract_keypoints(left_img, right_img, K, baseline)

    p1 = p1.astype('float32')
    z = 0
    pnp_objP = np.expand_dims(points, axis = 2)
    reference_img = left_img
    reference_2D  = p1
    landmark_3D   = points
    #storing the true pose values 
    truePose = dataset_svo.getTruePose()
    #interface for displaying the trajectory
    traj = np.zeros((600, 600, 3), dtype=np.uint8)
    maxError = 0

    for i in range(0, 5000):

        print('image: ', i)
        curImage =  dataset_svo.getLeftImage(i)

        #tracking the left frame features with the right frame
        landmark_3D, reference_2D, tracked_2Dpoints = tracking_svo.featureTracking(reference_img, curImage, reference_2D,  landmark_3D)

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
            curImage_R = dataset_svo.getRightImage(i)
            z = z + 1
            #extracting the features and matching
            landmark_3D_new, reference_2D_new  = keypoints.extract_keypoints(curImage, curImage_R, K, baseline, reference_2D)
            reference_2D_new = reference_2D_new.astype('float32')
            landmark_3D_new = inv_transform.dot(np.vstack((landmark_3D_new.T, np.ones((1,landmark_3D_new.shape[0])))))
            valid_matches = landmark_3D_new[2,:] >0
            landmark_3D_new = landmark_3D_new[:,valid_matches]
            reference_2D = np.vstack((reference_2D, reference_2D_new[valid_matches,:]))
            landmark_3D =  np.vstack((landmark_3D, landmark_3D_new.T)) 
            print(z)       
        reference_img = curImage

        #storing the estimated trajectory
        draw_x, draw_y = int(tvec[0]) + 300, int(tvec[2]) + 100
        #storing the ground truth trajectory
        true_x, true_y = int(truePose[i][3]) + 300, int(truePose[i][11]) + 100
        curError = np.sqrt((tvec[0]-truePose[i][3])**2 + (tvec[1]-truePose[i][7])**2 + (tvec[2]-truePose[i][11])**2)
        #finding the current error between ground truth and estimated trajectory
        print('Current Error: ', round(float(curError),2))
        #saving the maximum error
        if (curError > maxError):
            maxError = curError
        #3D visualization of the point clouds 
        #text to be put in the interface 
        text = "Coordinates: x ={0:02f}m y = {1:02f}m z = {2:02f}m".format(float(tvec[0]), float(tvec[1]), float(tvec[2]))
        #estimated trajectory
        cv2.circle(traj, (draw_x, draw_y) ,1, (0,0,255), 2)
        #ground truth trajectory
        cv2.circle(traj, (true_x, true_y) ,1, (255,0,0), 2)
        #displaying of the point clouds 
        cv2.rectangle(traj, (10, 30), (550, 50), (0,0,0), cv2.FILLED)
        cv2.putText(traj, text, (10,50), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)
        cv2.imshow( "Trajectory", traj )

        k = cv2.waitKey(1) & 0xFF
        if k == 27: break
        
    #printing the maximum error
    print('Maximum Error: ', maxError)
    #saving the map
    cv2.imwrite('traj.png', traj)

if __name__ == '__main__':
	#returning the left frame 
    left_img    = dataset_svo.getLeftImage(0)
    #returning the right frame
    right_img   = dataset_svo.getRightImage(0)
    baseline = 0.54
    #calibrating the camera intrinsic and extrinsic parameters
    K =  dataset_svo.getK()
    #pose estimation and visualization
    playImageSequence(left_img, right_img, K)