# File : Test : Stream Capture using ImageIO
# Author : Tej Pandit
# Date : Oct 2024
# NOTE : Tested with Android App [IPWebcam]
# URL = "http://192.168.4.27:8080/video"

import imageio.v3 as iio
import matplotlib.pyplot as plt

URL = "http://192.168.4.27:8080/video"

# for idx, frame in enumerate(iio.imiter(URL)):
#     print(f"Frame {idx}: avg. color {np.sum(frame, axis=-1)}")

with iio.imread(
    URL,  # Replace with your actual MJPEG URL
    # plugin="FFMPEG",  # Use the FFMPEG plugin
    # Other FFMPEG parameters can be added here if needed
) as reader:
    for i, im in enumerate(reader):
        print(f"Frame {i}: {im.shape}")
  
# create an image object 
# images = iio.imopen(URL, 'r') 
# print(images.shape) 
  
# # read frames one-by-one instead 
# for i in range(16): 
#     img = iio.immeta(URL)
#     # Each frame is a numpy matrix 
#     print(img.shape) 

# FAILS EVERY TIME