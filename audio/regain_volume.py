import os
import sys
from pydub import AudioSegment
import numpy as np

def calculate_average_amplitude(audio):
    raw_data = np.array(audio.get_array_of_samples())
    return np.mean(np.abs(raw_data))

def calculate_required_gain(current_avg, target_avg=8000):
    return 20 * np.log10(target_avg / current_avg)

def amplify_audio(file_path, target_avg=8000, bitrate="256k"):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)
    
    # Calculate the current average amplitude
    current_avg = calculate_average_amplitude(audio)
    
    # Calculate the required gain in dB
    required_gain_db = calculate_required_gain(current_avg, target_avg)
    
    # Amplify the audio
    amplified_audio = audio + required_gain_db
    
    # Create the 'regained' subfolder if it doesn't exist
    regained_folder = os.path.join(os.path.dirname(file_path), "regained")
    os.makedirs(regained_folder, exist_ok=True)
    
    # Save the amplified audio to the 'regained' subfolder with the original file name
    new_file_path = os.path.join(regained_folder, os.path.basename(file_path))
    amplified_audio.export(new_file_path, format="mp3", bitrate=bitrate)
    
    print(f"File: {file_path}")
    print(f"Current average amplitude: {current_avg:.2f}")
    print(f"Required gain: {required_gain_db:.2f} dB")
    print(f"Amplified file saved to: {new_file_path}")

def process_folder(folder_path, target_avg=8000, bitrate="256k"):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                amplify_audio(file_path, target_avg, bitrate)

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3, 4]:
        print("Usage: python script.py <file_or_folder_path> [target_avg] [bitrate]")
        sys.exit(1)

    path = sys.argv[1]
    target_avg = 8000 if len(sys.argv) < 3 else float(sys.argv[2])
    bitrate = "256k" if len(sys.argv) < 4 else sys.argv[3]

    if os.path.isfile(path):
        amplify_audio(path, target_avg, bitrate)
    elif os.path.isdir(path):
        process_folder(path, target_avg, bitrate)
    else:
        print(f"The path '{path}' is neither a file nor a folder.")
        sys.exit(1)