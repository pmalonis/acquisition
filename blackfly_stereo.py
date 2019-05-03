import PySpin
import time

nframes = 200

# Get system
system = PySpin.System.GetInstance()

# Get camera list
cam_list = system.GetCameras()

# Figure out which is primary and secondary
if cam_list.GetByIndex(0).TLDevice.DeviceSerialNumber() == '18384055':
    cam_primary = cam_list.GetByIndex(0)
    cam_secondary = cam_list.GetByIndex(1)
else:
    cam_primary = cam_list.GetByIndex(1)
    cam_secondary = cam_list.GetByIndex(0)

# Initialize cameras
cam_primary.Init()
cam_secondary.Init()

# Set up primary camera trigger
cam_primary.LineSelector.SetValue(PySpin.LineSelector_Line2)
cam_primary.V3_3Enable.SetValue(True)

# Set up secondary camera trigger
cam_secondary.TriggerMode.SetValue(PySpin.TriggerMode_Off)
cam_secondary.TriggerSource.SetValue(PySpin.TriggerSource_Line3)
cam_secondary.TriggerOverlap.SetValue(PySpin.TriggerOverlap_ReadOut)
cam_secondary.TriggerMode.SetValue(PySpin.TriggerMode_On)

# Set acquisition mode
cam_primary.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
cam_secondary.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)


# Start acquisition; note that secondary camera has to be started first so
# acquisition of primary camera triggers secondary camera.
cam_secondary.BeginAcquisition()
cam_primary.BeginAcquisition()

#get frame rate
nodemap = cam_primary.GetNodeMap()
node_acquisition_framerate = PySpin.CFloatPtr(nodemap.GetNode("AcquisitionFrameRate"))
framerate_to_set = node_acquisition_framerate.GetValue()

recorder_primary = PySpin.AVIRecorder()
recorder_secondary = PySpin.AVIRecorder()

option = PySpin.AVIOption
option.frameRate = framerate_to_set

recorder_primary.AVIOpen('primary.avi', option)
recorder_secondary.AVIOpen('secondary.avi', option)

# Acquire images
for i in range(nframes):
    image_primary = cam_primary.GetNextImage()
    image_secondary = cam_primary.GetNextImage()
    if image_primary.IsIncomplete():
        print("Primary camera image incomplete with image
                status %d"%image_primary.GetImageStatus())
        continue
    if image_secondary .IsIncomplete():
        print("Secondary camera image incomplete with image status %d"%image_primary.GetImageStatus())
        continue

    recorder_primary.AVIAppend(image_primary)
    print("primary timestamp: %f"%time.time())
    recorder_secondary.AVIAppend(image_secondary)
    print("secondary timestamp: %f"%time.time())

recorder_primary.AVIClose()
recorder_secondary.AVIClose()

# Save images
# image_primary.Save('primary.png')
# image_secondary.Save('secondary.png')

# Stop acquisition
cam_primary.EndAcquisition()
cam_secondary.EndAcquisition()

# De-initialize
cam_primary.DeInit()
cam_secondary.DeInit()

# Clear references to images and cameras
del image_primary
del image_secondary
del cam_primary
del cam_secondary
del cam_list
