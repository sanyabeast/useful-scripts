#!/bin/bash

# Check if the script received two or three arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <terminal-emulator> \"<command>\" [\"<title>\"]"
    exit 1
fi

# Use the arguments in the command
if [ "$#" -eq 3 ]; then
    title="$3"
else
    title="terminal"
fi

# Get current time and date
launch_time=$(date "+%Y-%m-%d %H:%M:%S")

# Combine launch_time and title
terminal_title="$launch_time - $title"

$1 -T "$terminal_title" -e "bash -c '$2; read -n1 -r -p \"Press any key to close the terminal...\"'"