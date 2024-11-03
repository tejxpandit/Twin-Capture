# File : Test : Chaning Image Texture
# Author : Tej Pandit
# Date : Oct 2024

import dearpygui.dearpygui as dpg
from ImageView import ImageView
import time
import cv2

def update():
    check, frame = webcam.read()
    ImgViewer.updateImage(image=frame, tag="jelly", img_type="opencv")

# DPG Context
dpg.create_context()
# DPG Viewport
dpg.create_viewport(title="Image Viewer", width=600, height=300)
# DPG Window
dpg.add_window(label="Image Viewer", tag="img_view")
dpg.add_tab_bar(parent="img_view", tag="tabs")
dpg.add_tab(parent="tabs", tag="taba", label="Tab-A")
dpg.add_tab(parent="tabs", tag="tabb", label="Tab-B")

dpg.add_button(label="Update", parent="tabb", tag="update_button", callback=update)
dpg.add_group(parent="tabb", tag="mygroup", horizontal=True, width=400, height=400)

# DPG Image Viewer Example
ImgViewer = ImageView()
# ImgViewer.newImage("TestImage.png", parent="img_view", tag="jelly")

# OpenCV Stream
URL = "http://192.168.4.27:8080/video"
webcam = cv2.VideoCapture(URL)
# webcam = cv2.VideoCapture(0)
check, frame = webcam.read()
# cv2.imshow("Capturing", frame)

id = ImgViewer.newImage(parent="tabb", tag="jelly", def_width=1920, def_height=1080, def_channels=3)
print(ImgViewer.images[id].img_type)
print(ImgViewer.images[id].format)
print(ImgViewer.images[id].width)
print(ImgViewer.images[id].height)
print(ImgViewer.images[id].channels)
print(len(ImgViewer.images[id].data))

# DPG Render Context
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()