# ordered_hexnamer.py

## ordered_hexnamer.py - Rename Images to Hexadecimal Names

This script renames image files (JPG and PNG) within a specified folder to names based on their sequential order represented in hexadecimal format. It first creates temporary unique filenames, then renames them sequentially.

**Important:** This script modifies files directly in the provided directory.  Back up your images before running this script!

### Main Functionality:

The script iterates through image files (JPG and PNG) within a given folder and renames them to sequential hexadecimal names, starting from '1' represented as '1'. The order of renaming is determined by the file name sorting or shuffling.

### Components & Logic Breakdown:

*   **`rename_images_hex(folder_path, shuffle=False)` Function:** This is the core function that performs the image renaming. It takes the folder path and an optional `shuffle` flag as input.
    *   **Directory Validation:** Checks if the provided `folder_path` exists and is a directory.
    *   **Image File Listing:**  Lists all files in the specified folder, filtering for JPG and PNG images (case-insensitive).
    *   **Shuffling (Optional):** If the `shuffle` flag is True, the list of image files is shuffled randomly. Otherwise, it's sorted alphabetically.
    *   **Temporary Renaming:**  Each image file is temporarily renamed to a unique UUID string combined with its original extension. This prevents naming conflicts during the final renaming process and allows for tracking the original filenames.
    *   **Hexadecimal Renaming:** The script iterates through the temporary names, converts the index (starting from 1) to hexadecimal format using `format(i + 1, 'x')`, constructs a new filename by combining the hex name with the original extension, and renames the file.  The original filenames are printed alongside the new ones.
*   **`if __name__ == '__main__':` Block:** This block handles command-line argument parsing and calls the `rename_images_hex` function.
    *   **Argument Parsing:** Checks for the correct number of arguments (folder path, optional shuffle flag).  Prints usage instructions if incorrect. 
    *   **Function Call:** Calls `rename_images_hex` with the provided folder path and determines whether to shuffle based on the presence of 'shuffle' as a command-line argument.

### Assumptions & Requirements:

*   **Python Environment:** Requires Python 3.x installed.
*   **File Permissions:** The script needs write permissions in the specified `folder_path`.
*   **Image File Types:**  Only supports renaming `.jpg` and `.png` files (case-insensitive).
*   **No Duplicate Filenames:** Assumes that there are no duplicate filenames within the target directory. If duplicates exist, the script's behavior is unpredictable.
*   **Error Handling:** The script includes basic error handling for file renaming operations but may not catch all possible exceptions.

### Limitations:

*   **Limited File Type Support:** Only handles JPG and PNG files.  Adding support for other image formats would require extending the file extension filter.
*   **No Error Recovery:** If a rename operation fails, the script prints an error message but continues processing. It doesn't attempt to recover from errors (e.g., by rolling back changes).
*   **Simple Sorting/Shuffling:** The sorting is based on filename and not any other criteria.

### Example Use Cases:

1.  **Renaming images in sequential order:**
    ```bash
    python ordered_hexnamer.py /path/to/your/images
    ```
    This will rename all JPG and PNG files in `/path/to/your/images` to names like `1.jpg`, `2.png`, `3.JPG`, etc.

2.  **Renaming images in a random order:**
    ```bash
    python ordered_hexnamer.py /path/to/your/images shuffle
    ```
    This will rename the files in `/path/to/your/images` to hexadecimal names, but the order of renaming will be randomized.

### Usage:

```bash
python ordered_hexnamer.py <folder_path> [shuffle]
```

*   `<folder_path>`:  The path to the directory containing the images you want to rename.
*   `[shuffle]` (optional): If present and set to 'shuffle', the script will shuffle the image files before renaming. Otherwise, they are renamed in alphabetical order.

### Developer Notes:

*   **Error Handling:** Consider adding more robust error handling, such as logging errors to a file or implementing retry mechanisms.
*   **File Type Support:**  To support additional image formats, modify the `endswith()` check within the list comprehension.
*   **Customizable Hexadecimal Format:** The hexadecimal format can be adjusted by changing the format string in `format(i + 1, 'x')` (e.g., `'0X'` for uppercase hex).  You could also add a command-line argument to control this.
*   **Progress Indicator:** For large directories, adding a progress indicator would improve user experience.

### Author:

[Your Name/Organization]

### License:

[Specify license - e.g., MIT License]
