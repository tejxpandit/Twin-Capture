# File : Test : Shared Memory Image Transfer between Processes
# Author : Tej Pandit
# Date : Oct 2024

import numpy as np
from multiprocessing import Process, Array, Value
from PIL import Image

def process_image(arr, shape, dtype, filename):
  """
  Process an image using shared memory.

  Args:
    arr: The shared memory array.
    shape: Shape of the image as a tuple (height, width, channels).
    dtype: NumPy data type of the image.
    filename: Name of the file to save the processed image.
  """
  # Convert the 1D array to a NumPy array with the correct shape and data type
  img_np = np.frombuffer(arr.get_obj(), dtype=dtype).reshape(shape)

  # Perform image processing (example: convert to grayscale)
  img_gray = Image.fromarray(img_np).convert('L') 

  # Save the processed image
  img_gray.save(filename)
