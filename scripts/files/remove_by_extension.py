# This script should be used in the following way from the command line:

# python remove_by_extension.py --dir "/path/to/directory" --ext "txt" --recursive
# Replace remove_by_extension.py with the name of your script, "/path/to/directory" with the path of your directory, "txt" with your file extension. Use --recursive flag if you want to delete files recursively.

# Caution: As before, please be careful as this script deletes files permanently. Always ensure that you have a backup of your files before running this script.


import os
import glob
import argparse


def delete_files(folder_path, extension, recursive):
    if recursive:
        files = glob.glob(f"{folder_path}/**/*.{extension}", recursive=True)
    else:
        files = glob.glob(f"{folder_path}/*.{extension}")

    for file in files:
        try:
            os.remove(file)
            print(f"File {file} has been deleted")
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")


def main():
    parser = argparse.ArgumentParser(
        description='Delete files with a specific extension in a directory.')
    parser.add_argument('-d', '--dir', required=True,
                        help='Directory to delete files from')
    parser.add_argument('-e', '--ext', required=True,
                        help='File extension to delete')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Recursively delete files in subdirectories')

    args = parser.parse_args()

    delete_files(args.dir, args.ext, args.recursive)


if __name__ == "__main__":
    main()
