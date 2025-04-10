import os
import sys
import random
import string


def generate_random_string(length):
    """Generate a random alphanumeric string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def rename_files(directory, length):
    """Recursively rename all files in a directory to random alphanumeric strings while preserving extensions."""
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_base, file_ext = os.path.splitext(file_name)
            new_file_name = generate_random_string(length)
            new_file_name_with_ext = new_file_name + file_ext
            new_file_path = os.path.join(root, new_file_name_with_ext)
            os.rename(file_path, new_file_path)
            print(f"Renamed '{file_path}' to '{new_file_path}'")


def main():
    if len(sys.argv) != 3:
        print("Usage: python hashnamer.py <directory_path> <length>")
        sys.exit(1)

    directory = sys.argv[1]
    length = int(sys.argv[2])

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    rename_files(directory, length)


if __name__ == "__main__":
    main()