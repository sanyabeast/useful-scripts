# paletted.py

README for paletted.py

## Overview

The `paletted.py` script takes an input image and reduces its color palette to a specified number of colors, while also applying pixelation. It uses the Python Imaging Library (PIL) to perform these operations.

## Logic Breakdown

The script performs the following steps:

1.  **Argument Parsing:** Retrieves the input image filename and desired number of colors from command-line arguments. If the number of colors is not provided, it defaults to 8. Also retrieves pixelation level which defaults to 4.
2.  **Image Loading:** Loads the specified image using `PIL.Image.open()`. 
3.  **Pixelation:** The image is first resized down and then back up again using nearest neighbor resampling. This effectively creates a pixelated effect.
4.  **Palette Conversion:** Converts the image to an 8-bit paletted format ('P') using `PIL.Image.convert()`. It utilizes adaptive quantization for color selection, limiting the number of colors to the specified value. Floyd-Steinberg dithering is implicitly used by Image.ADAPTIVE.
5.  **Output Saving:** Saves the resulting image with a modified filename that includes the original filename and the number of colors used (e.g., `image_8colors.png`).

## Requirements & Assumptions

*   **Python Environment:** Requires Python 3 to be installed.
*   **PIL/Pillow Library:**  Requires the Pillow library (`pip install pillow`). This is a fork of PIL (Python Imaging Library).
*   **Input Image:** Assumes that the input image file exists and is in a format supported by PIL (e.g., PNG, JPG, GIF). 
*   **Command Line Usage:** The script is designed to be run from the command line.
*   **Pixelation Level:** Pixelation level must be an integer greater than 0.

## Limitations

*   **Error Handling:**  The script has minimal error handling. It will exit with an error message if the input filename is missing, but it doesn't handle cases where the image file is corrupted or in an unsupported format.
*   **Color Palette Selection:** The adaptive quantization method used for palette selection might not always produce visually optimal results.  The quality of the color reduction depends heavily on the original image content.
*   **Output Format:** The output image is saved as a PNG file, regardless of the input image's format. This ensures lossless compression and compatibility.

## Usage Examples

1.  **Basic usage (default 8 colors):**
    ```bash
    python paletted.py my_image.jpg
    ```
    This will create a file named `my_image_8colors.png` with an 8-color palette applied to the image.

2.  **Specifying the number of colors:**
    ```bash
    python paletted.py my_image.jpg 16
    ```
    This will create a file named `my_image_16colors.png` with a 16-color palette.

3.  **Specifying the number of colors and pixelation level:**
    ```bash
    python paletted.py my_image.jpg 4 2
    ```
    This will create a file named `my_image_4colors.png` with a 4-color palette and pixelation level of 2.

## Additional Notes

*   The script uses adaptive quantization for color reduction, which attempts to choose the best colors based on the image's content.  Experimenting with different numbers of colors can significantly affect the visual outcome.
*   The output filename is constructed by replacing the original extension with `_num_colors.png`. This ensures a consistent naming convention.
*   Consider adding more robust error handling to handle invalid input files or other potential issues in a production environment.

## Author

[Your Name/Organization (Optional)]
