# rename_substitute_in_folder.py

Rename Files in a Folder by Substituting a String

This script renames files within a specified folder by replacing a given string with another. It's useful for cleaning up file names or standardizing naming conventions.

**Author:** [Your Name/Team Name]
**Version:** 1.0
**Date Created:** October 26, 2023

## Overview

The `rename_substitute_in_folder.py` script iterates through all files within a designated folder and renames them by substituting a specified string with another.  The original filename is only changed if the substitution results in a different name.

## Main Components/Logic

*   **Import Statements:** Imports `os` for interacting with the operating system (file system operations) and `sys` for accessing command-line arguments.
*   **`rename_files_in_folder(folder_path, to_replace, replacement)` Function:** This is the core function that performs the renaming. It takes three arguments:
    *   `folder_path`: The path to the folder containing the files to be renamed (string).
    *   `to_replace`: The string to be replaced in the filenames (string).
    *   `replacement`: The string to replace `to_replace` with. Defaults to an empty string if not provided (string).
        The function iterates through each file in the folder using `os.listdir()`. For each filename, it replaces the specified substring using Python's built-in `replace()` method. If the resulting name is different from the original, it renames the file using `os.rename()`.  A message indicating whether a rename occurred or not is printed to the console.
*   **Main Execution Block (`if __name__ == '__main__':`)**: This block handles command-line argument parsing and calls the `rename_files_in_folder` function.
    *   It checks if at least three arguments are provided (folder path, string to replace, and optional replacement string). If not, it prints a usage message and exits.  The script also prints the values of the folder path, string to replace, and replacement string for verification before proceeding with renaming.

## Assumptions & Requirements

*   **Python Environment:** Requires Python 3.x installed on your system.
*   **Permissions:** The script needs read and write permissions within the specified `folder_path`.  If you don't have sufficient permissions, the script will fail with an error.
*   **File System:** Assumes a standard file system structure (e.g., Windows, macOS, Linux).
*   **String Replacement:** The `replace()` method performs a simple string substitution. It replaces *all* occurrences of `to_replace` within the filename.  Consider this when choosing your strings.

## Limitations

*   **No Error Handling for Specific File Errors:** While there's a general `try...except` block, it doesn't handle specific file-related errors (e.g., file already exists with the new name). This could lead to unexpected behavior in some cases.
*   **No Recursive Processing:** The script only processes files directly within the specified folder; it does not recursively process subfolders.
*   **Simple String Replacement:**  Uses basic string replacement, which might be insufficient for complex renaming scenarios (e.g., regular expressions).
*   **No Undo Functionality:** Renaming operations are permanent. There's no built-in undo functionality.

## Example Use Cases

1.  **Removing "(Copy)" from filenames:**
    ```bash
    python rename_substitute_in_folder.py "c:/my/lovely/dir" "(Copy)\
