# replace_pixels.py

README for replace_pixels.py

This document provides information about the `replace_pixels.py` script, including its purpose, functionality, usage instructions, and limitations.

## Overview

The `replace_pixels.py` script modifies an image by cropping a portion from the top and adding a colored band to the bottom. This is useful for tasks like removing unwanted elements from the top of an image or adding a custom footer/banner.

## Main Components & Logic

The script performs the following steps:

1.  **Argument Parsing:** It checks if exactly three command-line arguments are provided: `image_path`, `pixels`, and `color`. If not, it prints usage instructions and exits.
2.  **Image Loading:** It opens the image specified by `image_path` using the Pillow (PIL) library.
3.  **Cropping:** It crops a rectangular region from the top of the image with a height equal to the value provided in the `pixels` argument. This effectively removes the top 'pixels' number of rows.
4.  **Color Band Creation:** It creates a new RGB image (a band) with dimensions matching the width of the original image and the height specified by the `pixels` argument. The color of this band is determined by the comma-separated values provided in the `color` argument (e.g., '255,0,0' for red).
5.  **Image Composition:** It creates a new RGB image with the same dimensions as the original image.
6.  **Pasting:** It pastes the cropped portion of the original image into the top-left corner of the new image and then pastes the color band onto the bottom edge of the new image.
7.  **Saving:** It saves the modified image to a new file with a name derived from the original filename, appended with an underscore and a unique hexadecimal identifier generated using `uuid.uuid4().hex`. The saved image is always in PNG format.

## Requirements & Assumptions

*   **Python Environment:** Requires Python 3.x installed on your system.
*   **Pillow (PIL) Library:**  The script relies heavily on the Pillow library for image manipulation. You **must** install it before running the script: `pip install pillow`
*   **Image Format:** The script assumes the input image is in a format supported by Pillow (e.g., PNG, JPG).
*   **Color Format:**  The color argument expects comma-separated RGB values (e.g., '255,0,0'). It's assumed that these are integers.
*   **Pixel Value:** The `pixels` argument must be an integer representing the number of pixels to crop from the top and the height of the colored band added at the bottom.

## Limitations

*   **Error Handling:**  The script has minimal error handling. It doesn't explicitly handle cases like invalid image paths, incorrect color formats, or file write errors. These would likely result in a Python traceback.
*   **Image Format Conversion:** The output is always saved as a PNG file. There's no option to specify the output format.
*   **Color Space:**  The script assumes an RGB color space. It might not work correctly with images using different color spaces (e.g., grayscale, CMYK).
*   **No Input Validation:** The script does not validate user input beyond checking the number of arguments. Invalid pixel or color values could lead to unexpected results.

## Usage Examples

To run the script, use the following command-line syntax:

```bash
python replace_pixels.py <image_path> <pixels> <color>
```

*   **Example 1: Removing 100 pixels from the top and adding a red band:**
    ```bash
    python replace_pixels.py image.png 100 255,0,0
    ```
    This will crop 100 pixels from the top of `image.png` and add a red (RGB: 255, 0, 0) band with a height of 100 pixels at the bottom. The modified image will be saved as something like `image_xxxxxxxxxxxxxxx.png`, where 'xxxxxxxxxxxxxxx' is a unique identifier.

*   **Example 2: Removing 50 pixels from the top and adding a green band:**
    ```bash
    python replace_pixels.py my_photo.jpg 50 0,255,0
    ```
    This will crop 50 pixels from the top of `my_photo.jpg` and add a green (RGB: 0, 255, 0) band with a height of 50 pixels at the bottom.

## Additional Notes

The script's filename is intentionally named `modify_image.py` in the comments to align with the usage example provided within the code itself.  This discrepancy should be addressed by renaming the file to `replace_pixels.py` and updating all references accordingly for consistency.

## Author

@sanyabeast, 2023, Ukraine
```
