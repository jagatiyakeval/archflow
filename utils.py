from random import randrange as rand
from config import *
import math
import cv2
import numpy as np
import random
from skimage import measure
# import matplotlib.pyplot as plt

# returns the general Bezier cubic formula given 4 control points
def get_cubic(a, b, c, d):
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

# return one cubic curve for each consecutive points
def get_bezier_cubic(points):
    A, B = get_bezier_coef(points)
    return [
        get_cubic(points[i], A[i], B[i], points[i + 1])
        for i in range(len(points) - 1)
    ]

# evalute each cubic curve on the range [0, 1] sliced in n points
def evaluate_bezier(points, n):
    curves = get_bezier_cubic(points)
    return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])

# find the a & b points
def get_bezier_coef(points):
    # since the formulas work given that we have n+1 points
    # then n must be this:
    n = len(points) - 1

    # build coefficents matrix
    C = 4 * np.identity(n)
    np.fill_diagonal(C[1:], 1)
    np.fill_diagonal(C[:, 1:], 1)
    C[0, 0] = 2
    C[n - 1, n - 1] = 7
    C[n - 1, n - 2] = 2

    # build points vector
    P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
    P[0] = points[0] + 2 * points[1]
    P[n - 1] = 8 * points[n - 1] + points[n]

    # solve system, find a & b
    A = np.linalg.solve(C, P)
    B = [0] * n
    for i in range(n - 1):
        B[i] = 2 * points[i + 1] - A[i + 1]
    B[n - 1] = (A[n - 1] + points[n]) / 2

    return A, B

def get_new_poly_crd_v2(org_crd):
    org_new_hand = org_crd.copy()
    points = np.array(org_new_hand)
    path = evaluate_bezier(points, 50)
    final_pnts = path.astype(int)
    return final_pnts

def get_new_poly_crd_v1(org_crd):
    org_new_hand = org_crd.copy()
    new_hand = np.array(org_new_hand)
    for _ in range(5):
        new_hand = measure.subdivide_polygon(new_hand, degree=2)
    # approximate subdivided polygon with Douglas-Peucker algorithm
    appr_hand = measure.approximate_polygon(new_hand, tolerance=0.01)
    final_pnts = appr_hand.astype(int)
	# tpl_pnts = list(map(tuple, final_pnts))
    return final_pnts#, tpl_pnts

def get_random_color():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)    
    return (r, g, b)

def get_center_of_poly(pts):    
    M = cv2.moments(np.array([pts]))
    centX = int(M["m10"] / M["m00"])
    centY = int(M["m01"] / M["m00"])
    return [centX, centY]

def get_start_pos(entrance, direction):
    center = get_center_of_poly(entrance)
    top_right,btm_right = max_x,max_y = max(entrance)
    top_left,btm_left = min_x,min_y = min(entrance)
    width = max_x-min_x
    height = max_y-min_y 
    if direction == 'W->E':
        center[0] += width
    elif direction == 'E->W':
        center[0] -= width
    else:
        pass
    return tuple(center)

def dist(p1, p2):
	"""
	Compute the euclidean distance between p1 and p2.

	p1 -- point (x, y)
	p2 -- point (x, y)
	"""
	return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def randomPoint():
	"""
	Returns coordinates of a random point on the screen.
	"""
	return rand(WIDTH), rand(HEIGHT)

def inside(point, center):
	"""
	Determine if point is inside the circle centered at
	  center and with radius equal config.RADIUS.
	"""
	return dist(point, center) < RADIUS

def normalize(vx, vy):
	"""
	Normalizes the input vector and returns its coordinates.
	"""
	norm = math.sqrt(vx * vx + vy * vy)
	if (norm > 1e-6):
		vx /= norm
		vy /= norm
	return (vx, vy)
