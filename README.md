# VISUAL ODOMETRY
Development of python package/ tool for mono and stereo visual odometry. Also, pose file generation in KITTI ground truth format is done. EVO evaluation tool is used for the evaluation of the estimated trajectory using my visual odometry code. For more infos, go through this readme file.  

## PROS OF THE TOOL 

- Without changing the contents of the code, the functionality of the codes can be adjusted. That's any type of feature extractor/ matcher/ pre-processing technique/ outlier removal technique can be used typing in the command line.  
- Automatic pose file generation for KITTI dataset for comparing with the EVO evaluation repo. 
- Scripts are split based on functionality for ease of understanding of the users.

## HOW TO USE THIS REPO?

- Clone the Repo.
- Download the KITTI Dataset with ground truth poses from <a href="http://www.cvlibs.net/datasets/kitti/eval_odometry.php">here</a>. Change the dataset path in the ``` dataset.py``` file. (or)
- Download one sequence (00) and its respective pose file by <a href="https://drive.google.com/file/d/19OpF7VrMP6AmQ1eC4aapsMwzvgkGlih3/view?usp=sharing"> clicking here</a> for ease (if you want to avoid the 22 gb full size files).
- Then, run the ``` main.py``` python file. The syntax is ``` python3 main.py <EXTRACTOR> <PRE-PROCESSOR> ```

For Example, type ``` python3 main.py ORB bilateralFiltering ``` to run monocular visual odometry using ORB feature extractors and Bilteral preprocessing filtering technique.

## HOW TO CREATE A POSE FILE?

- As a result of running the ```main.py``` file, a ```pose.txt``` file will be generated. 
- Pass the ```pose.txt``` into the ```main.py``` file inside ```kitti_ground``` folder in this repo.
- Then, a new ```pose_1.txt``` file will be generated with proper delimiters set. 
- Now, you can use this pose file for evaluation using EVO repo.
- You can view the results for my set of codes using EVO repo in ```results``` folder.
## HOW TO EVALUATE THE VO?

There are a lot of ways to evaluate a trajectory estimated. I have used EVO package forevaluating the R-P-Y; errors and the difference in the estimated pose with the ground truth. To do the same, follow the below steps: 

- Clone the EVO Repo (<a href="https://github.com/MichaelGrupp/evo">here</a>).
- In the source EVO Repo local folder, run ```pip install --editable . --upgrade --no-binary evo```
- Proper functioning of all EVO repo function requires: numpy, matplotlib, scipy>=1.2, pandas, seaborn>=0.9, natsort, argcomplete, colorama>=0.3, pygments, pyyaml, pillow. Refer to the ```setup.py``` in the EVO repo. 
- Then, convert the estimated trajectory into a pose file similar to the ```pose.txt``` file used in KITTI dataset for comparison. Refer to previous topic to learn about conversion. 
- Then, type ```evo_traj kitti <file1>...<fileN> --ref=KITTI_00_gt.txt -p --plot_mode=xz``` in the EVO folders ```test/data```  directory for obtaining the results as mentioned in ```results``` folder. 

## HOW MANY METHODS ARE ADAPTED?

Currently, six types of extractors, two types of matchers, 3 types of pre-processing techniques are adapted in this repo. <br>
EXTRACTORS: ORB, SIFT, SURF, BRISK, KAZE, AKAZE.<br>
DESCRIPTORS: ORB, SIFT, SURF, BRISK, KAZE, AKAZE, FREAK, BRIEF.<br>
MATCHERS: FLANN, BFMatcher.<br>
PRE-PROCESSING: Guassian Blur, Bilateral Filtering, 2D Image Filtering, Average Blurring, Median Blurring, Rotating.<br>

## FEW INFOS

- The ```maps``` folder consists of few maps of the VO trajectory with different extractor techniques.
- The ```csv``` folder consists of few excel notebooks consisting various comparisons made amongst feature extractors, smoothening techniques, etc.
- The ```basics``` folder consists of a <a href="https://github.com/jerriebright/VISUAL-ODOMETRY/tree/main/basics">readme file</a> which explains the components of VO and few analysis on the components. 
- To know more about my work, <a href="https://jbright.tech/uploads/VO.pdf"> click here</a> for detailed overview and comparisons! 

## FUTURE WORK

Working on making a similar structure for Stereo Visual Odometry. You can refer to my ```main_svo.py``` which at present can be run to do any feature extraction, with any matcher and any type of pre-processing tool. Syntax to run the code ```python main_svo.py <EXTRACTOR> <DESCRIPTOR> <MATCHER> <PRE-PROCESSOR>```.

## REFERENCES
1.) https://github.com/felixchenfy/Monocular-Visual-Odometry<br>
2.) https://github.com/anubhavparas/visual-odometry<br>
3.) https://github.com/polygon-software/python-visual-odometry<br>

### FEEL FREE TO RAISE YOUR QNS IN THE ISSUES SECTION. WILL BE HAPPY TO ASSIST!
