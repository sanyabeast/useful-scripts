# jfif2jpg.sh

**README for jfif2jpg.sh**

This script renames files with the `.jfif` extension to `.jpg`. It recursively traverses directories, ensuring all `.jfif` files within a directory structure are converted.

## Overview

The `jfif2jpg.sh` script is designed to automate the renaming of image files from the `.jfif` format to the more common `.jpg` format. This can be useful for correcting file extensions or standardizing a collection of images. The script handles recursive directory traversal, meaning it will process all `.jfif` files within subdirectories as well.

## Logic Breakdown

The script operates in the following steps:

1.  **Argument Handling:** Checks if a directory path is provided as an argument. If no argument is given, it defaults to the current working directory (`.`).
2.  **Recursive Traversal:** Uses a `for` loop and recursion to iterate through all files and subdirectories within the specified (or default) directory.
3.  **Directory Check:** Inside the loop, it first checks if the current item is a directory using `[ -d "$file" ]`. If it's a directory, the script recursively calls itself (`$0`) with that directory as an argument to process its contents.
4.  **File Extension Check:** If the item is not a directory, it checks if the file has the `.jfif` extension using `[[ "$file" == *.jfif ]]`. This uses bash's pattern matching capabilities.
5.  **Renaming:** If the file matches the `.jfif` extension, the script renames it to `.jpg` using the `mv` command and parameter expansion `${file%.jfif}` which removes the `.jfif` suffix. 
6. **Statistics Tracking**: The script keeps track of how many files were renamed (`count`) and total number of files processed (`total`).
7.  **Output:** After processing all files, it prints a summary indicating the number of files renamed and the total number of files examined.

## Assumptions & Requirements

*   **Bash Shell:** The script is written for Bash shell and requires a compatible environment to execute.
*   **`mv` Command:**  The `mv` (move/rename) command must be available in the system's PATH. This is standard on most Unix-like systems.
*   **Read Permissions:** The user running the script needs read permissions for all directories and files it attempts to process.
*   **Write Permissions:** The user running the script needs write permissions in the directory where the renaming occurs, as `mv` modifies existing files.  If you don't have write permission, the rename operation will fail.
*   **No Overlapping Files:** The script does not handle cases where a file with the same name (but different extension) already exists. In such scenarios, the `mv` command might overwrite the existing file without warning. **Use caution!**

## Limitations

*   **Simple Extension Matching:**  The script relies on simple pattern matching for the `.jfif` extension. It doesn't perform more sophisticated checks to ensure that the files are actually valid JFIF images.
*   **No Error Handling:** The script lacks robust error handling. If a renaming operation fails (e.g., due to permissions issues), it will not explicitly report an error and may continue processing other files.
*   **Overwrites without Warning**: As mentioned above, the `mv` command can overwrite existing files with the same name if they already exist in the target directory.  There is no check for this.

## Example Use Cases

1.  **Renaming all `.jfif` files in the current directory:**
    ```bash
    ./jfif2jpg.sh
    ```

2.  **Renaming all `.jfif` files in a specific directory (e.g., `/path/to/images`):**
    ```bash
    ./jfif2jpg.sh /path/to/images
    ```

3. **Renaming .jfif files recursively within a directory:**  The script automatically handles recursive renaming.

## Additional Notes

*   **Testing:** It's highly recommended to test this script on a small sample of files before running it on an entire directory structure, especially if you are unsure about the file permissions or potential conflicts.
*   **Backup:** Consider backing up your image files before running this script. While unlikely, errors can occur, and having a backup provides a safety net.
*   **Dry Run (Simulation):**  To see what changes *would* be made without actually renaming any files, you could modify the script to print the `mv` command instead of executing it. For example, replace `mv "$file" "${file%.jfif}.jpg"` with `echo mv "$file" "${file%.jfif}.jpg"`.  This is a good way to preview the changes before committing.
*   **File Validation:** If you need more robust validation of the files being renamed, consider integrating image file format detection libraries into the script. This would prevent renaming non-JFIF files with `.jfif` extensions.

## Author

[Your Name/Organization] (if applicable)
