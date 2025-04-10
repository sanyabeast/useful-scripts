# python merge_audio_video.py /path/to/input_folder /path/to/output_folder
# This will merge each pair of audio and video files 
# with the same name in the input folder and save the merged files to the output folder.

import os
from moviepy.editor import VideoFileClip, AudioFileClip
import argparse

output_extension="mkv"

video_codec="libx265"
video_bitrate="16m"

audio_codec="aac"
audio_bitrate="128k"

threads_count=16

def merge_audio_video(video_file, audio_file, output_folder):
    global video_codec
    global video_bitrate

    global audio_codec
    global audio_bitrate

    global threads_count
    global output_extension

    video_name = os.path.splitext(os.path.basename(video_file))[0]

    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)
    
    video_clip = video_clip.set_audio(audio_clip)
    
    video_clip.write_videofile(os.path.join(output_folder, video_name + "." + output_extension), threads=threads_count, codec=video_codec, fps=video_clip.fps, preset='superfast', audio_codec=audio_codec, audio_bitrate=audio_bitrate, bitrate=video_bitrate)
    
def merge_audio_video_pairs(input_folder, output_folder):
    for video_file in os.listdir(input_folder):
        if video_file.endswith(".mp4") or video_file.endswith(".webm"):
            video_name = os.path.splitext(video_file)[0]
            audio_file = os.path.join(input_folder, video_name + ".m4a")
            if os.path.exists(audio_file):
                merge_audio_video(os.path.join(input_folder, video_file), audio_file, output_folder)
                print(f"Merged {video_file} with {os.path.basename(audio_file)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge audio and video files.")
    parser.add_argument("input_folder", help="Input folder containing video and audio files.")
    parser.add_argument("output_folder", help="Output folder for merged files.")
    args = parser.parse_args()

    merge_audio_video_pairs(args.input_folder, args.output_folder)