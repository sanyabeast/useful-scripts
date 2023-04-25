import os
import sys
from PIL import Image

def convert_images(source_format, dest_format, folder_path):
    num_files = 0
    orig_size = 0
    new_size = 0

    for dirpath, _, filenames in os.walk(folder_path):
        for file_name in filenames:
            if file_name.lower().endswith(f'.{source_format}'):
                num_files += 1
                file_path = os.path.join(dirpath, file_name)
                with Image.open(file_path) as img:
                    file_root, _ = os.path.splitext(file_name)
                    new_file_path = os.path.join(dirpath, f'{file_root}.{dest_format}')
                    try:
                        img.save(new_file_path)
                        orig_size += os.path.getsize(file_path)
                        new_size += os.path.getsize(new_file_path)
                        os.remove(file_path)
                    except:
                        print(f"failed to save {new_file_path}")

    print(f"Converted {num_files} {source_format} files to {dest_format}.")
    print(f"Total size before conversion: {orig_size / 1024:.2f} KB")
    print(f"Total size after conversion: {new_size / 1024:.2f} KB")
    print(f"Total space saved: {(orig_size - new_size) / 1024:.2f} KB")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python script.py source_format dest_format folder_path')
        sys.exit(1)
    source_format = sys.argv[1].lower()
    dest_format = sys.argv[2].lower()
    folder_path = sys.argv[3]
    convert_images(source_format, dest_format, folder_path)