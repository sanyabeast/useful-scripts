# ico_hue_rotated_versions.py

ico_hue_rotated_versions.py - Generate rotated hue versions of an ICO file.

This script takes an ICO file as input and generates multiple new ICO files, each with the hue of the largest icon frame rotated by a specified step value (e.g., 10 degrees).  The alpha channel is preserved during the rotation process.

**Dependencies:**
*   Python 3.x
*   Pillow (PIL) - `pip install Pillow`
*   NumPy - `pip install numpy`

**Author:** [Your Name/Team Name]

**Version:** 1.0

## Functionality Breakdown:

The script is structured into the following key components:

### `apply_hue_rotation(image, angle)`:

*   Takes a PIL Image object and an angle (in degrees) as input.
*   Converts the image to RGBA format if it's not already.
*   Separates the alpha channel from the RGB channels.
*   Converts the RGB channels to HSV color space.
*   Rotates the hue component of the HSV image using NumPy, wrapping around at 256 degrees.
*   Converts the rotated HSV image back to RGB.
*   Merges the rotated RGB channels with the original alpha channel.
*   Returns a new PIL Image object with the rotated hue.

### `process_icon(image_path, step)`:

*   Takes the path to an ICO file and a rotation step value as input.
*   Validates that the provided file exists and is an ICO file.
*   Opens the ICO image using PIL.
*   Extracts all frames from the ICO file.  An ICO can contain multiple icons of different sizes.
*   Determines the largest icon frame based on its pixel dimensions (width * height).
*   Iterates through hue angles, starting from the specified `step` and incrementing by `step` up to 360 degrees.
*   For each hue angle:
    *   Calls `apply_hue_rotation()` to rotate the hue of the largest icon frame.
    *   Constructs a new filename for the rotated image (e.g., `original_icon_hue10.ico`).
    *   Saves the rotated image as a new ICO file, ensuring that only the largest size is included in the output.
    *   Prints a confirmation message indicating the saved filepath.
*   Handles potential errors during image processing and prints error messages to the console.

### `if __name__ == '__main__':`:

*   This block executes when the script is run directly (not imported as a module).
*   Parses command-line arguments:  the ICO file path and the rotation step value.
*   Validates that the correct number of arguments are provided.
*   Converts the step value to an integer, handling potential `ValueError` exceptions if the input is not numeric.
*   Calls `process_icon()` with the parsed arguments.

## Assumptions & Requirements:

*   **Input File:** The script expects a valid ICO file as input.  It will check for this and exit gracefully if it's not an ICO file.
*   **ICO Structure:** It assumes that the ICO file contains at least one frame. If no frames are found, it will print an error message and exit.
*   **PIL Version:** The script is tested with Pillow (PIL) version 9.x or higher.  Older versions might have compatibility issues.
*   **NumPy:** NumPy is used for efficient array manipulation during hue rotation. Ensure that NumPy is installed correctly.
*   **Alpha Channel Preservation:** The script explicitly preserves the alpha channel during the hue rotation process, ensuring transparency is maintained in the output images.

## Limitations:

*   **Largest Size Only:**  The script currently only saves the largest icon frame from the input ICO file. It does not generate rotated versions of all frames within the ICO.
*   **No Error Handling for Invalid ICOs:** While it checks if the file is an ICO, more robust error handling could be added to handle malformed or corrupted ICO files.
*   **Performance:** Processing large ICO files with many frames can be slow.  Optimization might be necessary for very large files.
*   **Color Space Conversion:** The conversion between RGB and HSV color spaces can introduce slight rounding errors, which may result in minor color shifts.

## Example Use Cases:

1.  **Creating variations of an app icon:** Generate multiple versions of an application icon with slightly different hues for A/B testing or to provide users with a choice of colors.
2.  **Generating themed icons:** Create a set of icons with consistent themes by rotating the hue by specific amounts.
3.  **Automated icon generation:** Integrate this script into a larger workflow to automatically generate multiple icon variations as part of an asset creation pipeline.

## Usage:

To run the script, use the following command in your terminal:

```bash
python ico_hue_rotated_versions.py <ico_image_path> <step>
```

*   `<ico_image_path>`:  The path to the input ICO file (e.g., `myicon.ico`).
*   `<step>`: The rotation step value in degrees (e.g., 10, 30, 45). This determines how much the hue will be rotated for each generated image.

### Example:

To generate ICO files with hues rotated by 20 degrees from `myicon.ico`, run:

```bash
python ico_hue_rotated_versions.py myicon.ico 20
```

This will create new ICO files named `myicon_hue20.ico`, `myicon_hue40.ico`, `myicon_hue60.ico`, and so on, up to `myicon_hue340.ico` in the same directory as `myicon.ico`.

## Future Enhancements:

*   Add support for generating rotated versions of all frames within the ICO file.
*   Implement more robust error handling for invalid ICO files.
*   Allow users to specify the output directory.
*   Provide options for controlling the color space conversion process (e.g., using different HSV implementations).
*   Add a progress bar to indicate the processing status.
