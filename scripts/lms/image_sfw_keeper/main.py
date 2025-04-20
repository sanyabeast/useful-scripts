#!/usr/bin/env python3
"""
Usage:
    python remove_nsfw_images.py --folder "H:/Pictures" --model "gemma-3-4b-it" [--recursive] [--threshold 0.7]

This script scans images in a folder and removes those flagged by an LLM as NSFW.
When --recursive is specified, it will include nested folders in the search.
The threshold parameter (0-1) controls the NSFW filtering sensitivity:
    0 - Remove everything that is barely NSFW
    1 - Remove nothing
Default is 0.7 (moderate filtering)
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
    nsfw_score: float


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
    parser.add_argument("--threshold", type=float, default=0.7, help="NSFW score threshold (0-1). Lower values remove more images (0=strict, 1=permissive)")

    args = parser.parse_args()
    folder = Path(args.folder)

    # Validate threshold
    if args.threshold < 0 or args.threshold > 1:
        print("❌ Error: Threshold must be between 0 and 1.")
        return

    if not folder.exists() or not folder.is_dir():
        print("❌ Error: Provided folder does not exist or is not a directory.")
        return

    print(f"🤖 Loading model: {args.model}...")
    model = lms.llm(args.model)
    print(f"✅ Model loaded successfully!")
    
    print(f"📂 Scanning folder: {folder.resolve()}")
    print(f"🎚️ NSFW threshold set to: {args.threshold} ({get_threshold_description(args.threshold)})")

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

            chat.add_user_message(f"""
                You are a strict visual safety auditor trained to detect NSFW (Not Safe For Work) content.

                Analyze the image for the presence of any of the following:
                - nudity (partial or full)
                - sexual activity
                - explicit or fetish content
                - suggestive posing
                - visual emphasis on genitalia or sexual body parts
                - erotic context (even without nudity)

                Return a JSON response with this format:
                {{
                "nsfw_score": float
                }}

                Scoring scale:
                - 0.0 = Safe for all audiences, nothing inappropriate
                - 0.1–0.3 = Slightly suggestive (e.g., swimwear, mildly sensual posing)
                - 0.4–0.6 = Revealing or suggestive content with adult context
                - 0.7–0.9 = Highly suggestive or borderline explicit content
                - 1.0 = Explicit adult content (e.g., pornographic, graphic sex acts)

                Additional rules:
                - Avoid false positives for anatomy in medical or artistic context unless overtly eroticized
                - Prioritize visual cues over artistic ambiguity
                - If in doubt, err on the side of stricter classification

                Return only the `nsfw_score`, and nothing else.
            """,
                images=[image_handle],
            )

            print(f"  💭 Evaluating image safety...")
            prediction = model.respond(chat, response_format=NSFWCheck)
            nsfw_score = prediction.parsed["nsfw_score"]
            
            # Determine if the image should be removed based on threshold
            should_remove = nsfw_score > args.threshold
            
            # Display score with emoji indicator
            score_emoji = get_score_emoji(nsfw_score)
            print(f"  {score_emoji} NSFW Score: {nsfw_score:.2f}")

            if should_remove:
                print(f"  🚫 NSFW content detected (above threshold)")
                print(f"  🗑️ Removing file...")
                os.remove(image_path)
                print(f"❌ [{idx}/{total_images}] Removed: {image_path.name}\n")
                removed_count += 1
            else:
                if nsfw_score > 0:
                    print(f"  ⚠️ Some NSFW content detected (below threshold)")
                else:
                    print(f"  ✅ No NSFW content detected")
                print(f"✅ [{idx}/{total_images}] Kept: {image_path.name}\n")
                safe_count += 1

        except Exception as e:
            print(f"⚠️ [{idx}/{total_images}] Error processing {image_path.name}: {e}\n")
            error_count += 1

    print(f"📊 Summary:")
    print(f"  ✅ Safe/kept images: {safe_count}")
    print(f"  🚫 Removed NSFW images: {removed_count}")
    print(f"  ⚠️ Errors: {error_count}")
    print(f"  🎚️ Threshold used: {args.threshold} ({get_threshold_description(args.threshold)})")
    print(f"🎉 All done!")


def get_score_emoji(score):
    """Return an appropriate emoji based on the NSFW score."""
    if score < 0.1:
        return "🟢"  # Very safe
    elif score < 0.3:
        return "🟡"  # Mostly safe
    elif score < 0.6:
        return "🟠"  # Borderline
    elif score < 0.9:
        return "🔴"  # Highly suggestive
    else:
        return "⛔"  # Explicit


def get_threshold_description(threshold):
    """Return a description of what the threshold means."""
    if threshold < 0.2:
        return "very strict filtering"
    elif threshold < 0.4:
        return "strict filtering"
    elif threshold < 0.6:
        return "moderate filtering"
    elif threshold < 0.8:
        return "lenient filtering"
    else:
        return "very lenient filtering"


if __name__ == "__main__":
    main()
