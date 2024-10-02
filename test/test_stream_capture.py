# File : Test : Mobile Phone Webcam Server
# Author : Tej Pandit
# Date : Sept 2024
# NOTE : Tested with Android App [IPWebcam by]
# URL = "http://192.168.4.27:8080/video"

# Not Tested with Android App [ScreenStream by Dmytro Kryvoruchko]
# URL = "http://" + "192.168.0.105" + ":8080/stream.mjpeg"

import cv2
from time import sleep

URL = "http://192.168.4.27:8080/video"

key = cv2. waitKey(1)
webcam = cv2.VideoCapture(URL)
#webcam = cv2.VideoCapture(0)
sleep(2)

frame_number = 0
while True:

    try:
        check, frame = webcam.read()
        cv2.imshow("Capturing", frame)
 
        if(frame_number > 1):
            img = cv2.resize(frame,(640,480))
            #cv2.imshow("Img", img)

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # results = model(img_rgb)

            # for box in results.xyxy[0]:
            #     #print(box[5])
            #     if box[4]>0.5:
            #         xB = int(box[2])
            #         xA = int(box[0])
            #         yB = int(box[3])
            #         yA = int(box[1])
            #         cv2.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)
                

            # cv2.imshow("YOLO", img)
            #print(results)

            # results = results.pandas().xyxy[0]
            # for obj in range(len(results.index)):
            #     print(results.loc[obj].at["name"])

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