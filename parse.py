import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser(description='Parse the video file and Extractor')
parser.add_argument('video', type=str, help='path to video file')
parser.add_argument('extractor', type=str, help='extractor')
parser.add_argument('smoothening', type=str, help='smoothening')
parser.add_argument('descriptor', type=str, help='descriptor')
args = parser.parse_args()

def parse():

    if(args.extractor == 'ORB'):
        print('Executing ORB feature extractor')
        a = 1
    if(args.extractor == 'SURF'):
        print('Executing SURF feature extractor')
        a = 2
    if(args.extractor == 'SIFT'):
        print('Executing SIFT feature extractor')
        a = 3
    if(args.extractor == 'KAZE'):
        print('Executing KAZE feature extractor')
        a = 4
    if(args.extractor == 'AKAZE'):
        print('Executing AKAZE feature extractor')
        a = 5
    if(args.extractor == 'BRISK'):
        print('Executing BRISK feature extractor')
        a = 6

    if(args.smoothening == 'Filter2D'):
        print('Executing Filter2D prepocessing')
        b = 1
    if(args.smoothening == 'GaussianBlur'):
        print('Executing GaussianBlur prepocessing')
        b = 2
    if(args.smoothening == 'bilateralFilter'):
        print('Executing bilateralFilter prepocessing')
        b = 3

    if(args.descriptor == 'BFMatcher'):
        print('Executing BFMatcher')
        c = 1
    if(args.descriptor == 'FLANN'):
        print('Executing FLANN')
        c = 2

    return(a,b,c,args)