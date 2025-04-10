#!/bin/bash

# Check if the script received exactly one argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 {glx|xpresent|off}"
    exit 1
fi

# Check if the argument is one of the expected values
if [[ "$1" != "glx" && "$1" != "xpresent" && "$1" != "off" ]]; then
    echo "Error: Argument must be 'glx', 'xpresent', or 'off'"
    exit 1
fi

# Use the argument in the command
(xfconf-query -c xfwm4 -p /general/vblank_mode -s $1 && xfwm4 --replace --vblank=$1) &

echo "Command issued to set mode to $1. Please wait for the change to take effect."
exit 0