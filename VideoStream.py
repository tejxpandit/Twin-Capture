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
        self.camera_url = ""
        self.camera_id = 0
        self.setBuffersize(2)
        self.setTimeInterval(0.01)

    def listCameras(self):
        devices = FilterGraph().get_input_devices()
        available_cameras = {}
        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name
        return available_cameras

    def begin(self):
        self.enabled.set()
        self.process = mp.Process(target=self.func, args=(self.enabled, self.capture_device_type, self.camera_id, self.camera_url, self.buffer, self.initfunc, self.datafunc, self.time_interval, ))
        self.process.start()

