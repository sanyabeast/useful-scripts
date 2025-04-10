from pydub import AudioSegment
import sys
import glob
import os

def measure_volume(audio_file):
    # Load the audio file
    print("file: " + audio_file)
    sound = AudioSegment.from_file(audio_file)

    # Calculate the max, min, and average volume
    max_volume = sound.max
    min_volume = sound.min
    average_volume = sound.rms

    return max_volume, min_volume, average_volume

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python measure_volume.py <working_directory>")
        sys.exit(1)
        
    extension_list = ('*.m4a', '*.mp3')

    working_directory = sys.argv[1]
    os.chdir(working_directory)   

    for extension in extension_list:
        for audio_file in glob.glob(extension):
            clean_name = os.path.splitext(os.path.basename(audio_file))[0] + '.mp3'
            max_volume, min_volume, average_volume = measure_volume(audio_file)

            print(f"Max volume: {max_volume} dB")
            print(f"Min volume: {min_volume} dB")
            print(f"Average volume: {average_volume} dB")


    
    