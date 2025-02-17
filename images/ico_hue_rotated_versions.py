import sys
import os
from PIL import Image
import numpy as np

def apply_hue_rotation(image, angle):
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    # Separate alpha channel
    r, g, b, a = image.split()
    img_hsv = Image.merge("RGB", (r, g, b)).convert("HSV")
    np_img = np.array(img_hsv)
    np_img[..., 0] = (np_img[..., 0].astype(int) + angle) % 256
    rotated_rgb = Image.fromarray(np_img, "HSV").convert("RGB")
    
    # Merge with original alpha channel
    return Image.merge("RGBA", (*rotated_rgb.split(), a))

def process_icon(image_path, step):
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        return
    
    file_dir, file_name = os.path.split(image_path)
    file_base, file_ext = os.path.splitext(file_name)
    
    if file_ext.lower() != '.ico':
        print("Error: Only ICO files are supported.")
        return
    
    try:
        with Image.open(image_path) as img:
            icon_frames = []
            try:
                while True:
                    icon_frames.append((img.size, img.copy()))
                    img.seek(img.tell() + 1)
            except EOFError:
                pass  # End of frames
            
            if not icon_frames:
                print("Error: No frames found in ICO file.")
                return
            
            largest_size, largest_image = max(icon_frames, key=lambda x: x[0][0] * x[0][1])
            
            for hue in range(step, 361, step):
                rotated_image = apply_hue_rotation(largest_image, hue)
                new_filename = f"{file_base}_hue{hue}{file_ext}"
                new_filepath = os.path.join(file_dir, new_filename)
                rotated_image.save(new_filepath, format="ICO", sizes=[largest_size])
                print(f"Saved: {new_filepath}")
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <ico_image_path> <step>")
    else:
        try:
            step = int(sys.argv[2])
            process_icon(sys.argv[1], step)
        except ValueError:
            print("Error: Step must be a numeric value.")