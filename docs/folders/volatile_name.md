# volatile_name.py

README for volatile_name.py

This script renames folders within a specified directory that start with a given prefix to new, randomly generated names while ensuring uniqueness.

**Purpose:** The primary purpose of this script is to rename folders in a directory based on a provided prefix and generate unique random names for them. This can be useful for scenarios where you need to quickly change the names of multiple directories without manual intervention, especially when dealing with temporary or 'volatile' data.

## Main Components & Logic:

The script consists of the following key components:

1.  **`rename_folder(dir_path, name_prefix)` Function:** This is the core function that performs the renaming operation.
    *   It takes two arguments: `dir_path` (the path to the directory containing the folders) and `name_prefix` (a string prefix that target folder names must start with).
    *   **Folder Listing & Filtering:** It lists all entries within the specified directory using `os.listdir()` and filters them down to only those that are directories (`os.path.isdir()`).  It then further filters this list to identify folders whose names begin with the provided `name_prefix`. 
    *   **Error Handling:** Includes a try-except block to catch potential exceptions during file system operations.
    *   **Unique Name Generation:** For each folder matching the prefix, it generates a new name by appending a random integer between 1 and 9,999,999 to the `name_prefix`.  It ensures that the generated name is unique within the directory by repeatedly generating names until one not already in use is found. 
    *   **Renaming:** It uses `os.rename()` to rename the folder from its original name to the newly generated name.

2.  **Main Execution Block (`if __name__ == '__main__':`)**: This block handles command-line argument parsing and calls the `rename_folder` function.
    *   It checks if exactly two arguments (directory path and prefix) are provided via the command line.
    *   If not, it prints a usage message. 
    *   Otherwise, it extracts the directory path and prefix from the command-line arguments and passes them to `rename_folder`.

## Assumptions & Requirements:

*   **Python Environment:** Requires Python 3 installed on the system.
*   **Permissions:** The script must have write permissions within the specified `dir_path`.  If it doesn't, renaming operations will fail.
*   **Directory Existence:** The provided `dir_path` must exist. If not, an error will occur.
*   **Uniqueness Guarantee:** While the script attempts to generate unique names, there is a *very small* theoretical possibility of name collisions if the directory contains a very large number of folders and the random number generator produces duplicates (highly unlikely with the range used).

## Limitations:

*   **No Recursion:** The script only operates on folders directly within the specified `dir_path`. It does not recursively process subdirectories.
*   **Simple Prefix Matching:**  The prefix matching is a simple string comparison (`f.startswith(name_prefix)`). More complex pattern matching (e.g., regular expressions) is not supported.
*   **Error Handling:** The error handling is basic and only prints the exception message. More sophisticated logging or error recovery mechanisms could be added.

## Example Use Cases:

1.  **Renaming Temporary Folders:** You have a directory containing folders named `tmp_data_1`, `tmp_data_2`, etc., and you want to rename them to something more generic like `vol_0000001`, `vol_0000002`. 
    ```bash
    python volatile_name.py /path/to/temp/directory tmp_data_
    ```

2.  **Cleaning Up Staging Folders:** You have a staging directory with folders named `stage_file1`, `stage_file2`, and you want to rename them to something like `vol_1234567`.
    ```bash
    python volatile_name.py /path/to/staging/directory stage_
    ```

## Usage:

To run the script, use the following command-line syntax:

```bash
python volatile_name.py <directory_path> <name_prefix>
```

*   `<directory_path>`: The path to the directory containing the folders you want to rename.
*   `<name_prefix>`:  The prefix that the target folder names must start with.

**Example:**

Suppose you have a directory `/tmp/my_data` and you want to rename all folders starting with `backup_` to new, unique names. You would run:

```bash
python volatile_name.py /tmp/my_data backup_
```

The script will then print messages indicating which folders were renamed.

## Additional Notes:

*   **Backup:** It is *highly recommended* to back up the directory before running this script, as renaming operations are irreversible without a backup. 
*   **Testing:** Test the script on a small sample directory first to ensure it behaves as expected before applying it to a large or critical dataset.
