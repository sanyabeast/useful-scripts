import os
import sys
from pydub import AudioSegment, effects

def normalize_audio(input_path, output_dir):
    # Check if input_path is a directory or a file
    if os.path.isdir(input_path):
        # If it's a directory, normalize all audio files in the directory
        for file_name in os.listdir(input_path):
            file_path = os.path.join(input_path, file_name)
            if os.path.isfile(file_path) and any(file_name.lower().endswith(ext) for ext in ['.ogg', '.m4a', '.mp3']):
                normalize_audio_file(file_path, output_dir)
    elif os.path.isfile(input_path):
        # If it's a file, normalize only that file
        normalize_audio_file(input_path, output_dir)
    else:
        print("Invalid input path:", input_path)

def normalize_audio_file(input_file, output_dir):
    # Load the audio file
    sound = AudioSegment.from_file(input_file)
    print(sound)

    # Normalize the audio
    normalized_sound = effects.normalize(sound)

    # Set output file name
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + ".m4a")
    print(f"rendering result to: {output_file}")

    # Export the normalized audio with 128 bitrate
    normalized_sound.export(output_file, format="mp3", bitrate="256k")
    print("Normalized audio saved to:", output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python normalize_audio.py <output_directory> <path_to_audio_file_or_directory> ")
        sys.exit(1)

    output_dir = sys.argv[1]
    
    input_path = sys.argv[2]

    print(f"input: {input_path}, output: {output_dir}")
    
    # Check if output directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    normalize_audio(input_path, output_dir)