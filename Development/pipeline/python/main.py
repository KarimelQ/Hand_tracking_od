import sys, os
sys.path.append(os.path.join(os.getcwd(),'python'))

import tkinter as tk
import threading  # For running the gesture detection in a separate thread
import time

# from hand_simulator     import handSimulator, handDetector
from hand_detector      import HandDetector
from camera_handler     import CameraHandler
from interface_handler  import GestureApp

def gesture_detection_loop(app, CameraHandler):
    while True:
        gesture = "x"
        app.update_gesture_label(gesture)  # Update label with detected gesture
        time.sleep(0.1)  # Sleep for a while to control the loop frequency


if __name__ == "__main__":
    root = tk.Tk()
    app = GestureApp(root)
    HD = HandDetector('','')
    CH = CameraHandler()

    gesture_thread = threading.Thread(target=gesture_detection_loop, args=(app,CH))
    gesture_thread.daemon = True
    gesture_thread.start()
    root.mainloop()