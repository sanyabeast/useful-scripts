# dir_to_m3u8.py

dir_to_m3u8.py - Generates M3U8 playlists for directories containing audio files.

This script automatically creates `.m3u8` playlist files within directories that contain `.m4a` or `.mp3` audio files. The order of the songs in the playlist is randomized. It can operate on a single directory or recursively search through subdirectories.

**Author:** [Your Name/Team Name]
**Version:** 1.0
**Date:** October 26, 2023

## Functionality Overview

The script's primary function is to scan a given directory (and optionally its subdirectories) for `.m4a` and `.mp3` files.  For each directory containing these audio file types, it generates an associated `.m3u8` playlist file. The playlist contains relative paths to the audio files within that directory.

## Main Components & Logic

The script is structured into several key functions:

*   **`randomize_array(arr)`:** Shuffles the order of elements in an array randomly using `random.shuffle()`. This ensures a randomized playlist order.
*   **`create_playlist(directory, recursive)`:**  The main entry point for creating playlists. It takes the directory path and a boolean flag (`recursive`) as input. If `recursive` is True, it iterates through all subdirectories using `os.walk()`. Otherwise, it processes only the specified directory.
*   **`create_playlist_in_directory(directory)`:**  This function handles the playlist creation for a single directory. It uses `glob.glob()` to find `.m4a` and `.mp3` files within the directory. The found audio files are then randomized using `randomize_array()`. A new `.m3u8` file is created in the same directory, containing the relative paths of the audio files prefixed with '#EXTM3U'.
*   **`if __name__ == '__main__':`:** This block handles command-line argument parsing and calls the `create_playlist()` function based on user input.

## Assumptions & Requirements

*   **Python Environment:** Requires Python 3.x to be installed.
*   **Operating System:**  Should work on any operating system with a standard file system (Windows, macOS, Linux).
*   **Audio File Types:** Currently supports only `.m4a` and `.mp3` audio files. Adding support for other formats would require modifying the `glob.glob()` patterns.
*   **Permissions:** The script needs read permissions to access the specified directory and write permissions to create the `.m3u8` file within that directory.
*   **Relative Paths:**  The generated playlists contain relative paths to the audio files. This means the playlist will only work correctly if the audio files are located relative to the location of the `.m3u8` file.

## Limitations

*   **No Error Handling:** The script lacks robust error handling (e.g., for permission errors, invalid directory paths).  It prints messages but doesn't explicitly handle exceptions.
*   **Limited Audio Format Support:** Only supports `.m4a` and `.mp3`. Expanding this would require adding more glob patterns.
*   **No Playlist Metadata:** The generated playlists only contain the file paths. They do not include any metadata (e.g., song titles, artist names).

## Example Use Cases

1.  **Create a playlist for a single directory:**
    ```bash
    python dir_to_m3u8.py /path/to/my/audio/directory
    ```
    This will create a file named `/path/to/my/audio/directory.m3u8` containing the relative paths of all `.m4a` and `.mp3` files in that directory.

2.  **Create playlists for all subdirectories recursively:**
    ```bash
    python dir_to_m3u8.py /path/to/my/audio/directory -r
    ```
    This will create a `.m3u8` file in *every* directory under `/path/to/my/audio/directory` that contains at least one `.m4a` or `.mp3` file.

## Usage Instructions

1.  **Save the script:** Save the code as `dir_to_m3u8.py`.
2.  **Run from the command line:** Open a terminal or command prompt and navigate to the directory where you saved the script.
3.  **Execute the script:** Use one of the example commands above, replacing `/path/to/my/audio/directory` with the actual path to your audio files.

## Future Enhancements

*   Implement more robust error handling and logging.
*   Add support for additional audio file formats (e.g., `.flac`, `.ogg`).
*   Allow users to specify a different output directory for the playlists.
*   Include playlist metadata (song titles, artist names) in the `.m3u8` files.
*   Provide options for customizing the playlist format and content.
*   Add command-line arguments for specifying input and output file extensions.

## Dependencies

*   Python 3.x
*   Standard Python library (no external packages required)
```
