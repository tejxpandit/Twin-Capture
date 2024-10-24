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


if __name__ == '__main__':
  # Load the image
  img = Image.open("your_image.jpg")  # Replace with your image file
  img_np = np.array(img)

  # Get image shape and data type
  shape = img_np.shape
  dtype = img_np.dtype

  # Create a shared memory array
  arr = Array('b', img_np.size)  # 'b' for unsigned byte

  # Copy image data to the shared array
  arr[:] = img_np.flatten()

  # Create shared variables for shape
  height = Value('i', shape[0])
  width = Value('i', shape[1])
  channels = Value('i', shape[2])

  # Create and start the process
  p = Process(target=process_image, args=(arr, (height.value, width.value, channels.value), dtype, "processed_image.jpg"))
  p.start()
  p.join()

  print("Image processed and saved as processed_image.jpg")