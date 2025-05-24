#!/usr/bin/env python3
"""
Usage:
    python main.py --input-folder "path/to/images" --output-folder "path/to/output" --model "gemma-3-4b-it-qat"
        [--start-index 1] [--padding 4] [--recursive] [--prefix "text"] [--prompt "context"] [--resolution "512 768 1024"]

This script processes a folder of images to create a dataset by:
1. Renaming images to sequential numbers (0001.jpg, 0002.jpg, etc.)
2. Converting PNG images to JPEG format
3. Creating a text file for each image with an AI-generated description

Options:
    --input-folder: Path to the folder containing source images
    --output-folder: Path where renamed images and description files will be saved
    --model: LMS model name to use for generating image descriptions
    --start-index: Starting index for numbering (default: 1)
    --padding: Number of digits to use in the filename (default: 4)
    --recursive: Include images in subfolders of the input folder
    --prefix: Text to add at the beginning of each description
    --prompt: Additional context to guide the LLM (e.g., "images in John Blueberry art style")
    --resolution: Space-separated list of height resolutions (default: "512 768 1024")
"""

import argparse
from pathlib import Path
import shutil
import sys
import signal
import mimetypes
from PIL import Image
import lmstudio as lms
from pydantic import BaseModel


class ImageDescription(BaseModel):
    description: str


def is_image_file(file_path):
    """Check if a file is an image based on its MIME type."""
    mime, _ = mimetypes.guess_type(file_path)
    return mime is not None and mime.startswith("image")


def convert_to_jpg(image_path, output_path, height=None):
    """Convert any image format to JPEG and save to the output path with optional resizing."""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB mode if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                img = background
            else:
                img = img.convert('RGB')
                
            # Resize if height is specified
            if height:
                # Calculate new width to maintain aspect ratio
                aspect_ratio = img.width / img.height
                new_width = int(height * aspect_ratio)
                img = img.resize((new_width, height), Image.LANCZOS)
                
            img.save(output_path, 'JPEG', quality=95)
        return True
    except Exception as e:
        print(f"❌ Error converting image {image_path}: {e}")
        return False


def generate_image_description(image_path, model, prompt_context=None):
    """Generate a description for the image using the LMS model."""
    try:
        image_handle = lms.prepare_image(str(image_path))
        chat = lms.Chat()
        
        prompt = f"""
        You are a professional dataset assistant helping create clean image-caption pairs for a visual training model (LoRA).

        Context: {prompt_context or "None"}

        🎯 Task:
        - Describe what is clearly shown in this image.
        - Focus on visual content only: objects, subjects, setting, style, mood, color palette, camera angle, and texture.
        - Keep it visually descriptive and factual.
        - Avoid artistic interpretation, metaphor, storytelling, or imaginative additions.
        - Be concise but complete — use 3 to 4 grounded, informative sentences.

        ❌ Avoid:
        - Subjective impressions or emotions (e.g., "beautiful", "mysterious")
        - Hypotheticals or symbolic language (e.g., "as if", "represents", "feels like")
        - Stating what is *not* in the image
        - Prefixes like "This image shows..." or commentary

        ✅ Format your output as **valid JSON** with this structure only:

        ```json
        {{
        "description": "your detailed description here"
        }}
        """
        
        # Add context to the prompt if provided
        if prompt_context:
            prompt = f"Context: {prompt_context}\n\n{prompt}"
        
        chat.add_user_message(prompt, images=[image_handle])
        response = model.respond(chat, response_format=ImageDescription)
        
        # Extract the description from the parsed response
        if hasattr(response, 'parsed') and 'description' in response.parsed:
            return response.parsed['description'].strip()
        else:
            # Fallback to handle different response formats
            if hasattr(response, 'text'):
                return response.text.strip()
            elif hasattr(response, 'content'):
                return response.content.strip()
            elif hasattr(response, 'message'):
                return response.message.strip()
            else:
                # If we can't find a standard attribute, convert the whole response to string
                return str(response).strip()
    except Exception as e:
        print(f"❌ Error generating description for {image_path}: {e}")
        return "No description available due to an error in processing."


def signal_handler(sig, frame):
    print("\n\n⚠️ Ctrl+C detected. Exiting gracefully...")
    print("👋 Goodbye!")
    sys.exit(0)


