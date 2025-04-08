import os
import re
import sys

def to_snake_case(name):
    name_without_ext = os.path.splitext(name)[0]
    name_snake = re.sub(r'[\W_]+', ' ', name_without_ext)
    name_snake = re.sub(r'\s+', '_', name_snake).lower()
    return name_snake

def rename_files_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found - {folder_path}")
        return

    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)
        if os.path.isfile(old_path):
            name, ext = os.path.splitext(filename)
            new_name = to_snake_case(name) + ext.lower()
            new_path = os.path.join(folder_path, new_name)
            if old_path != new_path:
                print(f'Renaming: {filename} -> {new_name}')
                os.rename(old_path, new_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python snake_namer.py <folder_path>")
    else:
        folder = sys.argv[1]
        rename_files_in_folder(folder)