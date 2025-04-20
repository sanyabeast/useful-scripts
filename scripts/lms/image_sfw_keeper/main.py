#!/usr/bin/env python3
"""
Usage:
    python remove_nsfw_images.py --folder "H:/Pictures" --model "gemma-3-4b-it" [--recursive]

This script scans images in a folder and removes those flagged by an LLM as NSFW.
When --recursive is specified, it will include nested folders in the search.
"""

import argparse
from pathlib import Path
import lmstudio as lms
from pydantic import BaseModel
import mimetypes
import os
import signal
import sys


class NSFWCheck(BaseModel):
    nsfw: bool


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
    
    parser = argparse.ArgumentParser(description="Remove NSFW images in a folder using LLM detection.")
    parser.add_argument("--folder", required=True, help="Path to the folder containing images")
    parser.add_argument("--model", required=True, help="Model name to use for NSFW detection")
    parser.add_argument("--recursive", action="store_true", help="Include nested folders in the search")

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

    print(f"🖼️ Found {total_images} image(s). Starting NSFW check...\n")

    safe_count = 0
    removed_count = 0
    error_count = 0

    for idx, image_path in enumerate(image_files, start=1):
        try:
            print(f"🔍 [{idx}/{total_images}] Checking: {image_path}")

            print(f"  📊 Analyzing image content...")
            image_handle = lms.prepare_image(str(image_path))
            chat = lms.Chat()

            chat.add_user_message(
                """
You are an image safety classifier.

Task:
Determine if the image contains explicit nudity, sexual activity, or other NSFW (Not Safe For Work) content.
Return only a single JSON boolean field called `nsfw`:
- true → if the image is NSFW or sexually inappropriate
- false → if the image is clean and safe for all audiences
""",
                images=[image_handle],
            )

            print(f"  💭 Evaluating image safety...")
            prediction = model.respond(chat, response_format=NSFWCheck)

            if prediction.parsed["nsfw"]:
                print(f"  🚫 NSFW content detected")
                print(f"  🗑️ Removing file...")
                os.remove(image_path)
                print(f"❌ [{idx}/{total_images}] Removed: {image_path.name}\n")
                removed_count += 1
            else:
                print(f"✅ [{idx}/{total_images}] Safe: {image_path.name}\n")
                safe_count += 1

        except Exception as e:
            print(f"⚠️ [{idx}/{total_images}] Error processing {image_path.name}: {e}\n")
            error_count += 1

    print(f"📊 Summary:")
    print(f"  ✅ Safe images: {safe_count}")
    print(f"  🚫 Removed NSFW images: {removed_count}")
    print(f"  ⚠️ Errors: {error_count}")
    print(f"🎉 All done!")


if __name__ == "__main__":
    main()
