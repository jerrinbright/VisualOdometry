import numpy as np 
import cv2

"""
 Ret =  0.10048613996773315
 Mtx =  [[403.93733711   0.         354.93024916]
 [  0.         400.52743884 273.87009265]
 [  0.           0.           1.        ]]
 Dist =  [[-0.19248528  0.08166069 -0.00961472 -0.01167682 -0.03537033]]
 Rvecs =  [array([[-0.20059285],
       [-0.28117925],
       [-2.77186387]])]
 Tvecs =  [array([[-0.7703538 ],
       [ 2.23966891],
       [ 7.43031368]])]
total error: 0.015505118415585838 
"""

class PinholeCamera:
	def __init__(self, width, height, fx, fy, cx, cy, 
				k1=-0.19248528, k2=0.08166069, p1=-0.00961472, p2=-0.01167682, k3=-0.03537033):
		self.width = width
		self.height = height
		self.fx = fx
		self.fy = fy
		self.cx = cx
		self.cy = cy
		self.distortion = (abs(k1) > 0.0000001)
		self.d = [k1, k2, p1, p2, k3]