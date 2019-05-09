import PySpin
import time

nframes = 100

# Get system
system = PySpin.System.GetInstance()

# Get camera list
cam_list = system.GetCameras()

cam = cam_list.GetByIndex(0)

cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
cam.BeginAcquisition()

nodemap = cam.GetNodeMap()
PySpin.CFloatPtr(nodemap.GetNode("AcuisitionFrameRate"))
framerate_to_set = node_acquisition_framerate.GetValue()

for i in range(nframes):
    image = cam_primary.GetNextImage()
    if image.IsIncomplete():
        print("camera image incomplete with image status %d"%image.GetImageStatus())
        continue

cam.EndAcquisition()
cam.DeInit()
del image
del cam
