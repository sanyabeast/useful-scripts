# Usage: 
# python hashnamer.py <directory_path> [delete_dupes] [extensions] [method] [global_dupes] [trim_name]
# 
# Arguments:
# <directory_path>    : Path to the directory to process.
# [delete_dupes]      : Optional. Set to 'true' to remove duplicate files (default: false).
# [extensions]        : Optional. Comma-separated list of file extensions to process (e.g., 'jpg,png,gif'). Processes all files if omitted.
# [method]            : Optional. Hash method to use: 'md5', 'sha256', or 'sha512' (default: 'md5').
# [global_dupes]      : Optional. Set to 'true' to track duplicates globally across all subdirectories (default: false).
# [trim_name]         : Optional. Length to trim the hash for the new file name (default: 64).
#
# Example:
# python hashnamer.py /path/to/directory true jpg,png,gif md5 false 64

import os
import sys
import hashlib
import random
import string


def generate_random_string(length):
    """Generate a random alphanumeric string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_file_hash_md5(file_path):
    """Generate MD5 hash from file content."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def generate_file_hash_sha256(file_path):
    """Generate SHA-256 hash from file content."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def generate_file_hash_sha512(file_path):
    """Generate SHA-512 hash from file content."""
    hasher = hashlib.sha512()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def rename_files(directory, delete_dupes=False, extensions=None, method="md5", global_dupes=False, trim_name=64):
    """Recursively rename files in a directory using hash-based names."""
    if extensions is None:
        extensions = []

    renamed_count = 0
    dupe_count = 0
    removed_dupes = 0
    skipped_dupes = 0
    skipped_files = 0
    hash_to_file = {}

    for root, _, files in os.walk(directory):
        if not global_dupes:
            hash_to_file = {}  # Reset hash tracking for each directory

        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_ext = os.path.splitext(file_name)[1].lower().lstrip('.')  # Remove leading dot
            if file_ext not in extensions:
                print(f"Skipping file with unsupported extension: '{file_path}'")
                skipped_files += 1
                continue

            # Generate the hash for the file content
            if method == "md5":
                file_hash = generate_file_hash_md5(file_path)
            elif method == "sha256":
                file_hash = generate_file_hash_sha256(file_path)
            elif method == "sha512":
                file_hash = generate_file_hash_sha512(file_path)
            else:
                print(f"Unknown method '{method}'")
                return

            if file_hash in hash_to_file:
                if delete_dupes:
                    os.remove(file_path)
                    removed_dupes += 1
                    dupe_count += 1
                    print(f"Deleted duplicate file: '{file_path}'")
                else:
                    dupe_count += 1
                    skipped_dupes += 1
                    print(f"Skipping duplicate file: '{file_path}'")
            else:
                hash_to_file[file_hash] = file_path
                new_file_name = file_hash[:trim_name]  # Trim hash for file name
                new_file_name_with_ext = new_file_name + os.path.splitext(file_name)[1]  # Keep original extension
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
        print("Usage: python hashnamer.py <directory_path> [delete_dupes] [extensions] [method] [global_dupes] [trim_name]")
        sys.exit(1)

    directory = sys.argv[1]
    delete_dupes = sys.argv[2].lower() == 'true' if len(sys.argv) >= 3 else False
    extensions = sys.argv[3].lower().split(',') if len(sys.argv) >= 4 else []
    method = sys.argv[4].lower() if len(sys.argv) >= 5 else "md5"
    global_dupes = sys.argv[5].lower() == 'true' if len(sys.argv) >= 6 else False
    trim_name = int(sys.argv[6]) if len(sys.argv) >= 7 else 64

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    print(f"""Preparing to rename files:
Directory: {directory}
Delete duplicates: {delete_dupes}
Global duplicates: {global_dupes}
Extensions: {extensions}
Hash method: {method}
Trim name length: {trim_name}
""")

    rename_files(directory, delete_dupes, extensions, method, global_dupes, trim_name)


if __name__ == "__main__":
    main()