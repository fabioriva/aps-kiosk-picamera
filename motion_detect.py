#!/usr/bin/python3

import numpy as np
import time
import urllib.request
from picamera2 import Picamera2

lsize = (320, 240)
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"},
                                                 lores={"size": lsize, "format": "YUV420"})
picam2.configure(video_config)
picam2.start()

time.sleep(1)  # Allow the camera to warm up

w, h = lsize
prev = None
motion = True
start_time = 0

while True:
    cur = picam2.capture_buffer("lores")
    cur = cur[:w * h].reshape(h, w)
    if prev is not None:
        # Measure pixels differences between current and previous frame
        mse = np.square(np.subtract(cur, prev)).mean()
        if mse > 20:
            print("New motion", mse)
            motion = True
            start_time = time.time()  # init start time
            contents = urllib.request.urlopen(
                "http://localhost:9999/api/kiosk/motion/1").read()
            print(contents)
            # urllib.request.urlopen("http://localhost:9999/api/kiosk/motion/1").read()
        else:
            diff = time.time() - start_time
            if diff > 60 and motion:
                print("No motion detected!")
                motion = False
                contents = urllib.request.urlopen(
                    "http://localhost:9999/api/kiosk/motion/0").read()
                print(contents)
            # urllib.request.urlopen("http://localhost:9999/api/kiosk/motion/0").read()

    prev = cur
    time.sleep(0)
