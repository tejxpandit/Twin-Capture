# File      : Twin Capture App
# Project   : Twin Capture
# Author    : Tej Pandit
# Date      : Sept 2024

import dearpygui.dearpygui as dpg

class TwinCaptureApp:
    def __init__(self):
        self.varName = None

    def start(self):
        # DPG Context
        dpg.create_context()
        
        # DPG Viewport
        dpg.create_viewport(title="Twin Capture", width=600, height=200)
        
        # DPG Window
        dpg.add_window(label="", tag="tag")
        
        # DPG Render Context
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
