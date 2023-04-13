#!/bin/bash

# Get the script name and directory
SCRIPT_NAME=$(basename "$0")
SCRIPT_DIR=$(dirname "$0")

# Create the log file name
LOG_FILE="$SCRIPT_DIR/${SCRIPT_NAME%.sh}.log"

# Get the current date and time
DATETIME=$(date +"%Y-%m-%d %H:%M:%S")

# Get the command line arguments
ARGS="$@"

# Get the name of the function or script that called this function
if [ "$FUNCNAME" = "main" ]; then
    CALLER="$SCRIPT_NAME"
else
    CALLER="$FUNCNAME"
fi

# Log the message
echo "$DATETIME: $ARGS" >> "$LOG_FILE"