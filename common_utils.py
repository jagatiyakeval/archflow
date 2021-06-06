import cv2
import numpy as np

def get_center_of_poly(pts):
    # try:
    #     M = cv2.moments(pts)
    # except:        
    M = cv2.moments(np.array([pts]))
    centX = int(M["m10"] / M["m00"])
    centY = int(M["m01"] / M["m00"])
    return (centX, centY)