def main():
    # Set up signal handler for graceful exit on Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(description="Create an image dataset with sequential numbering and descriptions.")
    parser.add_argument("-i", "--input-folder", required=True, help="Path to the folder containing images")
    parser.add_argument("-o", "--output-folder", required=True, help="Path where renamed images and descriptions will be saved")
    parser.add_argument("-m", "--model", required=True, help="Model name to use for image description generation")
    parser.add_argument("--start-index", type=int, default=1, help="Starting index for numbering (default: 1)")
    parser.add_argument("--padding", type=int, default=4, help="Number of digits to use in the filename (default: 4)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Include images in subfolders")
    parser.add_argument("--prefix", help="Text to add at the beginning of each description")
    parser.add_argument("--prompt", help="Additional context to guide the LLM (e.g., \"images in John Blueberry art style\")")
    parser.add_argument("--resolution", default="512 768 1024", help="Space-separated list of height resolutions (default: \"512 768 1024\")")
    args = parser.parse_args()
    
    input_folder = Path(args.input_folder)
    output_folder = Path(args.output_folder)
    
    # Validate input folder
    if not input_folder.exists() or not input_folder.is_dir():
        print(f"❌ Error: Input folder '{input_folder}' does not exist or is not a directory.")
        return
    
    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Load the LMS model
    print(f"🤖 Loading model: {args.model}...")
    try:
        model = lms.llm(args.model)
        print(f"✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Collect image files
    print(f"📂 Scanning folder: {input_folder.resolve()}")
    image_files = []
    
    if args.recursive:
        print(f"🔍 Searching recursively through all nested folders")
        image_files = [f for f in input_folder.rglob("*") if f.is_file() and is_image_file(f)]
    else:
        print(f"🔍 Searching only in the top-level folder")
        image_files = [f for f in input_folder.glob("*") if f.is_file() and is_image_file(f)]
    
    total_images = len(image_files)
    
    if not image_files:
        print("⚠️ No image files found.")
        return
    
    print(f"🖼️ Found {total_images} image(s). Starting processing...\n")
    
    # Parse resolutions
    resolutions = [int(res.strip()) for res in args.resolution.split()]
    print(f"📷 Using resolutions: {resolutions}")
    
    # Create subdirectories for each resolution
    resolution_dirs = {}
    for res in resolutions:
        res_dir = output_folder / str(res)
        res_dir.mkdir(parents=True, exist_ok=True)
        resolution_dirs[res] = res_dir
        print(f"  📂 Created directory for resolution {res}: {res_dir}")
    
    # Process each image
    success_count = 0
    error_count = 0
    
    for idx, image_path in enumerate(image_files, start=args.start_index):
        try:
            # Create the new filename with padding
            new_filename = str(idx).zfill(args.padding)
            
            print(f"🔄 [{idx-args.start_index+1}/{total_images}] Processing: {image_path.name}")
            
            # Generate description first (do this only once per image)
            print(f"  📝 Generating description...")
            description = generate_image_description(image_path, model, args.prompt)
            
            # Add prefix if provided
            if args.prefix:
                description = f"{args.prefix} {description}"
            
            # Process for each resolution
            for res in resolutions:
                res_dir = resolution_dirs[res]
                new_image_path = res_dir / f"{new_filename}.jpg"
                new_text_path = res_dir / f"{new_filename}.txt"
                
                # Convert/resize the image to the output folder
                print(f"  📷 Converting to {res}px height: {new_image_path.name}")
                if not convert_to_jpg(image_path, new_image_path, height=res):
                    print(f"  ⚠️ Failed to convert {image_path.name} to {res}px, skipping")
                    continue
                
                # Save the description to a text file
                with open(new_text_path, "w", encoding="utf-8") as f:
                    f.write(description)
            
            print(f"  ✅ Successfully processed {image_path.name} to all resolutions")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {image_path}: {e}")
            error_count += 1
    
    print(f"\n📊 Processing complete!")
    print(f"✅ Successfully processed: {success_count} images")
    if error_count > 0:
        print(f"❌ Errors encountered: {error_count} images")
    print(f"📁 Output saved to: {output_folder.resolve()}")


if __name__ == "__main__":
    main()
