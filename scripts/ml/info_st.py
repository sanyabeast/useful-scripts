import sys
from safetensors.torch import safe_open

def print_safetensors_info(file_path):
    try:
        # Open the safetensors file
        with safe_open(file_path, framework="torch") as f:
            # Fetch metadata
            metadata = f.metadata()
            print("\n=== Metadata ===")
            if metadata:
                for key, value in metadata.items():
                    print(f"{key}: {value}")
            else:
                print("No metadata found.")

            # Fetch tensor names and shapes
            print("\n=== Tensors ===")
            for tensor_name in f.keys():
                tensor = f.get_tensor(tensor_name)
                print(f"Tensor Name: {tensor_name}")
                print(f"  Shape: {tensor.shape}")
                print(f"  Data Type: {tensor.dtype}\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <safetensors_file_path>")
    else:
        file_path = sys.argv[1]
        print_safetensors_info(file_path)