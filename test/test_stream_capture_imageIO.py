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

# FAILS EVERY TIME