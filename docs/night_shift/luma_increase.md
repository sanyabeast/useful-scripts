# luma_increase.bat

README for luma_increase.bat - Batch Script to Increase Monitor Brightness using DDC/CI Control

This document provides information about the `luma_increase.bat` script, including its purpose, functionality, requirements, and usage.

## Overview

The `luma_increase.bat` script is a simple batch file designed to increase the brightness of your monitor using the Display Data Channel/Command Interface (DDC/CI) protocol. It leverages a Python script (`ddc/luma_control.py`) to communicate with the monitor and adjust its backlight level.

## Main Components & Logic

The batch file consists of two identical lines:

```batch
@echo off
py ddc/luma_control.py 1
```

*   `@echo off`:  Suppresses the display of commands as they are executed in the command prompt.
*   `py ddc/luma_control.py 1`: This is the core command. It executes the Python script `ddc/luma_control.py` using the Python interpreter (`py`). The argument '1' passed to the Python script likely represents a specific action or parameter within that script (e.g., increase brightness by a certain amount).  The exact meaning of this argument is determined *within* the `ddc/luma_control.py` script itself and is not defined in this batch file.

The repetition of the line suggests an attempt to execute the command twice, potentially for a more noticeable or cumulative effect on brightness. However, it's important to understand that the effectiveness depends entirely on how `ddc/luma_control.py` handles repeated calls and monitor behavior.

## Assumptions, Requirements & Limitations

**Assumptions:**
*   **Python Installation:**  You have Python installed on your system (preferably Python 3). The `py` command is used to invoke the Python interpreter.
*   **ddc/luma_control.py Script:** A Python script named `ddc/luma_control.py` exists in a relative path accessible from the location where you run this batch file.  This script *must* be present and functional for the batch file to work correctly.
*   **DDC/CI Support:** Your monitor supports DDC/CI communication, and your system has the necessary drivers installed to enable it. Not all monitors support DDC/CI.
*   **ddcutil Installation (Likely):** The `ddc/luma_control.py` script likely relies on a Python library called `ddcutil`.  You will need to install this using pip: `pip install ddcutil`
*   **Permissions:** You have the necessary permissions to access and control your monitor's settings.

**Requirements:**
*   Python 3 (or compatible version)
*   The `ddc/luma_control.py` script.
*   `ddcutil` Python library installed (`pip install ddcutil`) - *This is a very likely requirement.*

**Limitations:**
*   **Monitor Compatibility:**  DDC/CI support varies between monitors. This script may not work with all monitors.
*   **Brightness Increment:** The amount by which the brightness increases depends entirely on how `ddc/luma_control.py` is implemented and what value '1' represents within that script. It might be a percentage, a fixed number of steps, or something else.
*   **Error Handling:**  The batch file itself has minimal error handling. If the Python script fails (e.g., due to DDC/CI communication errors), the batch file will likely just silently fail without providing helpful information.
*   **Security Considerations:** Modifying monitor settings via DDC/CI can potentially have unintended consequences if not handled carefully.  Always review and understand the `ddc/luma_control.py` script before running it.

## Example Use Cases

1.  **Quick Brightness Increase:** Double-clicking the `luma_increase.bat` file will attempt to increase your monitor's brightness by a predefined amount (as determined by `ddc/luma_control.py`). The repetition of the command might result in a more significant change.

## Usage Examples

1.  **Basic Execution:** Simply double-click the `luma_increase.bat` file to execute it. This will attempt to increase your monitor's brightness.

2.  **Execution from Command Line:** Open a command prompt or terminal, navigate to the directory containing `luma_increase.bat`, and type `luma_increase.bat` then press Enter.

## Additional Information & Troubleshooting

*   **Investigate ddc/luma_control.py:** The most important part of understanding this script is examining the contents of `ddc/luma_control.py`.  This will reveal how it interacts with your monitor and what the '1' argument signifies.
*   **Check DDC/CI Support:** Verify that your monitor supports DDC/CI. You can often find this information in the monitor's documentation or online specifications.
*   **ddcutil Command Line Tool:**  You can also use the `ddcutil` command-line tool directly to test and control your monitor's settings. This allows for more granular control and troubleshooting (e.g., `ddcutil vcp get`).
*   **Error Messages:** If you encounter errors, carefully examine any error messages displayed in the command prompt or terminal. These messages can provide clues about the cause of the problem.
*   **Permissions Issues:**  If you are unable to control your monitor's settings, it is possible that you do not have sufficient permissions. Try running the batch file as an administrator (right-click and select "Run as administrator").

## Disclaimer

The use of this script is at your own risk. The author is not responsible for any damage or unintended consequences resulting from its use. Always back up important data before making changes to system settings.
