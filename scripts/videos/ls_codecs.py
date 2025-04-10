# @sanyabeast, Apr 2024, Ukraine

"""

SAMPLE USAGE:
python ./videos/ls_codecs.py "C:/Movies" --recursive --codec hevc
outputs all hevc coded video files in specified directory recursively
or 
python ./videos/ls_codecs.py "C:/Movies"
outputs all video files in specified directory and their codecs NON-recursively

"""

"""
Video Codec Finder

This script lists video files and their codecs in a specified folder.
You can choose to perform a recursive search and filter the output by codec.

Usage:
    python ls_code.py /path/to/folder [--recursive] [--codec <codec_name>]

Arguments:
    /path/to/folder      Path to the folder to search for video files.
    --recursive          Perform a recursive search (optional).
    --codec <codec_name> Filter the output by a specific codec (optional).

Examples:
    List all video files and their codecs in a folder recursively:
    python ls_code.py /path/to/folder --recursive

    List all video files and their codecs in a folder without recursion:
    python ls_code.py /path/to/folder

    List video files with a specific codec (e.g., hevc):
    python ls_code.py /path/to/folder --codec hevc
"""


import os
import subprocess
import argparse

# ANSI escape codes for color printing
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
RESET = '\033[0m'

# Codec color table
codec_color_table = {
    'hevc': RED,
    'mpeg4': CYAN,
    'h264': BLUE,
    'vp9': YELLOW,
    'vc1': MAGENTA,
    # Add more codecs and corresponding colors as needed
}

def print_separator():
    print("-------------------------------------------")

def get_video_info(filepath):
    try:
        # Use ffprobe to get video information
        cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', filepath]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            codec = result.stdout.strip()
            return codec
        else:
            return None
    except Exception as e:
        print(f"Error getting video info for {filepath}: {e}")
        return None

def colorize(color, text):
    return f"{color}{text}{RESET}"

def list_video_files(folder_path, recursive, filter_codec=None):
    print(f"Listing files in `{colorize(folder_path, GREEN)}`. recursively: {colorize(str(recursive), GREEN)}. filter codec: {colorize(str(filter_codec), GREEN)}")
    print_separator()
    count = 0
    for root, dirs, files in os.walk(folder_path):
        if not recursive:
            dirs.clear()
        
        for file in files:
            filepath = os.path.join(root, file)
            _, ext = os.path.splitext(filepath)
            ext = ext.lower()
            
            # Check if the file is a video file
            if ext in ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.mpeg']:
                codec = get_video_info(filepath)

                if filter_codec:
                    if codec == filter_codec:
                        print(f"{file} - {colorize(codec_color_table.get(codec, RED), codec)}")
                        count += 1
                else:
                    if codec:
                        print(f"{file} - {colorize(codec_color_table.get(codec, RED), codec)}")
                        count += 1
                    else:
                        print(f"{file} - Unknown codec")
                        count += 1

    print_separator()
    print(f"Total files printed: {colorize(GREEN, str(count))}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List video files and their codecs.')
    
    parser.add_argument('folder_path', type=str, help='Path to the folder to search for video files.')
    parser.add_argument('--recursive', action='store_true', help='Perform a recursive search.')
    parser.add_argument('--codec', type=str, help='Filter the output by codec.')
    
    args = parser.parse_args()
    
    if os.path.isdir(args.folder_path):
        list_video_files(args.folder_path, args.recursive, args.codec)
    else:
        print("Invalid folder path.")