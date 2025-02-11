**dir_to_m3u8.py**
==================

A Python script that creates .m3u8 playlists from directories containing .m4a or .mp3 files.

### Usage

To use this script, simply run it and provide the path to the directory you want to convert as an argument. You can also specify whether to search through subdirectories using the `-r` flag.

Example:
```
python dir_to_m3u8.py /path/to/directory [-r]
```

### Options

* `directory`: The path of the directory to convert.
* `-r`, `--recursive`: Whether to search through subdirectories. (Default: False)

### Features

This script includes a few features:

* Randomizes the order of audio files in each playlist
* Creates .m3u8 playlists for each directory containing .m4a or .mp3 files
* Writes the paths of the audio files relative to the playlist file, making it easier to manage your media library

### Notes

The script uses the `os` module to walk through directories, the `glob` module to find audio files, and the `random` module to randomize their order. It also includes some string manipulation functions to create more interesting playlist names.