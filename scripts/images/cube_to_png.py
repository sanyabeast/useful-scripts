"""
Converts .cube LUT files to PNG images for preview and compatibility.

.cube files are 3D color lookup tables used in video editing and color grading.
This script converts them to PNG format for easy preview or use in applications
that don't support .cube format natively.

Usage:
	python cube_to_png.py <folder>
	python cube_to_png.py <folder> -o <output_folder>
	python cube_to_png.py <folder> -l grid

Arguments:
	folder              Folder containing .cube files
	-o, --output        Output folder (default: same as input)
	-l, --layout        Layout: 'horizontal' (default) or 'grid'

The horizontal layout creates a wide strip image suitable for shader/texture use.
The grid layout creates a square grid for easier visual preview.
"""

import argparse
import os
import numpy as np
from PIL import Image
from pathlib import Path


def parse_cube_file(cube_path):
	with open(cube_path, 'r') as f:
		lines = f.readlines()
	
	size = None
	lut_data = []
	
	for line in lines:
		line = line.strip()
		
		if not line or line.startswith('#'):
			continue
		
		if line.startswith('TITLE'):
			continue
		
		if line.startswith('LUT_3D_SIZE'):
			size = int(line.split()[-1])
			continue
		
		if line.startswith('DOMAIN_MIN') or line.startswith('DOMAIN_MAX'):
			continue
		
		parts = line.split()
		if len(parts) == 3:
			try:
				r, g, b = map(float, parts)
				lut_data.append([r, g, b])
			except ValueError:
				continue
	
	if size is None:
		raise ValueError("LUT_3D_SIZE not found in .cube file")
	
	expected_entries = size ** 3
	if len(lut_data) != expected_entries:
		raise ValueError(f"Expected {expected_entries} entries, found {len(lut_data)}")
	
	lut_array = np.array(lut_data).reshape(size, size, size, 3)
	
	return lut_array


def lut_to_png(lut_array, output_path, layout='horizontal', bit_depth=8):
	size = lut_array.shape[0]
	
	if layout == 'horizontal':
		width = size * size
		height = size
		img_array = np.zeros((height, width, 3), dtype=np.float64)
		
		for b in range(size):
			for g in range(size):
				x_offset = b * size
				img_array[g, x_offset:x_offset + size] = lut_array[:, g, b]
	
	elif layout == 'grid':
		grid_size = int(np.ceil(np.sqrt(size)))
		width = size * grid_size
		height = size * grid_size
		img_array = np.zeros((height, width, 3), dtype=np.float64)
		
		for b in range(size):
			row = b // grid_size
			col = b % grid_size
			y_offset = row * size
			x_offset = col * size
			
			for g in range(size):
				img_array[y_offset + g, x_offset:x_offset + size] = lut_array[:, g, b]
	
	else:
		raise ValueError(f"Unknown layout: {layout}")
	
	if bit_depth == 16:
		img_array = np.clip(np.round(img_array * 65535.0), 0, 65535).astype(np.uint16)
		img = Image.fromarray(img_array, 'RGB')
		img.save(output_path, compress_level=0, optimize=False, bits=16)
	else:
		img_array = np.clip(np.round(img_array * 255.0), 0, 255).astype(np.uint8)
		img = Image.fromarray(img_array, 'RGB')
		img.save(output_path, compress_level=0, optimize=False)


def convert_folder(folder_path, layout='horizontal', output_folder=None, bit_depth=8):
	folder = Path(folder_path)
	
	if not folder.exists() or not folder.is_dir():
		print(f"Error: {folder_path} is not a valid directory")
		return
	
	if output_folder:
		out_dir = Path(output_folder)
		out_dir.mkdir(parents=True, exist_ok=True)
	else:
		out_dir = folder
	
	cube_files = list(folder.glob('*.cube'))
	
	if not cube_files:
		print(f"No .cube files found in {folder_path}")
		return
	
	print(f"Found {len(cube_files)} .cube file(s)")
	
	for cube_file in cube_files:
		try:
			lut_array = parse_cube_file(cube_file)
			size = lut_array.shape[0]
			slices = size
			
			print(f"Converting {cube_file.name} ({slices}x{slices}x{slices}, {slices} slices)...", end=' ')
			
			output_name = cube_file.stem + '.png'
			output_path = out_dir / output_name
			
			lut_to_png(lut_array, output_path, layout=layout, bit_depth=bit_depth)
			print(f"✓")
			
		except Exception as e:
			print(f"✗ Error: {e}")


def main():
	parser = argparse.ArgumentParser(description='Convert .cube LUT files to PNG images')
	parser.add_argument('folder', help='Folder containing .cube files')
	parser.add_argument('-o', '--output', help='Output folder (default: same as input)')
	parser.add_argument('-l', '--layout', choices=['horizontal', 'grid'], default='horizontal',
						help='PNG layout format (default: horizontal)')
	parser.add_argument('-b', '--bits', type=int, choices=[8, 16], default=8,
						help='Bit depth: 8 for compatibility, 16 for precision (default: 8)')
	
	args = parser.parse_args()
	
	convert_folder(args.folder, layout=args.layout, output_folder=args.output, bit_depth=args.bits)


if __name__ == '__main__':
	main()