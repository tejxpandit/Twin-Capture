# File      : Video Source Configurator
# Project   : Twin Capture
# Author    : Tej Pandit
# Date      : Oct 2024

import dearpygui.dearpygui as dpg
from util.VideoStream import VideoStream
from util.ImageView import ImageView

class VideoSource:
    def __init__(self, video_src_id=0, video_sources=[]):
        self.id = video_src_id
        self.video_sources = video_sources
        self.name = "Video " + str(video_src_id)
        self.type = None
        self.source_types = ["Camera", "IP/Mobile"]
        self.sources = []
        self.video_width = 400
        self.video_height = 100
        self.streaming_state = False
        self.recording_state = False
        self.ip_address = None
        self.port_address = None
        self.cam_src = None
    
    def app(self):
        self.window = dpg.add_window(label=self.name, width=200, height=200, on_close=self.deleteVideoSource)
        self.tabs = dpg.add_tab_bar(parent=self.window)

        # Settings Tab : Source Selection Controls
        self.settings_tab = dpg.add_tab(label="Settings", parent=self.tabs)
        dpg.add_text("Select Video Source Type", parent=self.settings_tab)
        self.source_types_dropdown = dpg.add_combo(self.source_types, parent=self.settings_tab, callback=self.selectSrcType)
