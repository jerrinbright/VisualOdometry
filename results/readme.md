# RESULTS USING EVO REPO

For KITTI dataset evaluation, ```pose.txt``` file is required. Follow the below steps for successful evaluation.

## HOW TO CREATE A POSE FILE?

Every row of the file contains the first 3 rows of a 4x4 homogeneous pose matrix (SE(3) matrix) flattened into one line, with each value separated by a space. For example, this pose matrix:
```
a b c d
e f g h
i j k l
0 0 0 1
```
will appear in the file as the row:
```
a b c d e f g h i j k l
```
- As a result of running the ```main.py``` file, the ```pose.txt``` file will be generated. 
- Pass the ```pose.txt``` into the ```main.py``` file inside ```kitti_ground``` folder in this repo.
- Then, a new ```pose_1.txt``` file will be generated with proper delimiters set. 
- Now, you can use this pose file for evaluation using EVO repo.
- You can view the results for my set of codes using EVO repo in ```result``` folder.

## HOW TO EVALUATE THE VO?

There are a lot of ways to evaluate a trajectory estimated. I have used EVO package forevaluating the R-P-Y; errors and the difference in the estimated pose with the ground truth. To do the same, follow the below steps: 

- Clone the EVO Repo (<a href="https://github.com/MichaelGrupp/evo">here</a>).
- In the source EVO Repo local folder, run ```pip install --editable . --upgrade --no-binary evo```
- Proper functioning of all EVO repo function requires: numpy, matplotlib, scipy>=1.2, pandas, seaborn>=0.9, natsort, argcomplete, colorama>=0.3, pygments, pyyaml, pillow. Refer to the ```setup.py``` in the EVO repo. 
- Then, convert the estimated trajectory into a pose file similar to the ```pose.txt``` file used in KITTI dataset for comparison. Refer to previous topic to learn about conversion. 
- Then, type ```evo_traj kitti <file1>...<fileN> --ref=KITTI_00_gt.txt -p --plot_mode=xz``` in the EVO folders ```test/data```  directory for obtaining the results as mentioned in ```results``` folder. 
 
## RESULTS

<img src="https://github.com/jerriebright/VisualOdometry/blob/main/results/traj.png" height="300" width="300">
<img src="https://github.com/jerriebright/VisualOdometry/blob/main/results/trans.png" height="300" width="300">
<img src="https://github.com/jerriebright/VisualOdometry/blob/main/results/R-P-Y.png" height="300" width="300">

## CITATION

If you use EVO repo for research purposes, cite @
``` 
@misc{grupp2017evo,
  title={evo: Python package for the evaluation of odometry and SLAM.},
  author={Grupp, Michael},
  howpublished={\url{https://github.com/MichaelGrupp/evo}},
  year={2017}
}
``` 
