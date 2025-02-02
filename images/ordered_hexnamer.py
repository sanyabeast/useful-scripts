import os
import sys
import random
import uuid

def rename_images_hex(folder_path, shuffle=False):
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return
    
    images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.png'))]
    
    if shuffle:
        random.shuffle(images)
    else:
        images.sort()  # Sort to maintain order before renaming
    
    temp_names = {}
    for filename in images:
        temp_name = str(uuid.uuid4()) + os.path.splitext(filename)[1].lower()
        temp_path = os.path.join(folder_path, temp_name)
        old_path = os.path.join(folder_path, filename)
        
        try:
            os.rename(old_path, temp_path)
            temp_names[temp_name] = filename
        except Exception as e:
            print(f"Failed to temporarily rename {filename}: {e}")
    
    images = list(temp_names.keys())  # Get the new temporary names
    
    for i, temp_name in enumerate(images):
        hex_name = format(i + 1, 'x')  # Convert index to hex (starting from 1)
        ext = os.path.splitext(temp_name)[1].lower()
        new_filename = f"{hex_name}{ext}"
        
        temp_path = os.path.join(folder_path, temp_name)
        new_path = os.path.join(folder_path, new_filename)
        
        try:
            os.rename(temp_path, new_path)
            print(f"Renamed: {temp_names[temp_name]} -> {new_filename}")
        except Exception as e:
            print(f"Failed to rename {temp_names[temp_name]}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python rename_images_hex.py <folder_path> [shuffle]")
    else:
        folder = sys.argv[1]
        shuffle = sys.argv[2].lower() == 'shuffle' if len(sys.argv) == 3 else False
        rename_images_hex(folder, shuffle)
