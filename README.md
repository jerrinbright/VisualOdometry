# VISUAL ODOMETRY
Development of python package to reconstruct indoor and outdoor environments with diverse texture contrasts using Oriented FAST and Rotated Brief (ORB) feature detector and descriptor, FLANN for matching and RANSAC for outlier removal and Optical flow and PnP (DLT and Levenberg) for estimating the pose of the robot.

## HOW TO USE THIS REPO?

- Clone the Repo.
- Download the KITTI Dataset with ground truth poses from <a href="http://www.cvlibs.net/datasets/kitti/eval_odometry.php">here</a>. Change the dataset path in the ``` dataset.py``` file.
- Then, run the ``` main.py``` python file. The syntax is ``` python3 main.py <EXTRACTOR> <PRE-PROCESSOR> ```

For Example, type ``` python3 main.py ORB bilateralFiltering ``` to run monocular visual odometry using ORB feature extractors and Bilteral preprocessing filtering technique.

## HOW TO EVALUATE THE VO?

There are a lot of ways to evaluate a trajectory estimated. I have used EVO package forevaluating the R-P-Y; errors and the difference in the estimated pose with the ground truth. To do the same, follow the below steps: 

- Clone the EVO Repo (<a href="https://github.com/MichaelGrupp/evo">here</a>).
- In the source EVO Repo local folder, run ```pip install --editable . --upgrade --no-binary evo```
- Proper functioning of all EVO repo function requires: numpy, matplotlib, scipy>=1.2, pandas, seaborn>=0.9, natsort, argcomplete, colorama>=0.3, pygments, pyyaml, pillow. Refer to the ```setup.py``` in the EVO repo. 
- Then, convert the estimated trajectory into a pose file similar to the ```pose.txt``` file used in KITTI dataset for comparison. 

## HOW TO CREATE A POSE FILE?

- As a result of running the ```main.py``` file, a ```pose.txt``` file will be generated. 
- Pass the ```pose.txt``` into the ```main.py``` file inside ```kitti_ground``` folder in this repo.
- Then, a new ```pose_1.txt``` file will be generated with proper delimiters set. 
- Now, you can use this alongside the EVO repo mentioned above for comparison.

## FUTURE WORK

- Working on making a similar structure for Stereo Visual Odometry. You can refer to my ```main_svo.py``` which at present can be run to do any feature extraction, with any matcher and any type of pre-processing tool. Syntax to run the code ```python main_svo.py <VIDEO-PATH> <EXTRACTOR> <DESCRIPTOR> <MATCHER> <PRE-PROCESSOR>```.

## FEW INFOS

- The ```maps``` folder consists of few maps of the VO trajectory with different extractor techniques.
- The ```csv``` folder consists of few excel notebooks consisting various comparisons made amongst feature extractors, smoothening techniques, etc.
- The ```basics``` folder consists of a <a href="https://github.com/jerriebright/VISUAL-ODOMETRY/tree/main/basics">readme file</a> which explains the components of VO and few analysis on the components. 
- To know more about my work, <a href="https://jbright.tech/uploads/VO.pdf"> click here</a> for detailed overview and comparisons! 

## REFERENCES
1.) https://github.com/felixchenfy/Monocular-Visual-Odometry<br>
2.) https://github.com/anubhavparas/visual-odometry<br>
3.) https://github.com/polygon-software/python-visual-odometry<br>

### FEEL FREE TO RAISE YOUR QNS IN THE ISSUES SECTION. WILL BE HAPPY TO ASSIST!
