# @sanyabeast, 2023, Ukraine
# install `pillow` first
# usage example:
# python modify_image.py image.png 100 255,0,0

import sys
import os
import uuid
from PIL import Image

if len(sys.argv) != 4:
    print("Usage: python modify_image.py <image_path> <pixels> <color>")
    sys.exit()

image_path = sys.argv[1]
pixels = int(sys.argv[2])
color = tuple(map(int, sys.argv[3].split(',')))
modified_image_path = os.path.splitext(image_path)[0] + '_' + uuid.uuid4().hex + '.png'

with Image.open(image_path) as image:
    width, height = image.size
    cropped = image.crop((0, 0, width, height - pixels))
    color_band = Image.new('RGB', (width, pixels), color)
    new_image = Image.new('RGB', (width, height))
    new_image.paste(cropped, (0, 0))
    new_image.paste(color_band, (0, height - pixels))
    new_image.save(modified_image_path)

print("Modified image saved as:", modified_image_path)