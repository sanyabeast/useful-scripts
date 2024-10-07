
**Merge Audio Video**
=====================

A Python script that merges audio and video files with the same name in an input folder and saves the merged files to an output folder.

**Usage**

1. Run the script from the command line: `python merge_audio_video.py /path/to/input_folder /path/to/output_folder`
2. The script will iterate through each pair of audio (`.m4a`) and video (`.mp4` or `.webm`) files with the same name in the input folder.
3. It will then merge the audio and video files using MoviePy, a Python library for video editing.

**Options**

* `output_extension`: The file extension to use for the merged output files (default: `mkv`)
* `video_codec`, `audio_codec`, `video_bitrate`, `audio_bitrate`, `threads_count`: These options control the encoding settings used by MoviePy. You can adjust them as needed.

**Example**

Suppose you have an input folder containing audio and video files named `example.mp4` and `example.m4a`. Running the script with the command `python merge_audio_video.py /path/to/input_folder /path/to/output_folder` would create a merged file called `example.mkv` in the output folder.