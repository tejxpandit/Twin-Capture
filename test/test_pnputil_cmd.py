# File : Test : Get list of Cameras using pnputil on windows
# Author : Tej Pandit
# Date : Nov 2024

import subprocess
import re

def getCameraDevices(device_class):
  try:
    # Try to run the pnputil command as a subprocess
    result = subprocess.run(['pnputil', '/enum-devices', '/class', device_class], 
                           capture_output=True, text=True, check=True)
    output = result.stdout
    
    # Use a regular expression to find the device descriptions
    descriptions = re.findall(r"Device Description:\s*(.*)", output)
    if len(descriptions) > 0:
      return descriptions
    else:
      return []
  except subprocess.CalledProcessError as e:
    print(f"Error executing pnputil: {e}")
    return []

# Example
image_devices = getCameraDevices("Image")
camera_devices = getCameraDevices("Camera")
camera_devices.extend(image_devices)
for device in camera_devices:
    print(device)