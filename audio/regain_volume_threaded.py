import os
import sys
import signal
from pydub import AudioSegment
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global flag to signal threads to stop
stop_flag = False

def calculate_average_amplitude(audio):
    raw_data = np.array(audio.get_array_of_samples())
    return np.mean(np.abs(raw_data))

def calculate_max_amplitude(audio):
    raw_data = np.array(audio.get_array_of_samples())
    return np.max(np.abs(raw_data))

def calculate_required_gain(current_avg, target_avg=8000):
    return 20 * np.log10(target_avg / current_avg)

def amplify_audio(file_path, target_avg=8000, bitrate="256k"):
    global stop_flag
    if stop_flag:
        return
    try:
        # Load the audio file
        audio = AudioSegment.from_file(file_path)
        
        # Calculate the current average and max amplitude
        current_avg = calculate_average_amplitude(audio)
        current_max = calculate_max_amplitude(audio)
        
        # Calculate the required gain in dB
        required_gain_db = calculate_required_gain(current_avg, target_avg)
        
        # Ensure we do not exceed the max amplitude
        max_possible_gain = 20 * np.log10(32767 / current_max)  # 32767 is the max amplitude for 16-bit audio
        if required_gain_db > max_possible_gain:
            required_gain_db = max_possible_gain
        
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
        print(f"Current max amplitude: {current_max:.2f}")
        print(f"Required gain: {required_gain_db:.2f} dB")
        print(f"Amplified file saved to: {new_file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_folder(folder_path, target_avg=8000, bitrate="256k", max_workers=4):
    global stop_flag
    files_to_process = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                files_to_process.append(file_path)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(amplify_audio, file_path, target_avg, bitrate) for file_path in files_to_process]
        try:
            for future in as_completed(futures):
                if stop_flag:
                    break
                future.result()  # This will raise any exceptions that occurred during processing
        except KeyboardInterrupt:
            stop_flag = True
            print("\nProcess interrupted by user. Shutting down...")
            for future in futures:
                future.cancel()

def signal_handler(sig, frame):
    global stop_flag
    print("\nCtrl+C received. Stopping...")
    stop_flag = True

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    if len(sys.argv) not in [2, 3, 4, 5]:
        print("Usage: python script.py <file_or_folder_path> [target_avg] [bitrate] [max_workers]")
        sys.exit(1)

    path = sys.argv[1]
    target_avg = 8000 if len(sys.argv) < 3 else float(sys.argv[2])
    bitrate = "256k" if len(sys.argv) < 4 else sys.argv[3]
    max_workers = 4 if len(sys.argv) < 5 else int(sys.argv[4])

    if os.path.isfile(path):
        amplify_audio(path, target_avg, bitrate)
    elif os.path.isdir(path):
        process_folder(path, target_avg, bitrate, max_workers)
    else:
        print(f"The path '{path}' is neither a file nor a folder.")
        sys.exit(1)