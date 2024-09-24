
# usage: 
# python hashnamer.py /path/to/directory remove_dupes extensions_to_process
# example:
# python hashnamer.py /path/to/directory true jpg,png,gif

import os
import sys
import hashlib
import random
import string


def generate_random_string(length):
    """Generate a random alphanumeric string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_file_hash(file_path):
    """Generate SHA-512 hash from file content."""
    hasher = hashlib.sha512()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def rename_files(directory, delete_dupes=False, extensions=None):
    """Recursively rename all files in a directory using a SHA-512 hash of file content."""
    if extensions is None:
        extensions = []

    renamed_count = 0
    dupe_count = 0
    removed_dupes = 0
    skipped_dupes = 0
    skipped_files = 0

    for root, _, files in os.walk(directory):
        hash_to_file = {}  # Track hashes per directory (per `root`)
        
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_ext = os.path.splitext(file_name)[1].lower().lstrip('.')  # Remove leading dot
            if file_ext not in extensions:
                print(f"Skipping file with unsupported extension: '{file_path}'")
                skipped_files += 1
                continue
            
            file_hash = generate_file_hash(file_path)
            if file_hash in hash_to_file:
                if delete_dupes:
                    os.remove(file_path)
                    removed_dupes += 1
                    dupe_count += 1
                    print(f"Deleted duplicate file in the same directory: '{file_path}'")
                else:
                    dupe_count += 1
                    skipped_dupes += 1
                    print(f"Skipping duplicate file in the same directory: '{file_path}'")
            else:
                hash_to_file[file_hash] = file_path
                file_base, file_ext = os.path.splitext(file_name)
                new_file_name = file_hash[:128]  # Use first 128 characters of hash as file name
                new_file_name_with_ext = new_file_name + file_ext  # Add extension
                new_file_path = os.path.join(root, new_file_name_with_ext)
                os.rename(file_path, new_file_path)
                renamed_count += 1
                print(f"Renamed '{file_path}' to '{new_file_path}'")

    print("\n--- Statistics ---")
    print(f"Total files renamed: {renamed_count}")
    print(f"Total files skipped: {skipped_files}")
    print(f"Total duplicate files removed: {removed_dupes}")
    print(f"Total duplicate files skipped: {skipped_dupes}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python hashnamer.py <directory_path> [delete_dupes] [extensions]")
        sys.exit(1)

    directory = sys.argv[1]
    delete_dupes = False
    extensions = []
    if len(sys.argv) >= 3:
        delete_dupes_str = sys.argv[2].lower()
        if delete_dupes_str == "true":
            delete_dupes = True
    if len(sys.argv) >= 4:
        extensions = [ext.lower() for ext in sys.argv[3].split(',')]  # Convert extensions to lowercase

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    rename_files(directory, delete_dupes, extensions)


if __name__ == "__main__":
    main()