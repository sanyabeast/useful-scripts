#!/bin/bash

# Check if the script received exactly two arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <terminal-emulator> \"<command>\""
    exit 1
fi

# Use the arguments in the command
$1 -e "bash -c '$2; read -n1 -r -p \"Press any key to close the terminal...\"'"