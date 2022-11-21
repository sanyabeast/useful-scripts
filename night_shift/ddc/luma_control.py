import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('increment', metavar='N', type=int)

args = parser.parse_args()

import monitorcontrol
from monitorcontrol import Monitor
from monitorcontrol.__main__ import main
from monitorcontrol import get_monitors

luminance = 15
step = 10

for monitor in get_monitors():
    with monitor:
        luminance = monitor.get_luminance()
        break

luminance += int(args.increment * step)

if 0 > luminance:
    luminance = 0
elif 100 < luminance:
    luminance = 100
    
#setting values
for monitor in get_monitors():
    with monitor:
        monitor.set_parameter("image_luminance", luminance)
        break

# main(["--set-saturation", str(50)])
# main(["--set-luminance", str(luminance)])