import os
import glob


def create_playlist(directory, recursive):
    """Creates a .m3u playlist for each directory containing .m4a or .mp3 files.

    Args:
        directory (str): The path of the directory to search.
        recursive (bool): Whether to search through subdirectories.

    """
    if recursive:
        # Use os.walk to go through the directory and all its subdirectories
        for root, dirs, files in os.walk(directory):
            create_playlist_in_directory(root)
    else:
        create_playlist_in_directory(directory)


def create_playlist_in_directory(directory):
    """Creates a .m3u playlist in the directory if it contains .m4a or .mp3 files.

    Args:
        directory (str): The path of the directory to search.

    """
    # Use glob to find .m4a and .mp3 files in the current directory
    audio_files = glob.glob(os.path.join(directory, '*.m4a')) + \
        glob.glob(os.path.join(directory, '*.mp3'))

    # If there are any audio files in the current directory
    if audio_files:
        # Create a .m3u file in the current directory
        playlist_name = os.path.basename(directory) + '.m3u'
        playlist_path = os.path.join(directory, playlist_name)

        print(f'Creating playlist {playlist_path}')

        # Write the paths of the audio files to the .m3u file
        with open(playlist_path, 'w') as f:
            for audio_file in audio_files:
                # Write the path relative to the playlist file
                f.write(os.path.relpath(audio_file, directory) + '\n')

        print(f'Successfully created playlist {playlist_path}')
    else:
        print(f'No audio files found in {directory}')


if __name__ == '__main__':
    import sys

    # Expecting the directory and a boolean for whether to search subdirectories as command-line arguments
    if len(sys.argv) == 1:
        print(f'Usage: {sys.argv[0]} DIRECTORY [-r]')
    elif len(sys.argv) == 2:
        create_playlist(sys.argv[1], False)
    else:
        create_playlist(sys.argv[1], True)
