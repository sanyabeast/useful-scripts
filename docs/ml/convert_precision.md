# convert_precision.py

Convert Safetensors model precision (fp16, fp32, or fp8). This script leverages the `safetensors` library for efficient loading and saving of tensor data. It's designed to reduce memory footprint and potentially improve inference speed by converting models to lower precision formats like FP16 or FP8.  FP8 support requires PyTorch 2.1 or higher and compatible hardware (e.g., NVIDIA Ampere architecture or later).  The script preserves metadata during the conversion process, ensuring compatibility with downstream tools and workflows.
