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

