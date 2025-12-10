#!/usr/bin/env python3
"""
Usage:
    python rename_images_with_llm.py --folder "H:/Pictures" --model "gemma-3-4b-it"
        [--min-length 32] [--max-length 128] [--recursive] [--force] [--threshold 0.4]
    
    # Or process a single file:
    python rename_images_with_llm.py --file "H:/Pictures/image.jpg" --model "gemma-3-4b-it"
        [--min-length 32] [--max-length 128] [--force] [--threshold 0.4]

This script renames image files based on filenames suggested by an LLM.
It can process either a single file (--file) or a folder of images (--folder).
When --recursive is specified with --folder, it will include nested folders.
The LLM rates the current filename's descriptiveness (0-1), and files with 
scores above the threshold (default: 0.4) keep their names.
Use --force to rename all files regardless of their current name quality.
If the new name already exists, a numeric postfix (e.g., _2, _3) is added.
"""

import argparse
from pathlib import Path
import lmstudio as lms
from pydantic import BaseModel
import mimetypes
from PIL import Image, PngImagePlugin, ImageSequence
import signal
import sys


class ImageDescription(BaseModel):
    suggested_filename: str
    current_name_descriptiveness: float
    suggested_name_descriptiveness: float


def is_image_file(file_path):
    mime, _ = mimetypes.guess_type(file_path)
    return mime is not None and mime.startswith("image")


def get_processed_name(image_path: Path):
    """Return stored filename from image metadata if present."""
    try:
        with Image.open(image_path) as img:
            fmt = img.format
            if fmt == 'JPEG':
                exif = img.getexif()
                # 270 = ImageDescription, 37510 = UserComment
                for tag in (270, 37510):
                    if tag in exif and exif[tag]:
                        return str(exif[tag]).strip()
            elif fmt == 'PNG':
                # Pillow stores textual chunks in img.info
                for key in ('Description', 'ImageDescription'):
                    if key in img.info and img.info[key]:
                        return str(img.info[key]).strip()
            elif fmt == 'GIF':
                if 'comment' in img.info and img.info['comment']:
                    comment = img.info['comment']
                    if isinstance(comment, bytes):
                        return comment.decode('utf-8', errors='ignore').strip()
                    return str(comment).strip()
    except Exception:
        # Ignore any failures reading metadata
        pass
    return None


def store_processed_name(image_path: Path, name: str):
    """Write the processed filename into image metadata so we can detect it later."""
    try:
        with Image.open(image_path) as img:
            fmt = img.format
            if fmt == 'JPEG':
                exif = img.getexif()
                exif[270] = name  # ImageDescription
                img.save(image_path, exif=exif)
            elif fmt == 'PNG':
                # Copy existing text attributes
                meta = PngImagePlugin.PngInfo()
                for k, v in img.info.items():
                    if isinstance(v, str):
                        meta.add_text(k, v)
                meta.add_text("Description", name)
                img.save(image_path, pnginfo=meta)
            elif fmt == 'GIF':
                # Handle animated GIFs by iterating through frames
                frames = []
                for frame in ImageSequence.Iterator(img):
                    frames.append(frame.copy())
                
                # The info dict from the first frame contains global properties
                info = frames[0].info.copy()
                info['comment'] = name.encode('utf-8')

                # Save the first frame, appending the rest
                frames[0].save(image_path, save_all=True, append_images=frames[1:], **info)
    except Exception as e:
        print(f"  ⚠️ Could not write metadata for {image_path.name}: {e}")


def to_snake_case(filename):
    """Convert a filename to snake_case format."""
    # Replace hyphens with underscores
    filename = filename.replace('-', '_')
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Replace multiple underscores with a single one
    while '__' in filename:
        filename = filename.replace('__', '_')
    return filename


def signal_handler(sig, frame):
    print("\n\n⚠️ Ctrl+C detected. Exiting gracefully...")
    print("👋 Goodbye!")
    sys.exit(0)


