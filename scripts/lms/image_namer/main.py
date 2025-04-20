#!/usr/bin/env python3
"""
Usage:
    python rename_images_with_llm.py --folder "H:/Pictures" --model "gemma-3-4b-it"
        [--min-length 32] [--max-length 128] [--recursive] [--force] [--threshold 0.5]

This script walks through the given folder and renames each image file
based on a filename suggested by an LLM. When --recursive is specified, it will
include nested folders. The LLM rates the current filename's descriptiveness (0-1),
and files with scores above the threshold (default: 0.5) keep their names.
Use --force to rename all files regardless of their current name quality.
It skips files if the new name already exists, preserves the original file extension,
and logs progress to the console.
"""

import argparse
from pathlib import Path
import lmstudio as lms
from pydantic import BaseModel
import mimetypes
import signal
import sys


class ImageDescription(BaseModel):
    suggested_filename: str
    current_name_descriptiveness: float


def is_image_file(file_path):
    mime, _ = mimetypes.guess_type(file_path)
    return mime is not None and mime.startswith("image")


def signal_handler(sig, frame):
    print("\n\n⚠️ Ctrl+C detected. Exiting gracefully...")
    print("👋 Goodbye!")
    sys.exit(0)


def main():
    # Set up signal handler for graceful exit on Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(description="Rename images in a folder using LLM-generated filenames.")
    parser.add_argument("--folder", required=True, help="Path to the folder containing images")
    parser.add_argument("--model", required=True, help="Model name to use for filename generation")
    parser.add_argument("--min-length", type=int, default=32, help="Minimum filename length (default: 32)")
    parser.add_argument("--max-length", type=int, default=128, help="Maximum filename length (default: 64)")
    parser.add_argument("--recursive", action="store_true", help="Include nested folders in the search")
    parser.add_argument("--force", action="store_true", help="Force renaming all files regardless of LLM's assessment")
    parser.add_argument("--threshold", type=float, default=0.5, help="Threshold for keeping original filename (0-1, default: 0.5)")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.exists() or not folder.is_dir():
        print("❌ Error: Provided folder does not exist or is not a directory.")
        return

    print(f"🤖 Loading model: {args.model}...")
    model = lms.llm(args.model)
    print(f"✅ Model loaded successfully!")
    
    print(f"📂 Scanning folder: {folder.resolve()}")

    # Use glob or rglob based on the recursive flag
    if args.recursive:
        print(f"🔍 Searching recursively through all nested folders")
        image_files = [f for f in folder.rglob("*") if f.is_file() and is_image_file(f)]
    else:
        print(f"🔍 Searching only in the top-level folder")
        image_files = [f for f in folder.glob("*") if f.is_file() and is_image_file(f)]
    
    total_images = len(image_files)

    if not image_files:
        print("⚠️ No image files found.")
        return

    print(f"🖼️ Found {total_images} image(s). Starting renaming process...\n")
    if args.force:
        print(f"⚠️ Force mode enabled: All files will be renamed regardless of current name quality")
    else:
        print(f"ℹ️ Threshold set to {args.threshold}: Files with descriptiveness scores above this will keep their names")

    success_count = 0
    skip_count = 0
    error_count = 0
    kept_count = 0

    for idx, image_path in enumerate(image_files, start=1):
        try:
            current_filename = image_path.stem
            print(f"🔄 [{idx}/{total_images}] Processing: {image_path}")
            
            print(f"  📊 Analyzing image content...")
            image_handle = lms.prepare_image(str(image_path))
            chat = lms.Chat()

            prompt = f"""
Describe this image and suggest a filename for it.
The current filename is: "{current_filename}"

First, carefully analyze if the current filename is already descriptive and appropriate:
1. Does it accurately describe what's in the image?
2. Is it using appropriate snake_case format?
3. Is it descriptive enough without being excessively long?

Generate a filename using lowercase snake_case format, with a minimum length of {args.min_length} characters and a maximum of {args.max_length} characters.
Do not include the file extension in the filename.
Do not use personal names.

Also, rate the descriptiveness of the current filename on a scale from 0.0 to 1.0:
- 0.0: Not descriptive at all (e.g., "IMG_1234", "DSC00001")
- 0.3: Somewhat descriptive but missing key elements
- 0.5: Moderately descriptive, captures basic content
- 0.7: Good description, captures most important elements
- 1.0: Excellent description, accurately captures all important elements

Return both the suggested_filename and current_name_descriptiveness fields.
"""

            chat.add_user_message(prompt, images=[image_handle])
            print(f"  💭 Generating filename suggestion...")
            prediction = model.respond(chat, response_format=ImageDescription)

            # Trim result to max length and clean formatting
            new_filename_base = prediction.parsed["suggested_filename"].strip()[:args.max_length]
            new_filename = new_filename_base + image_path.suffix.lower()
            new_filepath = image_path.with_name(new_filename)
            
            # Get the descriptiveness score of the current filename
            descriptiveness = prediction.parsed["current_name_descriptiveness"]
            
            # Decide whether to rename based on descriptiveness and force flag
            should_rename = args.force or descriptiveness < args.threshold
            
            if not should_rename:
                print(f"🔒 [{idx}/{total_images}] Kept original name: Score {descriptiveness:.2f} > threshold {args.threshold:.2f}\n")
                kept_count += 1
                continue

            if new_filepath.exists():
                print(f"⏭️ [{idx}/{total_images}] Skipped: {new_filename} already exists.\n")
                skip_count += 1
                continue

            print(f"  ✏️ Renaming file...")
            image_path.rename(new_filepath)
            print(f"🔄 [{idx}/{total_images}] Renamed to: {new_filename} (old name score: {descriptiveness:.2f})\n")
            success_count += 1

        except Exception as e:
            print(f"❌ [{idx}/{total_images}] Error processing {image_path.name}: {e}\n")
            error_count += 1

    print(f"📊 Summary:")
    print(f"  🔄 Successfully renamed: {success_count}")
    print(f"  🔒 Kept original name: {kept_count}")
    print(f"  ⏭️ Skipped (already exists): {skip_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"🎉 All done!")


if __name__ == "__main__":
    main()
