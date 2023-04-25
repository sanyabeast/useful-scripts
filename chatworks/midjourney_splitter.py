import os
from PIL import Image

def split_images(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.jpg') or file_name.lower().endswith('.png'):
            file_path = os.path.join(folder_path, file_name)
            with Image.open(file_path) as img:
                width, height = img.size
                if width == height:  # check if the image is square
                    # calculate the size of each square
                    square_size = width // 2

                    # split the image into four square images
                    top_left = img.crop((0, 0, square_size, square_size))
                    top_right = img.crop((square_size, 0, width, square_size))
                    bottom_left = img.crop((0, square_size, square_size, height))
                    bottom_right = img.crop((square_size, square_size, width, height))

                    # save the four images with modified names
                    file_root, file_ext = os.path.splitext(file_name)
                    top_left.save(os.path.join(folder_path, f'{file_root}_top-left{file_ext}'))
                    top_right.save(os.path.join(folder_path, f'{file_root}_top-right{file_ext}'))
                    bottom_left.save(os.path.join(folder_path, f'{file_root}_bottom-left{file_ext}'))
                    bottom_right.save(os.path.join(folder_path, f'{file_root}_bottom-right{file_ext}'))

                    # remove the original file
                    os.remove(file_path)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python script.py folder_path')
        sys.exit(1)
    folder_path = sys.argv[1]
    split_images(folder_path)