# mousey.py

README: mousey.py - A Simple Mouse Movement Script

This document provides information about the `mousey.py` script, including its purpose, functionality, requirements, limitations, and usage examples.

## Overview

The `mousey.py` script is a simple Python program designed to continuously move the mouse cursor a small distance (1 pixel) to the right at regular intervals (5 seconds).  It utilizes the `pyautogui` library for mouse control and `time` for pausing execution.

## Main Components & Logic

The script consists of a single, infinite loop (`while True:`).

*   **Import Statements:** The script begins by importing necessary libraries:
    *   `pyautogui`:  Provides functions to control the mouse and keyboard. This library is essential for moving the cursor.
    *   `time`: Provides time-related functions, specifically used here for pausing execution.
*   **Infinite Loop:** The `while True:` loop ensures that the script runs continuously until manually terminated (e.g., by pressing Ctrl+C in the terminal).
*   **Mouse Movement:** Inside the loop, `pyautogui.moveRel(1, 0)` moves the mouse cursor relative to its current position.  The arguments `1` and `0` specify a movement of 1 pixel horizontally (right) and 0 pixels vertically.
*   **Pause:** `time.sleep(5)` pauses the script's execution for 5 seconds after each mouse movement. This prevents the cursor from moving too quickly and potentially interfering with user interaction or other processes.

## Assumptions, Requirements & Limitations

### Requirements:

*   **Python Installation:**  The script requires a Python interpreter (version 3.x is recommended).
*   **pyautogui Library:** The `pyautogui` library must be installed. It can be installed using pip: `pip install pyautogui`.
*   **Operating System Compatibility:** While `pyautogui` generally works across Windows, macOS, and Linux, behavior might vary slightly depending on the operating system and desktop environment.

### Assumptions:

*   The script assumes that the user has sufficient permissions to control the mouse cursor.  On some systems (especially macOS), you may need to grant accessibility permissions to Python or your IDE for `pyautogui` to function correctly.
*   It's assumed that moving the mouse 1 pixel at a time won't cause any unintended consequences in the user's workflow.

### Limitations:

*   **Continuous Movement:** The script moves the mouse continuously. This can be disruptive if not carefully managed.  Consider adding options for stopping or controlling the movement more precisely (e.g., based on time, events, or user input).
*   **Single Direction:** Currently, the script only moves the mouse to the right. It lacks flexibility in terms of direction and distance.
*   **No Error Handling:** The script doesn't include any error handling.  If `pyautogui` encounters an issue (e.g., due to permissions or hardware problems), the script will likely crash without a helpful message.
*   **Screen Boundaries:** The script does not check for screen boundaries. If the mouse is already at the right edge of the screen, moving it further to the right will cause it to wrap around to the left edge (or potentially trigger other OS-dependent behavior).

## Example Use Cases

The current implementation has limited practical use cases as written. However, it serves as a basic foundation for more complex mouse automation tasks.

*   **Testing Mouse Input:**  The script could be used to test mouse input handling in other applications or games (though this is not its primary purpose).
*   **Simple Automation Task (with modification):** With modifications, the script could form part of a larger automation workflow where small, controlled mouse movements are needed.

## Usage Examples

1.  **Save the Script:** Save the code as `mousey.py`.
2.  **Install pyautogui:** Open a terminal or command prompt and run: `pip install pyautogui`
3.  **Run the Script:** Execute the script from the terminal using: `python mousey.py`
4.  **Stop the Script:** Press Ctrl+C in the terminal to terminate the script.

## Further Development Ideas

*   **Add Command-Line Arguments:** Allow users to specify the movement distance, interval, and direction via command-line arguments.
*   **Implement Screen Boundary Checks:** Prevent the mouse from moving off-screen.
*   **Introduce User Input:**  Allow users to control the script's behavior in real-time (e.g., start/stop, change speed).
*   **Add Error Handling:** Implement `try...except` blocks to handle potential errors gracefully.
*   **Implement a GUI:** Create a graphical user interface for easier configuration and control.
*   **Randomize Movement:** Introduce randomness in the movement distance or direction to simulate more natural mouse behavior.

## Contact

[Your Name/Organization] - [Your Email Address (Optional)]
