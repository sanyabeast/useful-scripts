# Usage: python script.py folder_path new_format [--recursive]

import os
from PIL import Image

def convert_images(folder_path, new_format, recursive=False):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith('.webp'):
                file_path = os.path.join(root, file_name)
                with Image.open(file_path) as img:
                    file_root, file_ext = os.path.splitext(file_name)
                    new_file_path = os.path.join(root, f'{file_root}.{new_format}')
                    img.save(new_file_path)

                os.remove(file_path)
        if not recursive:
            break

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python script.py folder_path new_format [--recursive]')
        sys.exit(1)
    
    folder_path = sys.argv[1]
    new_format = sys.argv[2]
    recursive = '--recursive' in sys.argv

    if new_format not in ('jpg', 'png'):
        print('Invalid format specified. Please choose either "jpg" or "png".')
        sys.exit(1)
    
    convert_images(folder_path, new_format, recursive)