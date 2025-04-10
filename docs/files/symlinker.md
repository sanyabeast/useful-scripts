# symlinker.py

Symlinker Script - Creates Symbolic Links Based on YAML Configuration

This script automates the creation of symbolic links (symlinks) between directories based on a configuration file written in YAML format.

**Purpose:** To simplify the process of creating symlinks, especially when dealing with multiple source and target locations and patterns. This is particularly useful for keeping files synchronized across different installations or versions of software.

**Example Configuration (config.yaml):**
```yaml
- source_dir: C:/ML/ComfyUI_windows_portable/ComfyUI/models/checkpoints
  target_dir: C:/ML/a1111/models/Stable-diffusion
  match:
  - sd.1.5-* 
  - sdxl.1.0-*
  include_nested: false
- source_dir: C:/ML/ComfyUI_windows_portable/ComfyUI/models/vae
  target_dir: C:/ML/a1111/models/VAE
  match:
  - "*"
  include_nested: true
```

**Main Components and Logic:**

1. **Configuration Loading:** The script reads a YAML configuration file specified as an argument.
2. **YAML Parsing:** Uses the `yaml` library to parse the YAML data into Python dictionaries.
3. **Directory Handling:**  For each entry in the config:
   - Converts source and target directories to absolute paths using `os.path.abspath()`.
   - Creates the target directory if it doesn't exist using `os.makedirs()`.
4. **Invalid Symlink Removal:** Before creating new symlinks, the script checks for and removes any existing broken (invalid) symbolic links in the target directory.
5. **File Matching:**  Uses `glob` to find files matching specified patterns within the source directories. The `include_nested` flag determines whether to search recursively through subdirectories.
6. **Symlink Creation:** For each matched file:
   - Extracts the filename from the full path.
   - Constructs the target symlink path.
   - Checks if a file with the same name already exists in the target directory; skips creation if it does.
   - Creates the symbolic link using `os.symlink()`.  Handles potential `OSError` exceptions during symlink creation (e.g., due to permissions issues).
7. **Argument Parsing:** Uses `argparse` to handle command-line arguments, specifically the path to the configuration file.

**Assumptions, Requirements, and Limitations:**

*   **Python Environment:** Requires Python 3.x installed on your system.
*   **Dependencies:**  Requires the `PyYAML` library. Install using: `pip install PyYAML`
*   **Permissions:** The script needs write permissions in both the source and target directories to create symlinks.
*   **File Existence:** Assumes that the files specified in the YAML configuration exist at the given source paths.
*   **Overwriting:**  The script will *not* overwrite existing files in the target directory. It will skip creating a symlink if a file with the same name already exists.
*   **Error Handling:** While it includes basic error handling for `OSError` during symlink creation, more robust error logging and reporting could be added.
*   **YAML Format:** The YAML configuration must adhere to the expected format (see example above).  Incorrect formatting will lead to parsing errors.

**Example Use Cases:**

*   **Syncing Models between ComfyUI and Automatic1111:** As demonstrated in the example config, this script can be used to create symlinks for models (checkpoints, VAEs) so that changes in one location are reflected in the other.
*   **Managing Multiple Versions of Software:**  Create symlinks to point to specific versions of libraries or tools.
*   **Centralized File Access:** Create symlinks to provide a single access point to files stored in multiple locations.

**Usage:**

1. **Save the script as `symlinker.py`.**
2. **Create a YAML configuration file (e.g., `config.yaml`) with your desired source and target directories, matching patterns, and include_nested settings.**  See the example above for formatting.
3. **Run the script from the command line:**

```bash
python symlinker.py path/to/your/config.yaml
```

   Replace `path/to/your/config.yaml` with the actual path to your configuration file.

**Additional Notes:**

*   The script prints messages to the console indicating which symlinks are being created or skipped, and any errors encountered.
*   Consider adding more sophisticated error handling (e.g., logging to a file) for production use.
*   For very large numbers of files, consider optimizing the globbing process to improve performance.

**Author:** [Your Name/Organization]
**Date:** 2023-10-27
