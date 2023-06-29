import os
import glob
from xml.dom.minidom import Document


def create_playlist(directory, recursive):
    """Creates a .xspf playlist for each directory containing .m4a or .mp3 files.

    Args:
        directory (str): The path of the directory to search.
        recursive (bool): Whether to search through subdirectories.

    """
    if recursive:
        # Use os.walk to go through the directory and all its subdirectories
        for root, dirs, files in os.walk(directory):
            try:
                create_playlist_in_directory(root)
            except Exception as e:
                print(f'failed to create playlist in {root}; {e}')
    else:
        try:
            create_playlist_in_directory(directory)
        except Exception as e:
            print(f'failed to create playlist in {directory}; {e}')


def create_playlist_in_directory(directory):
    """Creates a .xspf playlist in the directory if it contains .m4a or .mp3 files.

    Args:
        directory (str): The path of the directory to search.

    """
    # Use glob to find .m4a and .mp3 files in the current directory
    audio_files = glob.glob(os.path.join(directory, '*.m4a')) + \
        glob.glob(os.path.join(directory, '*.mp3'))

    # If there are any audio files in the current directory
    if audio_files:
        # Create a .xspf file in the current directory
        playlist_name = os.path.basename(directory) + '.xspf'
        playlist_path = os.path.join(directory, playlist_name)

        print(f'Creating playlist {playlist_path}')

        # Create an XML document and define the root element
        doc = Document()
        playlist = doc.createElement('playlist')
        playlist.setAttribute('version', '1')
        playlist.setAttribute('xmlns', 'http://xspf.org/ns/0/')
        doc.appendChild(playlist)

        # Define the trackList element
        tracklist = doc.createElement('trackList')
        playlist.appendChild(tracklist)

        # Add each audio file to the trackList
        for audio_file in audio_files:
            # Define the track and location elements
            track = doc.createElement('track')
            location = doc.createElement('location')

            # Write the path relative to the playlist file
            location.appendChild(doc.createTextNode(
                os.path.relpath(audio_file, directory)))
            track.appendChild(location)

            # Add the track to the trackList
            tracklist.appendChild(track)

        # Write the XML document to the .xspf file
        with open(playlist_path, 'w', encoding='utf-8') as f:
            f.write(doc.toprettyxml(indent="  "))

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
