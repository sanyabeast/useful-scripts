import argparse
parser = argparse.ArgumentParser(description='Process some integers.')

args = parser.parse_args()

import monitorcontrol
from monitorcontrol import Monitor
from monitorcontrol.__main__ import main
from monitorcontrol import get_monitors

    
#setting values
for monitor in get_monitors():
    with monitor:
        monitor.set_parameter("image_luminance", 100)
        monitor.set_parameter("image_contrast", 75)
        monitor.set_parameter("video_gain_blue", 50)
        monitor.set_parameter("video_gain_green", 50)
        monitor.set_parameter("video_gain_red", 50)
        monitor.set_parameter("video_level_blue", 50)
        monitor.set_parameter("video_level_green", 50)
        monitor.set_parameter("video_level_red", 50)
        break

# main(["--set-saturation", str(50)])
# main(["--set-luminance", str(luminance)])