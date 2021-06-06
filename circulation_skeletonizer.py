import pandas as pd
# import cairo
import matplotlib.pylab as plt
import math
import numpy as np
from numpy import *
import glob
import os
import os.path
import time
import cv2
import random
import ast
from PIL import Image
from math import *
import networkx as nx
import matplotlib.cm as cm
from matplotlib.pyplot import figure, show, rc
from scipy.ndimage.interpolation import geometric_transform
from skimage.morphology import skeletonize
from skimage import data
import sknw
from shapely.geometry import LineString
import warnings
warnings.filterwarnings("ignore")

master_list = []

def get_len(x1,y1,x2,y2):
    length = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return length

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.abs(np.rad2deg((ang1 - ang2))+90)

def get_skeleton(img_2,im_background):
    # print("get skell called")
    # open and skeletonize
    img = np.abs(np.round(img_2[:,:,0]/255).astype(np.int))
    img_white = img_2
    ske = skeletonize(img).astype(np.uint16)

    # build graph from skeleton
    graph = sknw.build_sknw(ske)

    # draw edges by pts
    poly_point_lst = []
    for (s,e) in graph.edges():
        ps = graph[s][e]['pts']
        for i in range(len(ps)):      
            # cv2.circle(im_background,(ps[i][1], ps[i][0]), 4,(255,0,0), 3)
            poly_point_lst.append((ps[i][1], ps[i][0]))            
        _points = np.array([poly_point_lst])
        cv2.polylines(im_background,  np.int32([_points]), False, (255,0,255), 1, lineType=cv2.LINE_AA)
        poly_point_lst.clear()
    
    #TODO https://stackoverflow.com/questions/17241830/opencv-polylines-function-in-python-throws-exception

    # draw node by o
    nodes = graph.nodes()
    ps = np.array([nodes[i]['o'] for i in nodes])
    
    #print(ps)
    
    for i in range(len(ps)):
        #print((ps[i][1], ps[i][0]))
        cv2.circle(im_background,(int(ps[i][1]), int(ps[i][0])), 3,(0,255,0),-1)
    # cv2.imwrite("temp.png", im_background)
    return graph, im_background

def get_orientation_graph(graph, img_white):
    
    #get all edges
    edges_list = [graph[s][e]['pts'] for (s,e) in graph.edges()]
    
    angles = []
    length_ = []
    failed = 0
    index_ = []
    for i in range(len(edges_list)):
        try:
            #get length edge
            ps = edges_list[i]
            y_min = ps[:,1][0]
            x_min = ps[:,0][0]
            y_max = ps[:,1][-1]
            x_max = ps[:,0][-1]
            length_.append(get_len(x_min,y_min,x_max,y_max))

            #get mid point
            ps_midpoint = ps[int(len(ps)/2)]
            point_sample_id = 4            
            
            val_min = np.argmin([ ps[:,1][int(len(ps)/2)-point_sample_id] ,ps[:,1][int(len(ps)/2)+point_sample_id] ])
            
            if(val_min==0):
                i_ = int(len(ps)/2)-point_sample_id
                x__min= ps[:,0][i_]
                y__min= ps[:,1][i_]
            
            if(val_min==1):
                i_ = int(len(ps)/2)+point_sample_id
                x__min= ps[:,0][i_]
                y__min= ps[:,1][i_]
            
            s_pt = [ps[:,0][int(len(ps)/2)-point_sample_id] - x__min,ps[:,1][int(len(ps)/2)-point_sample_id] - y__min]
            e_pt = [ps[:,0][int(len(ps)/2)+point_sample_id] - x__min,ps[:,1][int(len(ps)/2)+point_sample_id] - y__min]

            angles.append(angle_between(e_pt, s_pt))
            index_.append(i)

        except:
            failed = failed+1
    
    angles = np.array(angles).astype(int)
    unique_angles, counts = np.unique(angles, return_counts=True)

    length_selected = np.array(length_)[index_]

    cumulative_sum = []
    for ang in unique_angles:
        cumulative_sum.append(np.sum(length_selected[angles==ang]))

    #add 0 and 180 and delete 180
    try:
        id_180 = np.where(unique_angles==180)[0][0]
        id_0 = np.where(unique_angles==0)[0][0]
        unique_angles = np.delete(unique_angles,id_180)
        cumulative_sum = np.delete(cumulative_sum,id_180)
    except:
        pass

    #double values for 180 to 360
    u_a = np.append(unique_angles,unique_angles+180)*2*np.pi/360
    radius = np.append(cumulative_sum,cumulative_sum) 

    fig = plt.figure(figsize=(10, 10))
    ax_exp = fig.add_subplot(polar=True)
    ax_exp.bar(u_a, radius, width=0.1, bottom=0.2, color="black")
    # print(f'cir module : failed : {failed}')

    return plt, (u_a/np.pi*360/2).astype(int), radius