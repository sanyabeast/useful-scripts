import os
import sys

def crop_filename(name, max_len):
    name_only, ext = os.path.splitext(name)
    cropped_name = name_only[:max_len]
    return cropped_name + ext

def crop_filenames_in_folder(folder_path, max_len=16):
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found - {folder_path}")
        return

    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)
        if os.path.isfile(old_path):
            new_name = crop_filename(filename, max_len)
            new_path = os.path.join(folder_path, new_name)
            if old_path != new_path:
                print(f"Renaming: {filename} -> {new_name}")
                os.rename(old_path, new_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crop_filenames.py <folder_path> [max_length]")
    else:
        folder = sys.argv[1]
        max_length = int(sys.argv[2]) if len(sys.argv) >= 3 else 16
        crop_filenames_in_folder(folder, max_length)