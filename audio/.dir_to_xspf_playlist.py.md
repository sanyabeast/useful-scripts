
**dir_to_xspf_playlist.py**
==========================

A Python script that creates .xspf playlists from directories containing .m4a or .mp3 files.

### Usage

To use this script, simply run it and provide the path to the directory you want to convert as an argument. You can also specify whether to search through subdirectories by adding the `-r` flag (e.g., `python dir_to_xspf_playlist.py /path/to/directory -r`).

### Description

This script creates a .xspf playlist for each directory containing .m4a or .mp3 files. The playlists are created in XML format and include information about each audio file, such as its path relative to the playlist.

The script uses the `glob` module to find all .m4a and .mp3 files in a given directory (and its subdirectories if specified) and then creates an XML document using the `xml.dom.minidom` module. The XML document is written to a file with the same name as the directory, but with a `.xspf` extension.

### Example

Here's an example of how you can use this script:
```
python dir_to_xspf_playlist.py /path/to/music -r
```
This will create .xspf playlists for each subdirectory in `/path/to/music`, including the paths to all .m4a and .mp3 files.

### Notes

* This script assumes that you have the `xml` module installed. If not, you can install it using pip: `pip install xml`
* The script does not handle errors well, so be careful when running it.
* You may want to modify the script to include additional information in the XML document, such as song titles or artist names.