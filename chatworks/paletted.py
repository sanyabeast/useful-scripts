import sys
from PIL import Image

# Get the input image filename and desired number of colors from the command line arguments
if len(sys.argv) < 2:
    print("Usage: python palette.py <input_image> [<num_colors>]")
    sys.exit(1)
input_filename = sys.argv[1]
num_colors = int(sys.argv[2]) if len(sys.argv) > 2 else 8
pixelation_level = int(sys.argv[3]) if len(sys.argv) > 3 else 4

# Load the input image
input_image = Image.open(input_filename)

# Pixelate the image
pixelated_image = input_image.resize((input_image.width // pixelation_level, input_image.height // pixelation_level), resample=Image.BOX)
pixelated_image = pixelated_image.resize(input_image.size, resample=Image.NEAREST)

# Convert the image to a palette using Floyd-Steinberg dithering
output_image = pixelated_image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)

# Save the output image with a modified filename
output_filename = f"{input_filename.rsplit('.', 1)[0]}_{num_colors}colors.png"
output_image.save(output_filename)

print(f"Saved output image to {output_filename}")