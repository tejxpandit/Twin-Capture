# File : Test : Stream Capture using ImageIO
# Author : Tej Pandit
# Date : Oct 2024
# NOTE : Tested with Android App [IPWebcam]
# URL = "http://192.168.4.27:8080/video"

import imageio.v3 as iio
import matplotlib.pyplot as plt

URL = "http://192.168.4.27:8080/shot.jpg"
Camera = "<video0>"

plt.figure()
plt.show(block=False)

try:
    while True:
        # Open the video stream
        reader = iio.imopen(URL, "r")
        # Read a single frame
        frame = reader.read()
        # Update the plot
        plt.imshow(frame)
        # Wait for some time
        plt.pause(0.1)
        
except KeyboardInterrupt:
    pass
    
