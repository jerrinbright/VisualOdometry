# 3D Pose Estimation using Stereo Visual Odometry 

Development of python package to reconstruct indoor and outdoor environments with diverse texture contrasts using Oriented FAST and Rotated Brief (ORB) feature detector and descriptor, FLANN for matching and RANSAC for outlier removal and Optical flow and PnP (DLT and Levenberg) for estimating the pose of robot<br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/map.png" width="2000"/><br><br>
Various Features extractors used for analysis: FAST, SURF, SIFT, ORB<br>
Various Matchers: BFMatcher, FLANN<br>
Tracking: KL-based Optical Flow<br>
Rotational and Traslational vector approximation: PnP<br><br>

Camera Projection Matrix:
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/projection.jpg" width="2000"/><br><br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/projection_expanded.jpg" width="2000"/><br><br>

PnP stamds for Perspective-n-points, where n=3 here.<br>
The 3 point clouds are taken as landmarks and are obtained by Triangulation. <br>

PnP is a 2 step process:<br>
1.) Direct Linear Transform (DLT)- To estimate approximate Rotational and Traslational vector<br>
2.) Levenberg Marquardt Algorithm- To optimize the Rotational and Traslational vector obtained from DLT by reducing the reprojection error<br>

Once Rotational and Traslational vector is obtained, trajectory can be plotted in the user interface. 
