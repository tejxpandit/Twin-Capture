# File      : Video Source Configurator
# Project   : Twin Capture
# Author    : Tej Pandit
# Date      : Oct 2024

import re
import subprocess
from multiprocessing import Process, Queue

import dearpygui.dearpygui as dpg

from VideoStream import VideoStream
from util.ImageView import ImageView

class VideoSource:
    def __init__(self, video_src_id=0, source_manager=None):
        self.id = video_src_id
        self.source_manager = source_manager
        self.name = "Video " + str(video_src_id)
        self.type = None
        self.source_types = ["Camera", "IP/Mobile"]
        self.sources = []
        self.video_width = 1920
        self.video_height = 1080
        self.streaming_state = False
        self.playing_state = False
        self.recording_state = False
        self.ip_address = None
        self.port_address = None
        self.ext_address = None
        self.cam_src = None
        self.video_view = None

        self.initCameraList()
        self.video_stream = VideoStream()
    
    def app(self):
        self.window = dpg.add_window(label=self.name, width=200, height=200, on_close=self.deleteVideoSource)
        self.tabs = dpg.add_tab_bar(parent=self.window)

        # Settings Tab : Source Selection Controls
        self.settings_tab = dpg.add_tab(label="Settings", parent=self.tabs)
        dpg.add_text("Select Video Source Type", parent=self.settings_tab)
        self.source_types_dropdown = dpg.add_combo(self.source_types, parent=self.settings_tab, callback=self.selectSrcType)
        
        # Source Settings : Camera
        self.camera_control_group = dpg.add_group(parent=self.settings_tab, show=False)
        dpg.add_text("Select Camera", parent=self.camera_control_group)
        self.sources_dropdown = dpg.add_combo(self.sources, parent=self.camera_control_group, callback=self.selectSrc)
        # Source Settings : IP/Mobile
        self.mobile_control_group = dpg.add_group(parent=self.settings_tab, show=False)
        self.ip_input = dpg.add_input_text(label="IP/URL", parent=self.mobile_control_group)
        self.port_input = dpg.add_input_text(label="PORT", parent=self.mobile_control_group)
        self.ext_input = dpg.add_input_text(label="EXT", parent=self.mobile_control_group)

        # View Tab : Video View
        self.view_tab = dpg.add_tab(label="View", parent=self.tabs)
        self.image_view = ImageView(parent=self.view_tab)
        self.video_view = self.image_view.newImage(scale=0.1, def_width=1920, def_height=1080, def_channels=3)
        
        # View Controls
        self.capture_control_group = dpg.add_group(parent=self.view_tab, horizontal=True)
        self.enable_stream_button = dpg.add_button(label="ENABLE", parent=self.capture_control_group, callback=self.toggleStreamingState)
        self.play_stream_button = dpg.add_button(label="PLAY", parent=self.capture_control_group, callback=self.togglePlayState)
        self.record_stream_button = dpg.add_button(label="RECORD", parent=self.capture_control_group, callback=self.toggleRecordingState, show=False)

    def getURL(self):
        self.ip_address = dpg.get_value(self.ip_input)
        self.port_address = dpg.get_value(self.port_input)
        self.ext_address = dpg.get_value(self.ext_input)

    def getCameraDevices(self, device_class):
        try:
            # Try to run the pnputil command as a subprocess
            result = subprocess.run(['pnputil', '/enum-devices', '/class', device_class], 
                                capture_output=True, text=True, check=True)
            output = result.stdout
            
            # Use a regular expression to find the device descriptions
            descriptions = re.findall(r"Device Description:\s*(.*)", output)
            if len(descriptions) > 0:
                return descriptions
            else:
                return []
        except subprocess.CalledProcessError as e:
            print(f"Error executing pnputil: {e}")
            return []
        
    def initCameraList(self):
        q = Queue()
        LC = Process(target=self.listCamerasProcess, args=(q,))
        LC.start()
        LC.join()
        vid_sources = q.get()
        # print(vid_sources)
        for id, name in vid_sources.items():
            self.sources.append(name)

    def listCamerasProcess(self, camlist):
        devices = FilterGraph().get_input_devices()
        available_cameras = {}
        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name
        camlist.put(available_cameras)
    
    def selectSrcType(self, selector, src_type):
        self.type = src_type
        if src_type == "Camera":
            dpg.show_item(self.camera_control_group)
            dpg.hide_item(self.mobile_control_group)
        elif src_type == "IP/Mobile":
            dpg.show_item(self.mobile_control_group)
            dpg.hide_item(self.camera_control_group)

    def selectSrc(self, selector, src):
        self.cam_src = self.sources.index(src)
        # print(self.cam_src)

    def toggleStreamingState(self):
        self.streaming_state = not self.streaming_state
        if self.streaming_state:
            # VIDEO ENABLED
            self.enableVideoStream()
            dpg.configure_item(self.enable_stream_button, label="DISABLE")
            dpg.show_item(self.play_stream_button)
        else:
            # VIDEO DISABLED
            self.disableVideoStream()
            dpg.configure_item(self.enable_stream_button, label="ENABLE")
            dpg.hide_item(self.play_stream_button)

    def togglePlayState(self):
        self.playing_state = not self.playing_state
        if self.playing_state:
            # VIDEO PLAYING
            self.playVideoStream()
            dpg.configure_item(self.play_stream_button, label="PAUSE")
            dpg.show_item(self.record_stream_button)
        else:
            # VIDEO PAUSE
            self.pauseVideoStream()
            dpg.configure_item(self.play_stream_button, label="PLAY")
            dpg.hide_item(self.record_stream_button)

    def toggleRecordingState(self):
        self.recording_state = not self.recording_state
        if self.recording_state:
            # RECORDING
            self.startRecording()
            dpg.configure_item(self.record_stream_button, label="STOP")
            dpg.configure_item(self.enable_stream_button, enabled=False)
        else:
            # STOPPED RECORDING
            self.stopRecording()
            dpg.configure_item(self.record_stream_button, label="RECORD")
            dpg.configure_item(self.enable_stream_button, enabled=True)
    
    def enableVideoStream(self):
        self.video_stream.setCaptureDevice(self.type)
        self.video_stream.setCameraID(self.cam_src)
        self.getURL()
        self.video_stream.setCameraIP(self.ip_address, self.port_address, self.ext_address)
        # print(self.type, self.cam_src, self.ip_address, self.port_address, self.ext_address)
        self.video_stream.begin()

    def disableVideoStream(self):
        self.video_stream.end()

    def playVideoStream(self):
        self.video_stream.unpause()

    def pauseVideoStream(self):
        self.video_stream.pause()

    def startRecording(self):
        self.updateVideoFrame()
        pass

    def stopRecording(self):
        self.updateVideoFrame()
        pass

    def deleteVideoSource(self):
        if self.recording_state:
            self.stopRecording()
        if self.streaming_state:
            self.disableVideoStream()
        if self.source_manager is not None:
            self.source_manager.removeVideoSource(self.id)

    def updateVideoFrame(self):
        frame = self.video_stream.getData()
        if frame is not None:
            self.image_view.updateImage(image=frame, tag=self.video_view, img_type="opencv")
        # print(frame)

    # CAMERA LIST : OPTION - A [DIRECT FILTERGRAPH]
    # def initCameraList(self):
    #     vid_sources = self.listCameras()
    #     # print(vid_sources)
    #     for id, name in vid_sources.items():
    #         self.sources.append(name)
    # def listCameras(self):
    #     devices = FilterGraph().get_input_devices()
    #     available_cameras = {}
    #     for device_index, device_name in enumerate(devices):
    #         available_cameras[device_index] = device_name
    #     return available_cameras

    # CAMERA LIST : OPTION - B [NEW FILTERGRAPH PROCESS]
    # def initCameraList(self):
    #     q = Queue()
    #     LC = Process(target=self.listCamerasProcess, args=(q,))
    #     LC.start()
    #     LC.join()
    #     vid_sources = q.get()
    #     # print(vid_sources)
    #     for id, name in vid_sources.items():
    #         self.sources.append(name)
    # def listCamerasProcess(self, camlist):
    #     devices = FilterGraph().get_input_devices()
    #     available_cameras = {}
    #     for device_index, device_name in enumerate(devices):
    #         available_cameras[device_index] = device_name
    #     camlist.put(available_cameras)


#----------------
# EXAMPLE : TEST
if __name__ == '__main__': 
    # DPG Context
    dpg.create_context()
    # DPG Viewport
    dpg.create_viewport(title="Video Source", width=600, height=300)

    VS = VideoSource()
    VS.app()

    # DPG Render Context
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()