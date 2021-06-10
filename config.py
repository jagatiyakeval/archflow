from pygame import font
from datetime import datetime
import cv2
font.init()

ICON_FILE = 'assets\outline_view_in_ar_black_24dp.png' #https://fonts.google.com/icons

# Screen size:
WIDTH = 3090
HEIGHT = 1933

# Radius of the start and goal circles:
RADIUS = 10

START_INIT_POS = (303, 250)
GOAL_INIT_POS = (680, 350)

START_COLOR = (0, 255, 0)
GOAL_COLOR = (255, 0, 0)

OBSTACLES_COLOR = (255, 255, 255)#(77, 135, 181)
OBSTACLES_RADIUS = 7

# During RRT, update the screen every MAX_EDGES_POOL new edges created.
MAX_EDGES_POOL = 10

# Filename to save and load obstacles map:
MAP_FILENAME = 'frames_shots\map.png'

# Video Settings
VIDEO_PATH = 'media\videos'
VIDEO_FPS = 200.0
VIDEO_FORMAT = 'MJPG' #https://www.fourcc.org/codecs.php
VIDEO_EXTENSION = 'avi'
VIDEO_FILENAME = f'media\{datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")}.{VIDEO_EXTENSION}'
# VIDEO_WRITER = cv2.VideoWriter(VIDEO_FILENAME, cv2.VideoWriter_fourcc(*VIDEO_FORMAT), VIDEO_FPS, (WIDTH, HEIGHT) )

# Font used to display information about the algorithm:
FONT = font.SysFont('Tahoma', 25, bold = True)
