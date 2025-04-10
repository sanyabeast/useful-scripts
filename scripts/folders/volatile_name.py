import os
import random
import sys


def rename_folder(dir_path, name_prefix):
    try:
        # List all folders in the directory
        folders = [f for f in os.listdir(
            dir_path) if os.path.isdir(os.path.join(dir_path, f))]

        # Filter out folders whose name starts with the specified prefix
        target_folders = [f for f in folders if f.startswith(name_prefix)]

        # If no such folder exists
        if not target_folders:
            print(f"No folder with prefix '{name_prefix}' found.")
            return

        # Rename each folder found with the specified prefix
        for folder in target_folders:
            new_name = folder  # Initialize new_name with the old name

            # Generate a new name that is different from the existing name and any other existing folder name
            while new_name == folder or new_name in folders:
                new_name = f"{name_prefix}{random.randint(1, 9999999)}"

            src = os.path.join(dir_path, folder)
            dst = os.path.join(dir_path, new_name)
            os.rename(src, dst)
            print(f"Renamed folder '{folder}' to '{new_name}'")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python volatile_dir_name.py <directory_path> <name_prefix>")
    else:
        dir_path = sys.argv[1]
        name_prefix = sys.argv[2]
        rename_folder(dir_path, name_prefix)
