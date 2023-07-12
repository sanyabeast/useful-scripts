import os
import glob
import random


def randomize_array(arr):
    random.shuffle(arr)
    return arr


def remove_spaces(input_string):
    # Remove leading and trailing spaces
    stripped_string = input_string.strip()
    # Remove multiple spaces
    no_extra_spaces_string = ' '.join(stripped_string.split())
    return no_extra_spaces_string


def create_playlist(directory, recursive):
    """Creates a .m3u8 playlist for each directory containing .m4a or .mp3 files.

    Args:
        directory (str): The path of the directory to search.
        recursive (bool): Whether to search through subdirectories.

    """

    root_directory = directory

    if recursive:
        # Use os.walk to go through the directory and all its subdirectories
        for root, dirs, files in os.walk(directory):
            create_playlist_in_directory(root_directory, root)
    else:
        create_playlist_in_directory(root_directory, directory)


def create_playlist_in_directory(root_directory, directory):
    """Creates a .m3u8 playlist in the directory if it contains .m4a or .mp3 files.

    Args:
        directory (str): The path of the directory to search.

    """
    # Use glob to find .m4a and .mp3 files in the current directory
    audio_files = glob.glob(os.path.join(directory, '*.m4a')) + \
        glob.glob(os.path.join(directory, '*.mp3'))

    audio_files = randomize_array(audio_files)

    # If there are any audio files in the current directory
    if audio_files:
        # Create a .m3u8 file in the current directory
        # playlist_name = f"{os.path.basename(directory)} ({remove_denied_symbols(directory.replace(root_directory, ''))}).m3u8"

        prefix = directory.replace(root_directory, '').replace(
            os.path.basename(directory), '').lstrip("/").lstrip("\\")

        prefix = prefix.replace(
            "/", ", ").replace("\\", ", ").replace(":", "-")

        playlist_name = f"{remove_spaces(prefix).lower()} - {os.path.basename(directory).upper()}.m3u8"

        print(prefix)
        if (prefix == ""):
            playlist_name = f"{os.path.basename(directory).upper()}.m3u8"

        playlist_path = os.path.join(
            root_directory, playlist_name)

        print(f'Creating playlist {playlist_path}')

        # Write the paths of the audio files to the .m3u8 file
        with open(playlist_path, 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            for audio_file in audio_files:
                # Write the path relative to the playlist file
                f.write(audio_file + '\n')

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
