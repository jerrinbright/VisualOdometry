# VISUAL ODOMETRY
Development of python package to reconstruct indoor and outdoor environments with diverse texture contrasts using Oriented FAST and Rotated Brief (ORB) feature detector and descriptor, FLANN for matching and RANSAC for outlier removal and Optical flow and PnP (DLT and Levenberg) for estimating the pose of the robot.

## HOW TO USE THIS REPO

- Clone the Repo.
- Download the KITTI Dataset with ground truth poses from <a href="http://www.cvlibs.net/datasets/kitti/eval_odometry.php">here</a>. Change the dataset path in the ``` dataset.py``` file.
- Then, run the ``` main.py``` python file. The format for running the VO is 
``` python3 main.py <EXTRACTOR> <PRE-PROCESSOR> ```

For Example, type ``` python3 main.py ORB bilateralFiltering ``` to run monocular visual odometry using Bilteral preprocessing filtering technique.

## EVALUATION

- Clone the EVO Repo (<a href="https://github.com/MichaelGrupp/evo"> here </a>).
- In the source EVO Repo local folder, run ```pip install --editable . --upgrade --no-binary evo```
- Proper functioning of all EVO repo function requires:
numpy
matplotlib
scipy>=1.2
pandas
seaborn>=0.9
natsort
argcomplete
colorama>=0.3
pygments
pyyaml
pillow.

Refer to the ```setup.py``` in the EVO repo. 
- Then, convert the estimated trajectory into a pose file similar to the ```pose.txt``` file used in KITTI dataset for comparison. 

## HOW TO CREATE A POSE FILE FOR KITTI DATASET

- As a result of running the ```main.py``` file, a ```pose.txt``` file will be generated. 
- Pass the ```pose.txt``` into the ```main.py``` file inside ```kitti_ground``` folder in this repo.
- Then, a new ```pose_1.txt``` file will be generated with proper delimiters set. 
- Now, you can use this 

## REFERENCES
1.) https://github.com/felixchenfy/Monocular-Visual-Odometry<br>
2.) https://github.com/anubhavparas/visual-odometry<br>
3.) https://github.com/polygon-software/python-visual-odometry<br>

Refer my <a href="https://jbright.tech/#projects"> website</a> for more info about visual odometry!
