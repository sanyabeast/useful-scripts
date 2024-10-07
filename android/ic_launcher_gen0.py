# created by @sanyabeast
# 18 may 2023, Kyiv, Ukraine

import os
import sys
import argparse
from PIL import Image
import cv2
import numpy as np


def resize_image(input_image_path, output_image_path, size):
    """
    Resizes the input image to the specified size and saves the resized image to the output path.

    Args:
        input_image_path (str): The path of the image to be resized.
        output_image_path (str): The path where the resized image will be saved.
        size (tuple): The size that the input image should be resized to.
    """
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)


def create_circle_image(image_path, output_path):
    """
    Creates a circular image from the input image and saves it to the output path.

    Args:
        image_path (str): The path of the image to be cropped.
        output_path (str): The path where the cropped image will be saved.
    """
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    shortest_dimension = min(img.shape[:2])
    square_img = cv2.resize(img, (shortest_dimension, shortest_dimension))

    mask = np.zeros_like(square_img)
    rows, cols, _ = square_img.shape
    cv2.ellipse(mask, center=(rows//2, cols//2), axes=(rows//2, cols//2), angle=0,
                startAngle=0, endAngle=360, color=(255, 255, 255, 255), thickness=-1)
    masked_img = cv2.bitwise_and(square_img, mask)
    masked_img[np.all(mask == 0, axis=2)] = (0, 0, 0, 0)
    cv2.imwrite(output_path, masked_img)


def main(image_path, gen_circular):
    """
    Main function that takes an image path as input, resizes the image to different dimensions
    and optionally creates circular versions of the images.

    Args:
        image_path (str): The path of the image to be resized.
        gen_circular (bool): Whether to generate circular images.
    """
    name, ext = os.path.splitext(os.path.basename(image_path))
    new_dir_path = os.path.join(os.path.dirname(image_path), name)

    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)

    dimensions = {'ldpi': (36, 36), 'mdpi': (48, 48), 'hdpi': (
        72, 72), 'xhdpi': (96, 96), 'xxhdpi': (144, 144), 'xxxhdpi': (192, 192)}

    index = 0
    for key, value in dimensions.items():
        new_image_path = os.path.join(
            new_dir_path, f'0_square_{str(index).zfill(2)}_{key.upper()}.png')
        resize_image(image_path, new_image_path, value)
        if gen_circular:
            circle_image_path = os.path.join(
                new_dir_path, f'1_rounded_{str(index).zfill(2)}_{key.upper()}.png')
            create_circle_image(new_image_path, circle_image_path)

        index += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate different sized images for Android apps.')
    parser.add_argument('image_path', help='Path of the image to resize')
    parser.add_argument('--rounded', action='store_true',
                        help='Generate circular images')
    args = parser.parse_args()
    main(args.image_path, args.rounded)
