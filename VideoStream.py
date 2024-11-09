# File      : Video Streaming Class for Python
# Author    : Tej Pandit
# Date      : Oct 2024

import time
import queue
import multiprocessing as mp

from pygrabber.dshow_graph import FilterGraph

from VideoCapture import VideoCapture
from util.DataStream import DataStream

# TODO : Create Events for control
# TODO : Create Pipes for data transfer
# TODO : Explore Shared Memory for Faster Data Transfer of Images

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

    def setCameraIP(self, ip, port, ext):
        self.camera_url = str(ip) + ":" + str(port) + "/" + str(ext)
        if not self.camera_url.startswith("http"):
            self.camera_url = "http://" + self.camera_url

    def setCameraID(self, camera_id):
        self.camera_id = camera_id

    def setCaptureDevice(self, capture_device_type):
        self.capture_device_type = capture_device_type

    def videoStream(self, enabled, camera_type, cam_id, cam_url, buffer, initfunc, datafunc, time_interval):
        VC = VideoCapture()
        VC.setCaptureDevice(camera_type)
        VC.setCameraID(cam_id)
        VC.setCameraURL(cam_url)
        CameraAccess = VC.start()
        while CameraAccess:
            if enabled.is_set():
                data = VC.getVideoFrame()
                try:
                    buffer.put_nowait(data)
                except queue.Full:
                    try:
                        buffer.get_nowait()
                        buffer.put_nowait(data)
                    except queue.Empty:
                        pass
                time.sleep(time_interval)

