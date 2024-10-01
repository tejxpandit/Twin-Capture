# File      : Twin Capture App
# Project   : Twin Capture
# Author    : Tej Pandit
# Date      : Sept 2024

import dearpygui.dearpygui as dpg

class TwinCaptureApp:
    def __init__(self):
        self.mode = "mode_capture"

    def start(self):
        # DPG Context
        dpg.create_context()
        
        # DPG Viewport
        dpg.create_viewport(title="Twin Capture", width=600, height=200)
        
        # DPG Window
        dpg.add_window(label="", tag="tag")
        dpg.add_viewport_menu_bar(tag="menubar_viewport")
        dpg.add_menu(label="Mode", parent="menubar_viewport", tag="menubar_viewport_mode")
        dpg.add_menu_item(label="Capture", parent="menubar_viewport_mode", tag="mode_capture", callback=self.setMode)
        dpg.add_menu_item(label="Playback", parent="menubar_viewport_mode", tag="mode_playback", callback=self.setMode)
        dpg.add_menu(label="Add", parent="menubar_viewport", tag="menubar_viewport_add")
        dpg.add_menu_item(label="Video Source", parent="menubar_viewport_add", tag="menubar_add_videosrc", callback=self.addVideoSource)
        
        # DPG Render Context
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def setMode(self, mode):
        self.mode = mode

    def addVideoSource(self):
        pass