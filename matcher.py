import numpy as np
import cv2
import time

GOOD_MATCH_PERCENT = 0.15
matches = []

def matching(a, c, bf, description, prev_description):
    
        if (c == 1):
            matches = bf.match(description,prev_description)
            matches = sorted(matches, key = lambda x:x.distance)
            numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
            best_matches = matches[:numGoodMatches]

        if (c == 2) and (a != 1):
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks=50)   # or pass empty dictionary
            flann = cv2.FlannBasedMatcher(index_params,search_params)
            matches = flann.knnMatch(description,prev_description,k=2)
            matchesMask = [[0,0] for i in range(len(matches))]
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    matchesMask[i]=[1,0]

        if (c == 2) and (a == 1):
            search_params = dict(checks=100)
            index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=2)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(description, prev_description, k=2)
            matchesMask = [[0,0] for i in range(len(matches))]
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    matchesMask[i]=[1,0]
        
        if (c == 2) and (a == 5):
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks = 50)
            description = np.float32(description)
            prev_description = np.float32(prev_description)
            FLANN = cv2.FlannBasedMatcher(indexParams = index_params, searchParams = search_params)
            matches = FLANN.knnMatch(queryDescriptors = description, trainDescriptors = prev_description, k = 2)
            matchesMask = [[0,0] for i in range(len(matches))]
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    matchesMask[i]=[1,0]
                    
        return(matches)