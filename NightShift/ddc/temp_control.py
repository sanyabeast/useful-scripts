import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('increment', metavar='N', type=int)

args = parser.parse_args()

import monitorcontrol
from monitorcontrol import Monitor
from monitorcontrol.__main__ import main
from monitorcontrol import get_monitors

use_gain = True
max_color = 50
min_blue = 0
min_green = 20
min_red = max_color

def get_current_level( value: int, min_value: int ) -> int:
    return 100 - (( value - min_value ) / ( max_color - min_value )) * 100

def calc_color_value(level: int, min_color: int) -> int:
    print(level)
    r = min_color + ( 1 - ( level / 100 ) ) * ( max_color - min_color )
    return int(r)



night_light_level = 0

for monitor in get_monitors():
    with monitor:
        video_gain_blue = monitor.get_parameter( "video_gain_blue" )
        night_light_level = get_current_level( video_gain_blue, min_blue )
        print("current level")
        print(night_light_level)
        break

night_light_level += int(args.increment)
print(night_light_level)

if 0 > night_light_level:
    night_light_level = 0
elif 100 < night_light_level:
    night_light_level = 100
    
print(night_light_level)


# night_light_level = 100


#setting values
for monitor in get_monitors():
    with monitor:
        if use_gain:
            monitor.set_parameter("video_gain_blue", calc_color_value( night_light_level, min_blue) )
            monitor.set_parameter("video_gain_green", calc_color_value( night_light_level, min_green) )
            monitor.set_parameter("video_gain_red", calc_color_value( night_light_level, min_red) )
        else:
            monitor.set_parameter("video_level_blue", calc_color_value( night_light_level, min_blue) )
            monitor.set_parameter("video_level_green", calc_color_value( night_light_level, min_green) )
            monitor.set_parameter("video_level_red", calc_color_value( night_light_level, min_red) )
        break

# main(["--set-saturation", str(50)])
# main(["--set-luminance", str(luminance)])