# 3D Pose Estimation using Stereo Visual Odometry 

Development of python package to reconstruct indoor and outdoor environments with diverse texture contrasts using Oriented FAST and Rotated Brief (ORB) feature detector and descriptor, FLANN for matching and RANSAC for outlier removal and Optical flow and PnP (DLT and Levenberg) for estimating the pose of robot

Various Features extractors used for analysis: FAST, SURF, SIFT, ORB
Various Matchers: BFMatcher, FLANN
Tracking: KL-based Optical Flow
Rotational and Traslational vector approximation: PnP

PnP stamds for Perspective-n-points, where n=3 here.
The 3 point clouds are taken as landmarks and are obtained by Triangulation. 

PnP is a 2 step process:
1.) Direct Linear Transform (DLT)- To estimate approximate Rotational and Traslational vector
2.) Levenberg Marquardt Algorithm- To optimize the Rotational and Traslational vector obtained from DLT by reducing the reprojection error

Once Rotational and Traslational vector is obtained, trajectory can be plotted in the user interface. 
