import os
import shutil
import sys

def copy_directory(source_dir, target_dir):
    """
    Copies the contents of the source directory to the target directory recursively.

    Args:
    source_dir (str): The path to the source directory.
    target_dir (str): The path to the target directory.
    """
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    total_files = sum([len(files) for _, _, files in os.walk(source_dir)])
    copied_files = 0
    skipped_files = 0

    for root, dirs, files in os.walk(source_dir):
        for dir_ in dirs:
            source_path = os.path.join(root, dir_)
            target_path = os.path.join(target_dir, os.path.relpath(source_path, source_dir))

            print(f"Dir: {target_path}")

            if not os.path.exists(target_path):
                os.makedirs(target_path)

        for file_ in files:
            source_path = os.path.join(root, file_)
            target_path = os.path.join(target_dir, os.path.relpath(source_path, source_dir))
            if not os.path.exists(target_path):
                shutil.copy2(source_path, target_path)
                copied_files += 1
                print(f"Copied {copied_files}/{total_files} files...", end='\r')
            else:
                skipped_files +=1
                print(f"Skipped {skipped_files}/{total_files} files...", end='\r')

    print(f"\nCopying completed. {copied_files} files copied.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python copy_directory.py <source_directory> <target_directory>")
        sys.exit(1)
    
    source_directory = sys.argv[1]
    target_directory = sys.argv[2]
    
    copy_directory(source_directory, target_directory)