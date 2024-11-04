# File      : Video Streaming Class for Python
# Author    : Tej Pandit
# Date      : Oct 2024

import time
import queue
import multiprocessing as mp

from pygrabber.dshow_graph import FilterGraph

from VideoCapture import VideoCapture
from util.DataStream import DataStream

class VideoStream(DataStream):
    def __init__(self):
        super().__init__()
        self.func = self.videoStream
        self.capture_device_type = "Camera" #"IP/Mobile"
