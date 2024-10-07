**dir_to_m3u**
================

A Python script that creates .m3u playlists from directories containing .m4a or .mp3 files.

### Usage

To use this script, simply run it and provide the path to the directory you want to convert as an argument. You can also specify whether to search through subdirectories using the `-r` flag.

Example:
```
python dir_to_m3u.py /path/to/directory [-r]
```

### Options

* `directory`: The path of the directory to convert.
* `-r`, `--recursive`: Whether to search through subdirectories. (Default: False)

### Output

The script will create a .m3u file in each directory containing .m4a or .mp3 files, with the paths relative to that playlist.

### Notes

This script assumes that all audio files are either .m4a or .mp3 format. If you have other formats and want them included in the playlists, please modify the `create_playlist` function accordingly.