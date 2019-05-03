from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import cv2

class CaptureRuntime(object):
    def __init__(self, output):

        self._done = False
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)
        self.cap = cv2.VideoCapture(output)

    def run(self):
        while not self._done:
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                print(frame)

if __name__=='__main__':
    ob = CaptureRuntime('test.avi')
    ob.run()
