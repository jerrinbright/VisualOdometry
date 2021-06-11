import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Parse the video file and Extractor')
parser.add_argument('extractor', type=str, help='extractor')
parser.add_argument('descriptor', type=str, help='descriptor')
parser.add_argument('matcher', type=str, help='matcher')
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
    
    if(args.extractor == 'ORB'):
        print('Executing ORB feature extractor')
        d = 1
    if(args.extractor == 'SURF'):
        print('Executing SURF feature extractor')
        d = 2
    if(args.extractor == 'SIFT'):
        print('Executing SIFT feature extractor')
        d = 3
    if(args.extractor == 'BRIEF'):
        print('Executing BRIEF feature extractor')
        d = 4
    if(args.extractor == 'AKAZE'):
        print('Executing AKAZE feature extractor')
        d = 5
    if(args.extractor == 'BRISK'):
        print('Executing BRISK feature extractor')
        d = 6
    if(args.extractor == 'KAZE'):
        print('Executing KAZE feature extractor')
        d = 7
    if(args.extractor == 'FREAK'):
        print('Executing FREAK feature extractor')
        d = 8

    if(args.descriptor == 'BFMatcher'):
        print('Executing BFMatcher')
        c = 1
    if(args.descriptor == 'FLANN'):
        print('Executing FLANN')
        c = 2

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

    return(a,d,c,b,args)