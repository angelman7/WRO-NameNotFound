# MIT License
# Copyright (c) ROBOTONIO
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

from logging import DEBUG as logging_debug_level, basicConfig as logging_basic_config, error as logging_error, info as logging_info
from cv2 import CAP_GSTREAMER, VideoCapture, imshow, waitKey
from imutils import resize as imutils_resize
from datetime import datetime

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

logging_basic_config(filename="./jetson.log", level=logging_debug_level, encoding='utf-8')

class Camera:
    def __init__(self, type=-1, width=1280, height=720, framerate=60, flip=0):
        self.width = width
        self.height = height
        self.framerate = framerate
        self.flip = flip
        self.camera = None
        try:
            if type == -1:
                self.camera = VideoCapture(self.gstreamer_pipeline(), CAP_GSTREAMER)
            else:
                self.camera = VideoCapture(type)
            logging_info("[" + str(datetime.now())[0:18] + "] Succesfuley opened camera")
        except:
            logging_error("[" + str(datetime.now())[0:18] + "] Failed to load camera")

    def gstreamer_pipeline(self):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                self.width,
                self.height,
                self.framerate,
                self.flip,
                self.width,
                self.height,
            )
        )

    def get_frame(self, w=640):
        suc, frame = self.camera.read()
        if not suc:
            logging_error("[" + str(datetime.now())[0:18] + "] Failed to capture image")
            return
        return imutils_resize(frame, width=w)


def main():
    camera = Camera()
    while True:
        frame = camera.get_frame(640)
        imshow("frame", frame)
        key = waitKey(1) & 0xFF
        if key == 27:
            break


if __name__ == "__main__":
    main()
