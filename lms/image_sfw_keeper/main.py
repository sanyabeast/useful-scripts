#!/usr/bin/env python3
"""
Usage:
    python remove_nsfw_images.py --folder "H:/Pictures" --model "gemma-3-4b-it"

This script recursively scans all images in a folder and removes those flagged by an LLM as NSFW.
"""

import argparse
from pathlib import Path
import lmstudio as lms
from pydantic import BaseModel
import mimetypes
import os


class NSFWCheck(BaseModel):
    nsfw: bool


def is_image_file(file_path):
    mime, _ = mimetypes.guess_type(file_path)
    return mime is not None and mime.startswith("image")


def main():
    parser = argparse.ArgumentParser(description="Remove NSFW images in a folder using LLM detection.")
    parser.add_argument("--folder", required=True, help="Path to the folder containing images")
    parser.add_argument("--model", required=True, help="Model name to use for NSFW detection")

    args = parser.parse_args()
    folder = Path(args.folder)

    if not folder.exists() or not folder.is_dir():
        print("❌ Error: Provided folder does not exist or is not a directory.")
        return

    model = lms.llm(args.model)
    print(f"📂 Scanning folder: {folder.resolve()}")

    image_files = [f for f in folder.rglob("*") if f.is_file() and is_image_file(f)]
    total_images = len(image_files)

    if not image_files:
        print("⚠️ No image files found.")
        return

    print(f"🖼️ Found {total_images} image(s). Starting NSFW check...\n")

    for idx, image_path in enumerate(image_files, start=1):
        try:
            print(f"🔍 [{idx}/{total_images}] Checking: {image_path}")

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
                images=[image_handle]
            )

            prediction = model.respond(chat, response_format=NSFWCheck)

            if prediction.parsed["nsfw"]:
                print(f"🚫 NSFW detected. Deleting: {image_path}")
                os.remove(image_path)
            else:
                print(f"✅ Safe: {image_path.name}")

        except Exception as e:
            print(f"❌ Error checking {image_path.name}: {e}")

    print("\n🎉 NSFW image filtering complete.")


if __name__ == "__main__":
    main()
