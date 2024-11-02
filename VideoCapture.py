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

    def setCameraURL(self, url):
        self.camera_url = url

    def setCameraIP(self, ip, port, ext):
        self.camera_url = str(ip) + ":" + str(port) + "/" + str(ext)
        if not self.camera_url.startswith("http"):
            self.camera_url = "http://" + self.camera_url

    def setCameraID(self, camera_id):
        self.camera_id = camera_id

    def setCaptureDevice(self, capture_device_type):
        self.capture_device_type = capture_device_type

    def initCaptureDevice(self):
        # First check and stop and existing camera connection
        self.stop()
        try:
            if self.capture_device_type == "Camera":
                self.cam = cv2.VideoCapture(self.camera_id)
            elif self.capture_device_type == "IP/Mobile":
                self.cam = cv2.VideoCapture(self.camera_url)
            self.capture_device_flag = True
        except:
            print("Camera Not Accessible!")
            self.capture_device_flag = False

    def start(self):
        if not self.capture_device_flag:
            self.initCaptureDevice()
        if self.capture_device_flag:
            return True
        else:
            return False
    
    def stop(self):
        if self.capture_device_flag:
            self.cam.release()
        
    def getVideoFrame(self):
        check, frame = self.cam.read()
        return frame

    # Testing Camera Function
    def testCameras(self):
        index = 0
        cameras = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                cameras.append(index)
            cap.release()
            index += 1
        return cameras


#----------------
# EXAMPLE : Test
if __name__ == '__main__': 
    VC = VideoCapture()
    VC.setCaptureDevice("Camera")
    # VC.setCaptureDevice("IP/Mobile")
    VC.setCameraIP("192.168.4.27", "8080", "video")
    VC.setCameraID(0)
    VC.start()

    frame = VC.getVideoFrame()
    import matplotlib.pyplot as plt
    plt.imshow(frame)
    plt.show()