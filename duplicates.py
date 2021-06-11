import numpy as np

#Remove duplicate points from new query points
def removeDuplicate(queryPoints, refPoints, radius=10):
    for i in range(len(queryPoints)):
        query = queryPoints[i]
        xliml, xlimh = query[0]-radius, query[0]+radius
        yliml, ylimh = query[1]-radius, query[1]+radius
        inside_x_lim_mask = (refPoints[:,0] > xliml) & (refPoints[:,0] < xlimh)
        curr_kps_in_x_lim = refPoints[inside_x_lim_mask]
        if curr_kps_in_x_lim.shape[0] != 0:
            inside_y_lim_mask = (curr_kps_in_x_lim[:,1] > yliml) & (curr_kps_in_x_lim[:,1] < ylimh)
            curr_kps_in_x_lim_and_y_lim = curr_kps_in_x_lim[inside_y_lim_mask,:]
            if curr_kps_in_x_lim_and_y_lim.shape[0] != 0:
                queryPoints[i] =  np.array([0,0])
    return (queryPoints[:, 0]  != 0 )