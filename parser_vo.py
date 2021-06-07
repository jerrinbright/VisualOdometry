import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser(description='Parse the type of Extractor and Pre-processing Method')
parser.add_argument('extractor', type=str, help='extractor')
parser.add_argument('smoothening', type=str, help='smoothening')
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
    if(args.smoothening == 'averageBlur'):
        print('Executing averageBlur prepocessing')
        b = 4
    if(args.smoothening == 'medianBlur'):
        print('Executing medianBlur prepocessing')
        b = 5
    if(args.smoothening == 'Rotate'):
        print('Executing rotate prepocessing')
        b = 6
    if(args.smoothening == 'None'):
        print('No prepocessing')
        b = 7

    return(a,b,args)
