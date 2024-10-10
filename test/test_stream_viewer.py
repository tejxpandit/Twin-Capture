# File : Test : Stream Viewer with DearPyGUI
# Author : Tej Pandit
# Date : Oct 2024
# NOTE : Tested with Android App [IPWebcam by]
# URL = "http://192.168.4.27:8080/video"

import cv2
import dearpygui.dearpygui as dpg
from time import sleep

URL = "http://192.168.4.27:8080/video"


def CaptureAndView():
    key = cv2. waitKey(1)
    # webcam = cv2.VideoCapture(URL)
    webcam = cv2.VideoCapture(0)
    sleep(2)

    frame_number = 0
    while True:

        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
    
            if(frame_number > 1):
                img = cv2.resize(frame,(640,480))
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                

                frame_number = 0
            else:
                frame_number += 1

            
            #results.show()

            key = cv2.waitKey(1)
            if key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break
        
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

# DPG Context
dpg.create_context()

# DPG Viewport
dpg.create_viewport(title="Project Title", width=600, height=200)

# DPG Window
dpg.add_window(label="viewer", tag="viewer_window")
CaptureAndView()

# DPG Render Context
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()