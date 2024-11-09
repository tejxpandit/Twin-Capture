# File      : Twin Capture App
# Project   : Twin Capture
# Author    : Tej Pandit
# Date      : Oct 2024

import dearpygui.dearpygui as dpg
from VideoSource import VideoSource
import threading
from threading import Event

class TwinCaptureApp:
    def __init__(self):
        self.mode = "mode_capture"
        self.video_sources = {}
        self.video_source_queue = {}
        self.source_count = 0
        self.source_enqueued = False
        self.source_dequeued = False
        self.remove_src_id = 0
        self.update_thread = None

    def start(self):
        # DPG Context
        dpg.create_context()
        
        # DPG Viewport
        dpg.create_viewport(title="Twin Capture", width=800, height=400)
        
        # Menu Toolbar
        dpg.add_viewport_menu_bar(tag="menubar_viewport")
        dpg.add_menu(label="Mode", parent="menubar_viewport", tag="menubar_viewport_mode")
        dpg.add_menu_item(label="Capture", parent="menubar_viewport_mode", tag="mode_capture", callback=self.setMode)
        dpg.add_menu_item(label="Playback", parent="menubar_viewport_mode", tag="mode_playback", callback=self.setMode)
        dpg.add_menu(label="Add", parent="menubar_viewport", tag="menubar_viewport_add")
        dpg.add_menu_item(label="Video Source", parent="menubar_viewport_add", tag="menubar_add_videosrc", callback=self.addVideoSource)
        
        # Add *Record All* Button
        # dpg.add_menu_item(label="RECORD ALL", parent="menubar_viewport", callback=self.recordAll)

        # Control Window
        # dpg.add_window(label="Source Controls", tag="tag")

        # Start Update Thread
        self.updatethread = threading.Thread(target=self.update)
        self.updatethread.start()
        # Use events for control
        
        # DPG Render Context
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

        
    def setMode(self, mode):
        self.mode = mode

    def addVideoSource(self):
        self.source_enqueued = True

    def enqueueVideoSource(self):
        self.source_count += 1
        vs = VideoSource(self.source_count, self)
        vs.app()
        self.video_sources[self.source_count] = vs

    def removeVideoSource(self, src_id):
        self.remove_src_id = src_id
        self.source_dequeued = True
        
    def dequeueVideoSource(self, src_id):
        del self.video_sources[src_id]

        # LOG ACTIVE VIDEO SOURCES
        # for v_id, v in self.video_sources.items():
        #     print(v.type)
        #     print(v.name)

    def update(self):
        while True:
            for v_id, vs in self.video_sources.items():
                vs.updateVideoFrame()
            if self.source_enqueued:
                self.enqueueVideoSource()
                self.source_enqueued = False
            if self.source_dequeued:
                self.dequeueVideoSource(self.remove_src_id)
                self.source_dequeued = False

#----------------
# EXAMPLE : TEST
if __name__ == '__main__': 
    # Start Twin Capture App
    twincapture = TwinCaptureApp()
    twincapture.start()