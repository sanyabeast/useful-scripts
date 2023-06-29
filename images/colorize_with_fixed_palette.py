from PIL import Image
import sys

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

if len(sys.argv) != 5:
    print("Usage: python3 fix_palette.py [image_path] [red] [green] [blue]")
    sys.exit(1)

image_path = sys.argv[1]
r, g, b = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])

try:
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size

    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            new_pixel = (clamp(pixel[0] + r, 0, 255),
                         clamp(pixel[1] + g, 0, 255),
                         clamp(pixel[2] + b, 0, 255))
            pixels[x, y] = new_pixel

    image.save("modified_" + image_path[:-4] + "_abracadabra.png", "PNG")
    print("Done")
except Exception as e:
    print("Error:", e)