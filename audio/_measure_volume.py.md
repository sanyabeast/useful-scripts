**Measure Volume**

This Python script measures the volume levels of audio files in decibels (dB). It uses the `pydub` library to load and process audio files, and NumPy for numerical computations.

The script can be used to analyze a single file or an entire folder containing multiple audio files. When run with a file path as input, it calculates the average volume level, minimum volume level, and maximum volume level of that file in decibels (dB). The results are printed to the console.

When run with a directory path as input, the script processes all MP3 files within that folder and its subfolders. For each file, it calculates the same three volume levels and prints them to the console.

**Example Usage**

To measure the volume level of a single audio file:
```
python measure_volume.py /path/to/file.mp3
```

To process an entire directory containing multiple MP3 files:
```
python measure_volume.py /path/to/folder/
```

In both cases, the script will print the average, minimum, and maximum volume levels for each file in decibels (dB).

**Note**

This script assumes that all audio files are in MP3 format. If you want to support other formats as well, you'll need to modify the script accordingly.

Also, keep in mind that this is a simple volume measurement tool and may not provide accurate results for all types of audio content.