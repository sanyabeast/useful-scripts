#!/usr/bin/env python3
"""
Usage:
    python rename_images_with_llm.py --folder "H:/Pictures" --model "gemma-3-4b-it"
        [--min-length 32] [--max-length 128]

This script walks through the given folder (recursively), and renames each image file
based on a filename suggested by an LLM. It skips files if the new name already exists,
preserves the original file extension, and logs progress to the console.
"""

import argparse
from pathlib import Path
import lmstudio as lms
from pydantic import BaseModel
import mimetypes


class ImageDescription(BaseModel):
    suggested_filename: str


def is_image_file(file_path):
    mime, _ = mimetypes.guess_type(file_path)
    return mime is not None and mime.startswith("image")


def main():
    parser = argparse.ArgumentParser(description="Rename images in a folder using LLM-generated filenames.")
    parser.add_argument("--folder", required=True, help="Path to the folder containing images")
    parser.add_argument("--model", required=True, help="Model name to use for filename generation")
    parser.add_argument("--min-length", type=int, default=32, help="Minimum filename length (default: 32)")
    parser.add_argument("--max-length", type=int, default=128, help="Maximum filename length (default: 64)")
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

    print(f"🖼️ Found {total_images} image(s). Starting renaming process...\n")

    for idx, image_path in enumerate(image_files, start=1):
        try:
            print(f"🔄 [{idx}/{total_images}] Processing: {image_path}")

            image_handle = lms.prepare_image(str(image_path))
            chat = lms.Chat()

            prompt = f"""
Describe this image and suggest a filename for it.
Generate a filename using lowercase snake_case format, with a minimum length of {args.min_length} characters and a maximum of {args.max_length} characters.
Do not include the file extension in the filename.
Do not use personal names.
"""

            chat.add_user_message(prompt, images=[image_handle])
            prediction = model.respond(chat, response_format=ImageDescription)

            # Trim result to max length and clean formatting
            new_filename_base = prediction.parsed["suggested_filename"].strip()[:args.max_length]
            new_filename = new_filename_base + image_path.suffix.lower()
            new_filepath = image_path.with_name(new_filename)

            if new_filepath.exists():
                print(f"⏭️ [{idx}/{total_images}] Skipped: {new_filename} already exists.\n")
                continue

            image_path.rename(new_filepath)
            print(f"✅ [{idx}/{total_images}] Renamed to: {new_filename}\n")

        except Exception as e:
            print(f"❌ [{idx}/{total_images}] Error processing {image_path.name}: {e}\n")

    print("🎉 All done!")


if __name__ == "__main__":
    main()
