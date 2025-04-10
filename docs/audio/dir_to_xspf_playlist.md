# dir_to_xspf_playlist.py

dir_to_xspf_playlist.py - Generates XSPF Playlists from Audio Files

This script automatically generates XSPF (XML Playlist Sequential File Format) playlists for directories containing audio files (.m4a and .mp3). It's designed to be a simple solution for creating playlists that can be used by various media players.

**Author:** [Your Name/Team Name]
**Version:** 1.0
**Date:** October 26, 2023

## Overview

The `dir_to_xspf_playlist.py` script scans a specified directory (and optionally its subdirectories) for `.m4a` and `.mp3` audio files. For each directory containing these files, it creates an XSPF playlist file (`[directory_name].xspf`) within that same directory. The playlist contains relative paths to the audio files found.

## Main Components & Logic

The script is structured into three main functions:

*   **`create_playlist(directory, recursive)`:** This is the primary function called to initiate the playlist generation process. It takes the directory path and a boolean flag (`recursive`) as input. If `recursive` is True, it uses `os.walk()` to traverse all subdirectories within the specified directory. Otherwise, it only processes the top-level directory.
*   **`create_playlist_in_directory(directory)`:** This function handles the creation of a single XSPF playlist for a given directory. It searches for `.m4a` and `.mp3` files using `glob.glob()`, creates an XML document representing the XSPF playlist, adds track entries with relative file paths, and saves the playlist to a file.
*   **`if __name__ == '__main__':`:** This block handles command-line argument parsing and calls the `create_playlist()` function based on user input. It checks for the correct number of arguments (directory path and optional recursive flag).

## Assumptions, Requirements & Limitations

*   **Python Version:** Requires Python 3.x.
*   **Dependencies:**  No external libraries are required beyond the Python standard library (`os`, `glob`, `xml.dom.minidom`).
*   **Audio File Types:** Currently supports only `.m4a` and `.mp3` audio files. Adding support for other formats would require modifying the `glob.glob()` patterns.
*   **Relative Paths:** The playlist file contains relative paths to the audio files, based on the directory where the playlist is created. This means that if you move the playlist or audio files, the links in the playlist might break.
*   **Error Handling:** Basic error handling is included (printing errors to the console), but more robust error management could be implemented for production use.
*   **File Encoding:** The script writes the XML file using UTF-8 encoding. This ensures compatibility with a wider range of characters in filenames.

## Example Use Cases

1.  **Generate a playlist for a single directory:**
    ```bash
    python dir_to_xspf_playlist.py /path/to/my/music
    ```
    This will create `my_music.xspf` in the `/path/to/my/music` directory.

2.  **Generate playlists for all subdirectories recursively:**
    ```bash
    python dir_to_xspf_playlist.py /path/to/my/music -r
    ```
    This will create `.xspf` files in each subdirectory of `/path/to/my/music` that contains audio files.

## Usage Instructions

1.  **Save the script:** Save the code as `dir_to_xspf_playlist.py`.
2.  **Run from the command line:** Open a terminal or command prompt and navigate to the directory where you saved the script.
3.  **Execute the script:** Use one of the example commands above, replacing `/path/to/my/music` with the actual path to your music directory.

## Additional Notes

*   The script prints messages to the console indicating which playlists are being created and any errors encountered.
*   You can modify the `glob.glob()` patterns in the `create_playlist_in_directory()` function to support additional audio file types.
*   For more complex playlist generation requirements (e.g., sorting, metadata extraction), consider using a dedicated playlist management library or tool.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please submit an issue or pull request on [link to your repository, if applicable].
