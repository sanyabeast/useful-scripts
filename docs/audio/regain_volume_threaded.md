# regain_volume_threaded.py

regain_volume_threaded.py - Audio Volume Enhancement Script with Threading

This script enhances the volume of audio files (MP3 format) by calculating and applying gain based on average amplitude.
It utilizes multi-threading for faster processing, especially when handling multiple files or large folders.

The script is designed to prevent clipping by limiting the maximum possible gain applied to each file. It saves the processed files into a 'regained' subfolder within the original directory.

**Dependencies:**
*   `pydub`: For audio processing (installation: `pip install pydub`) - Requires FFmpeg or Libav installed and accessible in your system's PATH.
*   `numpy`: For numerical calculations (installation: `pip install numpy`)

**Author:** [Your Name/Team Name]
**Version:** 1.0
**Date:** October 26, 2023
