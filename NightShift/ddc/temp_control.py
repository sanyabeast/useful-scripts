import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('increment', metavar='N', type=int)

args = parser.parse_args()
step = 15

import monitorcontrol
from monitorcontrol import Monitor
from monitorcontrol.__main__ import main
from monitorcontrol import get_monitors

params = {
    "max_color": 50,
    "blue_gain": {
        "min": 0,
        "max": 50
    },
    "red_gain": {
        "min": 50,
        "max": 50
    },
    "green_gain": {
        "min": 25,
        "max": 50
    },
    "blue_level": {
        "min": 30,
        "max": 50
    },
    "red_level": {
        "min": 50,
        "max": 50
    },
    "green_level": {
        "min": 39,
        "max": 50
    },
    "contrast": {
        "min": 35,
        "max": 50
    }
}

def get_current_level( value: int, min_value: int, max_value: int ) -> int:
    return 100 - (( value - min_value ) / ( max_value - min_value )) * 100

def calc_color_value(level: int, min_value: int, max_value: int) -> int:
    print(level)
    r = min_value + ( 1 - ( level / 100 ) ) * ( max_value - min_value )
    return int(r)

night_light_level = 0

for monitor in get_monitors():
    with monitor:
        video_gain_blue = monitor.get_parameter( "video_gain_blue" )
        night_light_level = get_current_level( video_gain_blue, params["blue_gain"]["min"], params["blue_gain"]["max"] )
        print("current level")
        print(night_light_level)
        break

night_light_level += int(args.increment * step)
print(night_light_level)

if 0 > night_light_level:
    night_light_level = 100
elif 100 < night_light_level:
    night_light_level = 0
    
print(night_light_level)


# night_light_level = 100


#setting values
for monitor in get_monitors():
    with monitor:
        monitor.set_parameter("video_gain_blue",   calc_color_value( night_light_level, params["blue_gain"]["min"], params["blue_gain"]["max"]) )
        monitor.set_parameter("video_gain_green",  calc_color_value( night_light_level, params["green_gain"]["min"], params["green_gain"]["max"]) )
        monitor.set_parameter("video_gain_red",    calc_color_value( night_light_level, params["red_gain"]["min"], params["red_gain"]["max"]) )
        monitor.set_parameter("video_level_blue",  calc_color_value( night_light_level, params["blue_level"]["min"], params["blue_level"]["max"]) )
        monitor.set_parameter("video_level_green", calc_color_value( night_light_level, params["green_level"]["min"], params["green_level"]["max"]) )
        monitor.set_parameter("video_level_red",   calc_color_value( night_light_level, params["red_level"]["min"], params["red_level"]["max"]) )
        monitor.set_parameter("image_contrast",    calc_color_value( night_light_level, params["contrast"]["min"], params["contrast"]["max"] ))

# main(["--set-saturation", str(50)])
# main(["--set-luminance", str(luminance)])