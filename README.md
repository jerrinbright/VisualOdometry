# 3D Pose Estimation using Stereo Visual Odometry 

Development of python package to reconstruct indoor and outdoor environments with diverse texture contrasts using Oriented FAST and Rotated Brief (ORB) feature detector and descriptor, FLANN for matching and RANSAC for outlier removal and Optical flow and PnP (DLT and Levenberg) for estimating the pose of robot. Additionally, pre-processing including bilateral filtering is done to enhance the robustness of the extraction thereby reducing the reprojection error significantly.

<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/flowchart.png" width="1000" height="400" align="center"/>

## FEATURE EXTRACTION
Experimented with ORB, FAST, SHI-TOMASI, SIFT and SURF. Below image shows ORB extraction with and without size for the set 1000 feature points<br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/feature%20extraction.png" width="1000" height="300" align="center"/><br>
```sh
orb = cv2.ORB_create(nfeatures=500)
kp1, desc1 = orb.detectAndCompute(img1, None)
kp2, desc2 = orb.detectAndCompute(img2, None)
```
Comparison of all feature extractors
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/extractors.png" width="1000" height="300" align="center"/><br>
<br><br>
Smoothening/ Blurring<br><br>
Pre-processed the frames using various filters including Bilateral filtering, 2D Image filtering, Median blurring and gaussian filtering. The comparison of all this fltering based pre-processing vs the original extraction is shown below
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/smoothening.png" width="1000" height="300" align="center"/><br>

## FEATURE MATCHING
Experimented with BFMatcher and FLANN. Below image shows ORB+FLANN<br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/features_matching.png" width="1000" height="300" align="center"/><br>
```sh
search_params = dict(checks=100)
index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=2)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(desc1,desc2,k=2)
```
Comparing FLANN with BF Matcher
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/matcher.png" width="1000" height="300" align="center"/><br>

## FEATURE TRACKING
KLT-based Optical Flow algorithm<br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/tracking.png" width="1000" height="300" align="center"/><br>
```sh
lk_params = dict( winSize  = (21,21), maxLevel = 3, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
p2, st, err = cv2.calcOpticalFlowPyrLK(img_1, img_2, p1, None, **lk_params)
```

## Camera Projection Matrix
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/projection.jpg" width="700"/><br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/projection_expanded.jpg" width="700"/><br><br>

## Rotational and Traslational vector approximation: PnP
PnP stands for Perspective-n-points, where n=3 here.<br>
The 3 point clouds are taken as landmarks and are obtained by Triangulation. <br><br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/imgs/pnp.jpg" width="700"/><br><br>

PnP is a 2 step process:<br>
1.) Direct Linear Transform (DLT)- To estimate approximate Rotational and Traslational vector<br>
2.) Levenberg Marquardt Algorithm- To optimize the Rotational and Traslational vector obtained from DLT by reducing the reprojection error<br>
```sh
_, rvec, tvec, inliers = cv2.solvePnPRansac(pnp_objP , pnp_cur, K, None)
```    
<br>
Once Rotational and Traslational vector is obtained, trajectory can be plotted in the user interface. <br><br>
<img src="https://github.com/jerriebright/VISUAL-ODOMETRY/blob/main/maps/orb.png" width="400" height="400" align="center"/><br>

## REFERENCES
1.) https://github.com/felixchenfy/Monocular-Visual-Odometry<br>
2.) https://github.com/anubhavparas/visual-odometry<br>
3.) https://github.com/polygon-software/python-visual-odometry<br>
<br>
THE END!
