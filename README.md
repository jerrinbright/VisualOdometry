# VISUAL-ODOMETRY
Development of python package to reconstruct indoor and outdoor environments with diverse texture contrasts using Oriented FAST and Rotated Brief (ORB) feature detector and descriptor, FLANN for matching and RANSAC for outlier removal and Optical flow and PnP (DLT and Levenberg) for estimating the pose of the robot

## HOW TO USE FOR MONO VO

- Clone the Repo
- Download the KITTI Dataset with ground truth poses from <a href="http://www.cvlibs.net/datasets/kitti/eval_odometry.php">here</a>. Change the dataset path in the ``` dataset.py``` file.
- Then, run the ``` main.py``` python file. The format for running the VO is 
``` python3 main.py <EXTRACTOR> <PRE-PROCESSOR> ```
For Example, ``` python3 main.py ORB bilateralFiltering ```

## REFERENCES
1.) https://github.com/felixchenfy/Monocular-Visual-Odometry<br>
2.) https://github.com/anubhavparas/visual-odometry<br>
3.) https://github.com/polygon-software/python-visual-odometry<br>

Refer my <a href="https://jbright.tech/#projects"> website</a> for more info about visual odometry!
