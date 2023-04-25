import os
from PIL import Image

def convert_images(folder_path, new_format):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.webp'):
            file_path = os.path.join(folder_path, file_name)
            with Image.open(file_path) as img:
                file_root, file_ext = os.path.splitext(file_name)
                new_file_path = os.path.join(folder_path, f'{file_root}.{new_format}')
                img.save(new_file_path)

            os.remove(file_path)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python script.py folder_path new_format')
        sys.exit(1)
    folder_path = sys.argv[1]
    new_format = sys.argv[2]
    if new_format not in ('jpg', 'png'):
        print('Invalid format specified. Please choose either "jpg" or "png".')
        sys.exit(1)
    convert_images(folder_path, new_format)