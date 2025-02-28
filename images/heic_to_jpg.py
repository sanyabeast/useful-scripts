import os
import sys
from PIL import Image
import pillow_heif

def convert_heic_to_jpg(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: The specified path '{folder_path}' is not a valid directory.")
        return
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".heic") or filename.lower().endswith(".heif"):
            heic_path = os.path.join(folder_path, filename)
            jpg_path = os.path.splitext(heic_path)[0] + ".jpg"

            try:
                heif_image = pillow_heif.open_heif(heic_path)
                image = Image.frombytes(
                    heif_image.mode,
                    heif_image.size,
                    heif_image.data
                )
                image.save(jpg_path, "JPEG", quality=100)
                print(f"Converted: {filename} -> {os.path.basename(jpg_path)}")

            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_heic_to_jpg.py <folder_path>")
    else:
        convert_heic_to_jpg(sys.argv[1])
