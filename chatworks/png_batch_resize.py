#!/usr/bin/env python3

import os
import sys
from PIL import Image

def resize_images(folder_path, max_size):
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            try:
                # Load the image
                image = Image.open(file_path)

                # Scale the image
                image.thumbnail((max_size, max_size), Image.ANTIALIAS)

                # Save the image
                image.save(file_path)
            except Exception as e:
                print("Error resizing image {}: {}".format(filename, e))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python resize_images.py <folder_path> <max_size>")
    else:
        folder_path = sys.argv[1]
        max_size = int(sys.argv[2])
        resize_images(folder_path, max_size)