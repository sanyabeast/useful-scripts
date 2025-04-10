# rhashnamer.py

README for rhashnamer.py - Random File Renamer

This script renames files within a specified directory to random alphanumeric strings while preserving their original file extensions.

**Note:** This script modifies the filesystem. **Back up your data before running it!**

## Overview
rhashnamer.py is a Python script designed to rename files in a given directory using randomly generated alphanumeric names. The script recursively traverses the specified directory and its subdirectories, renaming each file encountered.  The original file extensions are preserved during the renaming process.

## Main Components & Logic

The script consists of the following key components:

*   **`generate_random_string(length)`:** This function generates a random alphanumeric string of the specified `length`. It uses the `random.choices()` method to select characters from `string.ascii_letters + string.digits`.
*   **`rename_files(directory, length)`:**  This is the core function that performs the renaming operation. It takes the directory path and the desired length of the random filenames as input. It uses `os.walk()` to recursively traverse the directory tree. For each file found:
    *   It constructs the full file path.
    *   It splits the filename into its base name and extension using `os.path.splitext()`. 
    *   It generates a new random filename using `generate_random_string(length)`. 
    *   It combines the new filename with the original extension to create the new full file path.
    *   It renames the file using `os.rename()` and prints a confirmation message to the console.
*   **`main()`:** This function handles command-line argument parsing, input validation, and calls the `rename_files()` function.

## Assumptions, Requirements & Limitations

*   **Python Version:** Requires Python 3.x.
*   **Operating System:**  Should work on any OS with a standard file system (Windows, macOS, Linux).
*   **Permissions:** The script requires write permissions to the specified directory and its subdirectories.
*   **File Name Collisions:** While unlikely, there's a theoretical possibility of generating duplicate random filenames. This could lead to files being overwritten.  The probability is very low with longer lengths but should be considered for extremely large directories.
*   **Hidden Files/Directories:** The script will rename hidden files and directories if they are present in the specified directory.
*   **Special Characters:** While the script generates alphanumeric names, ensure that your operating system supports these characters in filenames.  Certain special characters might cause issues on some systems.

## Example Use Cases

This script is useful for:

*   **Anonymizing files:** Replacing identifiable file names with random strings.
*   **Cleaning up directories:** Generating consistent and less descriptive filenames.
*   **Testing environments:** Creating a set of files with unique, randomly generated names.

## Usage

The script is executed from the command line using the following syntax:

```bash
python rhashnamer.py <directory_path> <length>
```

*   `<directory_path>`: The path to the directory containing the files you want to rename.
*   `<length>`:  The desired length of the random alphanumeric filenames (an integer).

### Examples:

1.  **Rename all files in the `/home/user/documents` directory with a filename length of 8:**
    ```bash
    python rhashnamer.py /home/user/documents 8
    ```

2.  **Rename all files in the current directory ('.') with a filename length of 12:**
    ```bash
    python rhashnamer.py . 12
    ```

## Error Handling

The script includes basic error handling:

*   **Incorrect number of arguments:** If the user doesn't provide both a directory path and a length, an error message is displayed, and the script exits.
*   **Invalid directory:** If the provided directory path does not exist or is not a valid directory, an error message is displayed, and the script exits.

## Future Enhancements

*   Implement collision detection and handling to prevent overwriting files.  This could involve retrying with a different random string until a unique name is found.
*   Add options for dry-run mode (to preview changes without actually renaming files).
*   Allow specifying the character set used for generating random filenames (e.g., include underscores or hyphens).
*   Implement logging to record renamed files and any errors encountered.

## Author
[Your Name/Organization] - [Your Contact Information (Optional)]
