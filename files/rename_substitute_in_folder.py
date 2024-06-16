# useage: rename_substitute_in_folder.py "path/to/folder" "old_string" "new_string"
# example: rename_substitute_in_folder.py "c:/my/lovely/dir" "lol" "kek"
# example: rename_substitute_in_folder.py "c:/my/lovely/dir" "(Copy)" ""


import os
import sys

def rename_files_in_folder(folder_path, to_replace, replacement=""):
    try:
        for filename in os.listdir(folder_path):
            new_filename = filename.replace(to_replace, replacement)
            if new_filename != filename:
                os.rename(
                    os.path.join(folder_path, filename),
                    os.path.join(folder_path, new_filename)
                )
                print(f'Renamed: {filename} -> {new_filename}')
            else:
                print(f'No change: {filename}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py path/to/folder what_to_replace [replacement]")
        print(f"Arguments received: {sys.argv}")
        sys.exit(1)

    folder_path = sys.argv[1]
    to_replace = sys.argv[2]
    replacement = sys.argv[3] if len(sys.argv) > 3 else ""

    print(f"Folder path: {folder_path}")
    print(f"String to replace: '{to_replace}'")
    print(f"Replacement string: '{replacement}'")

    rename_files_in_folder(folder_path, to_replace, replacement)