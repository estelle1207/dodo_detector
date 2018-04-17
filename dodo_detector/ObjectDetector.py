#!/usr/bin/env python
import cv2
from abc import ABCMeta, abstractmethod

from imutils.video import WebcamVideoStream


class ObjectDetector(metaclass=ABCMeta):

    @abstractmethod
    def from_image(self, frame):
        pass

    def _detect_from_stream(self, get_frame, stream):
        ret, frame = get_frame(stream)

        while ret:
            marked_frame, objects = self.from_image(frame)

            cv2.imshow("image", marked_frame)
            if cv2.waitKey(1) == 27:
                break  # ESC to quit

            ret, frame = get_frame(stream)

    def from_camera(self, camera_id=0):
        stream = WebcamVideoStream(src=camera_id).start()

        def get_frame(stream):
            frame = stream.read()
            ret = True
            return ret, frame

        self._detect_from_stream(get_frame, stream)

    def from_video(self, filepath):
        stream = cv2.VideoCapture()
        stream.open(filename=filepath)

        def get_frame(stream):
            ret, frame = stream.read()
            return ret, frame

        self._detect_from_stream(get_frame, stream)
