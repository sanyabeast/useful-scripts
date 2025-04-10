# dir_to_m3u.py

dir_to_m3u.py - Creates .m3u playlists for directories containing audio files (mp3 and m4a). 

This script automatically generates `.m3u` playlist files within directories that contain `.mp3` or `.m4a` audio files.  It can operate on a single directory or recursively search through subdirectories.

**Author:** [Your Name/Team Name - Replace this] 
**Version:** 1.0
**Date:** October 26, 2023 (or current date)

## Overview

The `dir_to_m3u.py` script is a simple utility designed to create `.m3u` playlist files for directories containing audio files.  It searches for `.mp3` and `.m4a` files within the specified directory (and its subdirectories if requested) and creates a corresponding `.m3u` file in each directory where audio files are found. The paths listed in the .m3u file are relative to the location of the playlist itself.

## Main Components & Logic

The script is structured into three main functions:

*   **`create_playlist(directory, recursive)`:** This is the primary function that orchestrates the playlist creation process. It takes the directory path and a boolean flag (`recursive`) as input. If `recursive` is True, it uses `os.walk()` to traverse all subdirectories within the given directory. Otherwise, it processes only the specified directory.
*   **`create_playlist_in_directory(directory)`:** This function handles the creation of a single `.m3u` playlist file for a specific directory. It first searches for `.mp3` and `.m4a` files using `glob.glob()`. If audio files are found, it creates a `.m3u` file with the same name as the directory (e.g., 'MyMusic.m3u') in that directory. The script then writes the relative paths of each audio file to the playlist.
*   **`if __name__ == '__main__':`:** This block handles command-line argument parsing and calls the `create_playlist()` function with the provided arguments.

## Assumptions, Requirements & Limitations

*   **Python Version:** Requires Python 3.x (tested with [Specify version if tested]).
*   **Dependencies:**  The script only uses built-in Python modules (`os` and `glob`), so no external libraries need to be installed.
*   **File Types:** Currently supports only `.mp3` and `.m4a` audio files. Adding support for other formats would require modifying the `glob.glob()` patterns in `create_playlist_in_directory()`. 
*   **Relative Paths:** The script writes relative paths to the .m3u file. This means that if you move the playlist or the audio files, the links in the playlist might break unless the directory structure is preserved.
*   **Error Handling:**  The script lacks robust error handling (e.g., checking for invalid directory paths). It assumes that the provided directory exists and is accessible.
*   **Overwriting:** If a `.m3u` file with the same name already exists in a directory, it will be overwritten without warning.

## Example Use Cases

1.  **Create a playlist for a single directory:**
    ```bash
    python dir_to_m3u.py /path/to/my/music
    ```
    This command creates a `music.m3u` file (assuming the directory is named 'music') in `/path/to/my/music`, containing relative paths to all `.mp3` and `.m4a` files within that directory.

2.  **Create playlists for all subdirectories recursively:**
    ```bash
    python dir_to_m3u.py /path/to/my/music -r
    ```
    This command creates a `.m3u` file in *every* directory under `/path/to/my/music` that contains at least one `.mp3` or `.m4a` file.

## Usage Instructions

The script is executed from the command line. The syntax is as follows:

```bash
python dir_to_m3u.py DIRECTORY [-r]
```

*   **DIRECTORY:**  The path to the directory you want to process.
*   **-r (optional):** A flag that indicates whether to search recursively through subdirectories. If omitted, only the specified directory is processed.

## Additional Notes

*   The script prints messages to the console indicating which playlists are being created and if any directories contain no audio files.
*   Consider adding error handling for production use cases (e.g., checking if a directory exists before attempting to process it).
*   For more complex playlist generation requirements (e.g., sorting, filtering), consider using a dedicated playlist management tool or library.

## Contributing

Contributions are welcome! Please submit pull requests with clear descriptions of the changes you've made.
