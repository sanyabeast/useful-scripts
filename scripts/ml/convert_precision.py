import sys
import torch
from safetensors.torch import load_file, save_file

def convert_precision(input_path, output_path, precision="fp16"):
    # Map the precision argument to PyTorch dtype
    precision_map = {
        "fp16": torch.float16,
        "fp32": torch.float32,
        "fp8": torch.float8_e4m3fn  # Requires PyTorch 2.1+ and compatible hardware
    }

    if precision not in precision_map:
        raise ValueError(f"Unsupported precision: {precision}. Supported: {list(precision_map.keys())}")

    target_dtype = precision_map[precision]

    try:
        # Load tensors from the safetensors file
        tensors = load_file(input_path)
        metadata = tensors.metadata() if hasattr(tensors, "metadata") else {}

        print(f"Loaded {len(tensors)} tensors from '{input_path}'. Converting to {precision}...")

        # Convert tensors to the target precision
        converted_tensors = {
            key: tensor.to(target_dtype) for key, tensor in tensors.items()
        }

        # Save the converted tensors back to a new safetensors file
        save_file(converted_tensors, output_path, metadata)
        print(f"Successfully saved converted model to '{output_path}'.")

    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_safetensors_path> <output_safetensors_path> <precision>")
        print("Example: python script.py model.safetensors model_fp16.safetensors fp16")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        precision = sys.argv[3]
        convert_precision(input_path, output_path, precision)