# 3D Pose Estimation using Stereo Visual Odometry 

Development of python package to reconstruct indoor and outdoor environments with diverse texture contrasts using Oriented FAST and Rotated Brief (ORB) feature detector and descriptor, FLANN for matching and RANSAC for outlier removal and Optical flow and PnP (DLT and Levenberg) for estimating the pose of robot<br><br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/map.png" width="400" height="400" align="center"/><br><br>
FEATURE EXTRACTION<br><br>
Experimented with ORB, FAST, SHI-TOMASI, SIFT and SURF. Below image shows ORB extraction<br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/feature%20extraction.png" width="1000" height="300" align="center"/><br><br>
FEATURE EXTRACTION<br><br>
Experimented with BFMatcher and FLANN. Below image shows ORB+FLANN<br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/features_matching.png" width="1000" height="300" align="center"/><br><br>

FEATURE TRACKING<br><br>
KL-based Optical Flow<br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/features_matching.png" width="1000" height="300" align="center"/><br><br>

Camera Projection Matrix:<br><br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/projection.jpg" width="700"/><br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/projection_expanded.jpg" width="700"/><br><br>

Rotational and Traslational vector approximation: PnP<br><br>
PnP stamds for Perspective-n-points, where n=3 here.<br>
The 3 point clouds are taken as landmarks and are obtained by Triangulation. <br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/pnp.jpg" width="700"/><br><br>

PnP is a 2 step process:<br>
1.) Direct Linear Transform (DLT)- To estimate approximate Rotational and Traslational vector<br>
2.) Levenberg Marquardt Algorithm- To optimize the Rotational and Traslational vector obtained from DLT by reducing the reprojection error<br>

Once Rotational and Traslational vector is obtained, trajectory can be plotted in the user interface. 
