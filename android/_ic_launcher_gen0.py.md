**Image Resizer and Circular Image Generator**
=====================================================

This Python script generates different sized images from an input image and optionally creates circular versions of the resized images.

**Features**

* Resize images to various dimensions (LDPI, MDPI, HDPI, XHDPI, XXHDPi, XXXHDPI) for Android apps.
* Generate circular images from the resized images using OpenCV library.

**Usage**
--------

1. Run the script with Python: `python ic_launcher_gen0.py`
2. Provide the path of the input image as a command-line argument: `--image_path <path_to_image>`
3. Optionally, specify the '--rounded' flag to generate circular images: `--rounded`

Example:
```
$ python ic_launcher_gen0.py --image_path /path/to/input/image.png
```
or
```
$ python ic_launcher_gen0.py --image_path /path/to/input/image.png --rounded
```
**Dependencies**
--------------

* Python 3.x (tested with Python 3.9)
* PIL library for image processing
* OpenCV library for circular image generation

**Author**
--------

@sanyabeast, Kyiv, Ukraine - May 18th, 2023