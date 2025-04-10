# luma_decrease.bat

README for luma_decrease.bat

This document provides information about the `luma_decrease.bat` script, including its purpose, functionality, requirements, and usage.

## Overview

The `luma_decrease.bat` script is a simple batch file designed to decrease the brightness (luminance) of a connected monitor using DDC/CI communication. It leverages a Python script (`ddc/luma_control.py`) to interact with the monitor's firmware and adjust its brightness level.

## Main Components & Logic

The script consists of a single line that executes a Python script:

*   `@echo off`:  Suppresses command echoing, preventing commands from being displayed in the console window. This is standard practice for cleaner batch file execution.
*   `py ddc/luma_control.py -1`: Executes the `ddc/luma_control.py` Python script using the Python launcher (`py`). The `-1` argument passed to the Python script signifies a decrease in brightness (the specific implementation of how `-1` is interpreted by `ddc/luma_control.py` is detailed within that script itself).  The batch file repeats this line, effectively attempting to decrease brightness twice.

## Assumptions, Requirements & Limitations

*   **Python Installation:** Python must be installed on the system and accessible in the PATH environment variable. The `py` launcher should be associated with a suitable Python interpreter (e.g., Python 3).  Verify this by running `py --version` in your command prompt.
*   **ddc/luma_control.py:** This script is **required**. It's assumed to reside in a subdirectory named `ddc` relative to the location of `luma_decrease.bat`. The functionality and implementation details of this Python script are crucial for the batch file to work correctly.
*   **DDC/CI Support:**  The connected monitor must support DDC/CI (Display Data Channel / Command Interface) communication, which allows software to control certain monitor settings like brightness. Not all monitors support this feature. Check your monitor's documentation or manufacturer website for confirmation.
*   **ddcutil Installation (within ddc/luma_control.py):** The `ddc/luma_control.py` script likely relies on the `ddcutil` Python package.  This needs to be installed separately using pip: `pip install ddcutil`. This is a dependency of the *Python* script, not the batch file itself.
*   **Permissions:** The user running the batch file may need appropriate permissions to access and control the monitor's DDC/CI interface. On some systems (especially Linux), this might require root privileges or membership in specific groups.
*   **Monitor Driver:** A properly installed monitor driver is necessary for DDC/CI communication to function correctly.
*   **Double Execution:** The script repeats the command twice, which may not always be desirable and could lead to over-dimming.  Consider removing one of the lines if a single brightness reduction is sufficient.

## Example Use Cases

The primary use case for this script is to quickly decrease the monitor's brightness from the command line or within an automated workflow (e.g., as part of a desktop automation tool).

## Usage Examples

1.  **Basic Execution:**
    *   Open a Command Prompt window.
    *   Navigate to the directory containing `luma_decrease.bat`.
    *   Run the script by typing `luma_decrease.bat` and pressing Enter.

2. **Automated Scripting (PowerShell Example):**
    You can integrate this batch file into other scripts or automation tools:
    ```powershell
    # PowerShell example to run the batch file
    & 'path/to/luma_decrease.bat'
    ```

## Troubleshooting

*   **Error: `py` is not recognized as an internal or external command:**  This indicates that Python is either not installed or not in your PATH environment variable. Verify the Python installation and ensure it's accessible from the command line.
*   **Error messages related to DDC/CI communication:** These errors usually originate from the `ddc/luma_control.py` script itself.  Consult the documentation for that script for troubleshooting steps. Common causes include: monitor not supporting DDC/CI, incorrect monitor selection (if multiple monitors are connected), or insufficient permissions.
*   **Monitor brightness doesn't change:** Ensure your monitor supports DDC/CI and that the `ddcutil` package is correctly installed within the Python script environment.

## Further Information

*   **ddc/luma_control.py:**  For detailed information about how this script works, refer to its own README or documentation (if available).
*   **ddcutil:**  Learn more about `ddcutil` at [https://ddcutil.com/](https://ddcutil.com/).

## Disclaimer

Modifying monitor settings through DDC/CI can potentially cause unexpected behavior or damage to your hardware if not done correctly. Use this script at your own risk and ensure you understand the implications before running it.