def main():
    # Set up signal handler for graceful exit on Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(description="Rename images using LLM-generated filenames.")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--folder", help="Path to the folder containing images")
    input_group.add_argument("--file", help="Path to a single image file to rename")
    parser.add_argument("--model", required=True, help="Model name to use for filename generation")
    parser.add_argument("--min-length", type=int, default=32, help="Minimum filename length (default: 32)")
    parser.add_argument("--max-length", type=int, default=128, help="Maximum filename length (default: 64)")
    parser.add_argument("--recursive", action="store_true", help="Include nested folders when using --folder")
    parser.add_argument("--force", action="store_true", help="Force renaming all files regardless of LLM's assessment")
    parser.add_argument("--threshold", type=float, default=0.4, help="Threshold for keeping original filename (0-1, default: 0.4)")
    parser.add_argument("--max-words", type=int, default=5, help="Maximum content words in filename, excluding prepositions/articles (default: 5)")
    args = parser.parse_args()

    print(f"🤖 Loading model: {args.model}...")
    model = lms.llm(args.model)
    print(f"✅ Model loaded successfully!")
    
    # Collect image files based on whether --folder or --file was specified
    image_files = []
    
    if args.folder:
        folder = Path(args.folder)
        if not folder.exists() or not folder.is_dir():
            print("❌ Error: Provided folder does not exist or is not a directory.")
            return
            
        print(f"📂 Scanning folder: {folder.resolve()}")
        
        # Use glob or rglob based on the recursive flag
        if args.recursive:
            print(f"🔍 Searching recursively through all nested folders")
            image_files = [f for f in folder.rglob("*") if f.is_file() and is_image_file(f)]
        else:
            print(f"🔍 Searching only in the top-level folder")
            image_files = [f for f in folder.glob("*") if f.is_file() and is_image_file(f)]
    else:  # args.file
        file_path = Path(args.file)
        if not file_path.exists() or not file_path.is_file():
            print("❌ Error: Provided file does not exist or is not a file.")
            return
            
        if not is_image_file(file_path):
            print("❌ Error: Provided file is not a recognized image format.")
            return
            
        print(f"🖼️ Processing single file: {file_path.resolve()}")
        image_files = [file_path]
    
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
    error_count = 0
    kept_count = 0

    base_folder = Path(args.folder) if args.folder else None
    
    for idx, image_path in enumerate(image_files, start=1):
        try:
            current_filename = image_path.stem
            print(f"🔄 [{idx}/{total_images}] Processing: {image_path}")

            # Skip if already processed and metadata matches current filename
            if not args.force:
                stored_name = get_processed_name(image_path)
                if stored_name and stored_name == current_filename:
                    print(f"⏭️ [{idx}/{total_images}] Already processed (metadata matches filename). Skipping.\n")
                    kept_count += 1
                    continue
            
            print(f"  📊 Analyzing image content...")
            image_handle = lms.prepare_image(str(image_path))
            chat = lms.Chat()

            relative_folder = ""
            if base_folder:
                try:
                    rel_path = image_path.parent.relative_to(base_folder)
                    if str(rel_path) != ".":
                        relative_folder = str(rel_path).replace("\\", "/")
                except ValueError:
                    pass
            
            folder_hint = f'\nFolder context: "{relative_folder}" (use as hint about category/theme)' if relative_folder else ""
            
            prompt = f"""You are a filename generator for images. Analyze the image and suggest a descriptive snake_case filename.

Current filename: "{current_filename}"{folder_hint}

Requirements:
- Describe what is visually shown (subject, setting, mood, colors)
- Use lowercase snake_case, no extension
- Maximum {args.max_words} content words (nouns, verbs, adjectives); prepositions/articles (on, in, the, a, of, with, at, to, for) don't count
- Length: {args.min_length}-{args.max_length} characters
- Avoid: generic words (image, photo, picture), personal names, timestamps, abstract poetry

Examples: foggy_forest_cabin (3 words), red_cat_sleeping_on_balcony (4 words: red, cat, sleeping, balcony)

Rate current filename descriptiveness (0.0-1.0) and provide your suggestion."""

            chat.add_user_message(prompt, images=[image_handle])
            print(f"  💭 Generating filename suggestion...")
            prediction = model.respond(chat, response_format=ImageDescription)

            # Trim result to max length and clean formatting
            new_filename_base = prediction.parsed["suggested_filename"].strip()[:args.max_length]
            # Convert to snake_case
            new_filename_base = to_snake_case(new_filename_base)
            new_filename = new_filename_base + image_path.suffix.lower()
            new_filepath = image_path.with_name(new_filename)
            
            # Get the descriptiveness score of the current filename
            descriptiveness = prediction.parsed["current_name_descriptiveness"]
            suggested_descriptiveness = prediction.parsed["suggested_name_descriptiveness"]
            
            # Decide whether to rename based on descriptiveness and force flag
            should_rename = args.force or descriptiveness < args.threshold
            
            if not should_rename:
                print(f"🔒 [{idx}/{total_images}] Kept original name: Score {descriptiveness:.2f} > threshold {args.threshold:.2f}\n")
                # Store metadata so we skip on future runs
                store_processed_name(image_path, current_filename)
                kept_count += 1
                continue

            # Handle case when the new filename already exists by adding a numeric postfix
            if new_filepath.exists():
                counter = 2
                while True:
                    postfix_filename = f"{new_filename_base}_{counter}{image_path.suffix.lower()}"
                    postfix_filepath = image_path.with_name(postfix_filename)
                    if not postfix_filepath.exists():
                        new_filename = postfix_filename
                        new_filepath = postfix_filepath
                        break
                    counter += 1
                print(f"  ⚠️ Original target filename already exists, using {new_filename} instead")

            print(f"  ✏️ Renaming file...")
            image_path.rename(new_filepath)
            # After renaming, store metadata so we can skip next time
            store_processed_name(new_filepath, new_filename_base)
            print(f"✨ [{idx}/{total_images}] Renamed to: {new_filename} (old: {descriptiveness:.2f} → new: {suggested_descriptiveness:.2f})\n")
            success_count += 1

        except Exception as e:
            print(f"❌ [{idx}/{total_images}] Error processing {image_path.name}: {e}\n")
            error_count += 1

    print(f"📊 Summary:")
    print(f"  ✨ Successfully renamed: {success_count}")
    print(f"  🔒 Kept original name: {kept_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"🎉 All done!")


if __name__ == "__main__":
    main()
