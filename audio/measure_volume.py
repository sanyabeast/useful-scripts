import os
import sys
from pydub import AudioSegment
import numpy as np

def calculate_volume_levels(file_path):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)
    
    # Convert audio to raw data
    raw_data = np.array(audio.get_array_of_samples())
    
    # Calculate the average volume
    average_amplitude = np.mean(np.abs(raw_data))
    
    # Calculate the min and max volume in amplitude
    min_amplitude = np.min(raw_data)
    max_amplitude = np.max(raw_data)

    print(average_amplitude, min_amplitude, max_amplitude)
    
    # Convert amplitudes to decibels
    bit_depth = audio.sample_width * 8
    max_possible_amplitude = 2 ** (bit_depth - 1) - 1
    average_volume_db = 20 * np.log10(average_amplitude / max_possible_amplitude)
    min_volume_db = 20 * np.log10(np.abs(min_amplitude) / max_possible_amplitude)
    max_volume_db = 20 * np.log10(np.abs(max_amplitude) / max_possible_amplitude)
    
    return average_volume_db, min_volume_db, max_volume_db

def process_file(file_path):
    avg_volume_db, min_volume_db, max_volume_db = calculate_volume_levels(file_path)
    print(f"File: {file_path}")
    print(f"Average volume level: {avg_volume_db:.2f} dB")
    print(f"Minimum volume level: {min_volume_db:.2f} dB")
    print(f"Maximum volume level: {max_volume_db:.2f} dB\n")

def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_or_folder_path>")
        sys.exit(1)

    path = sys.argv[1]

    if os.path.isfile(path):
        process_file(path)
    elif os.path.isdir(path):
        process_folder(path)
    else:
        print(f"The path '{path}' is neither a file nor a folder.")
        sys.exit(1)