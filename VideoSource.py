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
