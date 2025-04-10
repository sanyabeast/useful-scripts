# png_batch_resize.py

## png_batch_resize.py - Batch Resize PNG Images

This script resizes all `.png` images within a specified folder to fit within a maximum dimension.
It uses the Pillow (PIL) library for image manipulation and overwrites the original files with the resized versions.

**Important:** This script modifies your original image files.  Back up your images before running this script if you want to preserve the originals.

### Overview
The `png_batch_resize.py` script automates the process of resizing multiple PNG images in a given directory. It iterates through each file, checks if it's a PNG image, and then resizes it using Pillow's `thumbnail()` method. The resized image is saved back to the original file path, effectively overwriting the original.

### Main Components & Logic

The script consists of the following key components:

*   **Import Statements:** Imports necessary modules: `os` for interacting with the operating system (file paths), `sys` for command-line arguments, and `PIL.Image` for image manipulation.
*   **`resize_images(folder_path, max_size)` Function:** This function performs the core resizing logic:
    *   It takes the folder path containing the images and the maximum size (width or height) as input.
    *   It iterates through each file in the specified `folder_path` using `os.listdir()`. 
    *   For each file, it checks if the filename ends with `.png` to ensure it's a PNG image.
    *   If it is a PNG image, it constructs the full file path using `os.path.join()`. 
    *   It attempts to open the image using `PIL.Image.open()`.  A `try...except` block handles potential errors during this process (e.g., corrupted files).
    *   The `image.thumbnail((max_size, max_size), Image.ANTIALIAS)` method resizes the image. The `thumbnail()` function ensures that the image fits within the specified dimensions while preserving its aspect ratio.  `Image.ANTIALIAS` is used for a higher quality resizing.
    *   The resized image is saved back to the original file path using `image.save()`, overwriting the original file.
    *   If an error occurs during any of these steps, it prints an error message including the filename and the exception details.
*   **`if __name__ == '__main__':` Block:** This block ensures that the resizing logic is executed only when the script is run directly (not imported as a module).
    *   It checks if the correct number of command-line arguments (3: script name, folder path, max size) are provided.
    *   If not, it prints a usage message. 
    *   Otherwise, it extracts the `folder_path` and `max_size` from the command-line arguments.
    *   It converts `max_size` to an integer using `int()`.  This is crucial for Pillow's image resizing functions.
    *   Finally, it calls the `resize_images()` function with the extracted folder path and maximum size.

### Assumptions & Requirements

*   **Python 3:** The script requires Python 3 to run. It uses features specific to Python 3 (e.g., `print()`).
*   **Pillow Library (PIL):**  The script relies on the Pillow library for image manipulation. You must have it installed.
    ```bash
pip install pillow
```
*   **Valid Folder Path:** The provided folder path must be a valid directory accessible by the user running the script.
*   **PNG Images Only:** The script is designed to process only `.png` files. Other file types will be ignored.
*   **Overwrites Original Files:**  The script *overwrites* the original image files with the resized versions. **Back up your images before using this script!**

### Limitations

*   **No Error Handling for All Cases:** While there's basic error handling within the `resize_images` function, it might not catch all possible errors (e.g., insufficient disk space).
*   **Aspect Ratio Preservation:** The `thumbnail()` method preserves aspect ratio, which means one dimension will be resized to fit the `max_size`, while the other is adjusted accordingly.
*   **No Progress Indicator:**  The script doesn't provide a progress indicator for large numbers of images. This can make it seem unresponsive during processing.
*   **Limited File Type Support:** Only PNG files are supported.

### Example Use Cases

1.  **Resizing Product Images:** You have a folder containing product images in PNG format, and you need to resize them all to fit within a specific display size on your website (e.g., 200x200 pixels).
2.  **Preparing Images for Social Media:** You want to resize a batch of PNG images to be suitable for posting on social media platforms with limited image dimensions.

### Usage Examples

To run the script, open your terminal or command prompt and navigate to the directory where `png_batch_resize.py` is located. Then use the following command:

```bash
python png_batch_resize.py /path/to/your/image/folder 200
```

*   Replace `/path/to/your/image/folder` with the actual path to the folder containing your PNG images.
*   Replace `200` with the desired maximum size (in pixels) for both width and height.  The script will resize each image so that its largest dimension is no more than 200 pixels.

### Additional Notes

*   **Backup:** Always back up your images before running this script, as it overwrites the original files.
*   **Permissions:** Ensure you have write permissions to the folder containing the images.
*   **Large Folders:** For very large folders with many images, consider using a more robust solution that provides progress monitoring and potentially uses multi-threading for faster processing.  This script is suitable for moderate numbers of images.

### Author
[Your Name/Organization]
