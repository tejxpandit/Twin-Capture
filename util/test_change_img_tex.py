# File : Test : Chaning Image Texture
# Author : Tej Pandit
# Date : Oct 2024

import dearpygui.dearpygui as dpg
from ImageView import ImageView
import time

def update():
    ImgViewer.updateImage("TestImage3.png", "jelly")

# DPG Context
dpg.create_context()
# DPG Viewport
dpg.create_viewport(title="Image Viewer", width=600, height=300)
# DPG Window
dpg.add_window(label="Image Viewer", tag="img_view")

dpg.add_button(label="Update", parent="img_view", tag="update_button", callback=update)
dpg.add_group(parent="img_view", tag="mygroup", horizontal=True, width=400, height=400)

# DPG Image Viewer Example
ImgViewer = ImageView()
ImgViewer.newImage("TestImage.png", parent="img_view", tag="jelly")

# DPG Render Context
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()