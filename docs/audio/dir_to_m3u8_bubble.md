# dir_to_m3u8_bubble.py

dir_to_m3u8_bubble.py - Generates M3U8 playlists for directories containing audio files (M4A and MP3). 

This script automatically creates `.m3u8` playlist files within each directory that contains `.m4a` or `.mp3` audio files. The playlist file names are derived from the directory path, making them descriptive and organized.

The order of songs in the playlists is randomized to provide a different listening experience each time.

**Note:** This script assumes relative paths for audio files within the generated M3U8 playlists.  The playlist will be created in the same directory as the audio files themselves.
