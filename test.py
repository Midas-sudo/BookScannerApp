
import scrcpy
import cv2
from functools import *

# If you already know the device serial
client = scrcpy.Client(device="PL2GAR9830701342")
pop = 0
def on_frame(frame, teste):
    global pop
    if frame is not None and pop != 1:
        print(frame)
        # frame is an bgr numpy ndarray (cv2' default format)
        cv2.imshow("viz", frame)
        pop =1
    cv2.waitKey(10)

client.max_fps = 10
client.max_width= 600
ola ="testet"
f = partial(on_frame, teste="1234")
client.add_listener(scrcpy.EVENT_FRAME, f)
client.start(threaded=True)