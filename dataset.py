import numpy as np
import cv2

#returning the absolute scale 
def getAbsoluteScale(f, frame_id):
      #acquiring the previous frame ground truth from the KITTI dataset
      x_pre, y_pre, z_pre = f[frame_id-1][3], f[frame_id-1][7], f[frame_id-1][11]
      #acquiring the current frame ground truth from the KITTI dataset
      x    , y    , z     = f[frame_id][3], f[frame_id][7], f[frame_id][11]
      #finding the root mean square (RMS) error that's the scaling factor
      scale = np.sqrt((x-x_pre)**2 + (y-y_pre)**2 + (z-z_pre)**2)
      #returning the calculated scaling factor value
      return x, y, z, scale

#Ground truth from KITTI dataset
def getTruePose():
    file = '00/00.txt'
    return np.genfromtxt(file, delimiter=' ',dtype=None)

#Frames of Left camera from KITTI dataset 
def getImages(i):
    return cv2.imread('00/image_1/{0:06d}.png'.format(i), 0)

#Declaring the camera parameters
def getK():
    return   np.array([[7.188560000000e+02, 0, 6.071928000000e+02], [0, 7.188560000000e+02, 1.852157000000e+02], [0, 0, 1]])