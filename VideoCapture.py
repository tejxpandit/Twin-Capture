# File      : Video Capture Class for Python
# Author    : Tej Pandit
# Date      : Oct 2024

import time
import cv2
from pygrabber.dshow_graph import FilterGraph

class VideoCapture:
    def __init__(self):
        self.cam = None
        self.capture_device_flag = False
        self.capture_device_type = "Camera" #"IP/Mobile"
        self.camera_url = None
        self.camera_id = 0
