# File : Test : Stream Capture using ImageIO
# Author : Tej Pandit
# Date : Oct 2024
# NOTE : Tested with Android App [IPWebcam]
# URL = "http://192.168.4.27:8080/video"

import imageio.v3 as iio
import matplotlib.pyplot as plt

URL = "http://192.168.4.27:8080/shot.jpg"

# with iio.imopen(URL, "r") as file:
#     frame = file.read()

# Open the video stream
reader = iio.imopen(URL, "r")

# Read a single frame
frame = reader.read()

# Display the frame
plt.imshow(frame)
plt.axis('off')  # Hide axis ticks
plt.show()