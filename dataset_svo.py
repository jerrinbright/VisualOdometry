import numpy as np
import cv2

#Ground truth from KITTI dataset
def getTruePose():
    file = '00/00.txt'
    return np.genfromtxt(file, delimiter=' ',dtype=None)

def getLeftImage(i):
    return cv2.imread('00/image_0/{0:06d}.png'.format(i), 0)

#Right camera frame from the stereo setup
def getRightImage(i):
    return cv2.imread('00/image_1/{0:06d}.png'.format(i), 0)

#Declaring the camera parameters
def getK():
    return   np.array([[7.188560000000e+02, 0, 6.071928000000e+02], [0, 7.188560000000e+02, 1.852157000000e+02], [0, 0, 1]])