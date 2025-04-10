# info_st.py

README for info_st.py - Safetensors File Information Script

This script provides information about safetensors files, including metadata and tensor details.

**Version:** 1.0
**Author:** [Your Name/Team Name]
**Date:** October 26, 2023

## Overview

The `info_st.py` script is a utility designed to inspect safetensors files. Safetensors are a safer and faster alternative to pickle for storing tensors, particularly in the context of machine learning models. This script allows you to view the metadata associated with a safetensors file (if any) and list all the tensors contained within it, along with their names, shapes, and data types.

## Main Components & Logic

The script is structured as follows:

1.  **Imports:** Imports necessary libraries: `sys` for command-line arguments and `safetensors.torch.safe_open` for handling safetensors files.
2.  **`print_safetensors_info(file_path)` Function:** This is the core function that performs the inspection:
    *   It takes the path to a safetensors file as input (`file_path`).
    *   It uses `safe_open` from the `safetensors` library to open the file in read-only mode, specifying 'torch' as the framework.
    *   **Metadata Extraction:** It attempts to retrieve and print any metadata associated with the safetensors file. If no metadata is present, it prints a message indicating this.
    *   **Tensor Listing:**  It iterates through all tensors stored within the safetensors file using `f.keys()`. For each tensor:
        *   It retrieves the tensor's name.
        *   It retrieves the tensor itself and extracts its shape and data type (dtype).
        *   It prints these details to the console in a formatted manner.
    *   **Error Handling:**  A `try...except` block is used to catch potential exceptions during file opening or processing, printing an error message if something goes wrong.
3.  **Main Execution Block (`if __name__ == '__main__':`)**: This section handles command-line argument parsing:
    *   It checks if the correct number of arguments (exactly one: the safetensors file path) is provided.
    *   If the number of arguments is incorrect, it prints a usage message to guide the user.
    *   If the argument count is correct, it assigns the file path from `sys.argv[1]` and calls the `print_safetensors_info` function to process the specified safetensors file.

## Assumptions & Requirements

*   **Python Environment:** The script requires a Python environment (version 3.7 or higher is recommended).
*   **Safetensors Library:**  The `safetensors` library must be installed. You can install it using pip:
    ```bash
pip install safetensors
```
*   **File Path:** The script assumes that the provided file path (`<safetensors_file_path>`) is a valid and accessible path to a safetensors file.
*   **Framework Compatibility**:  The `safe_open` function explicitly specifies `framework=
