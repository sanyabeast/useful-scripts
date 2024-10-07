**Page Title Maker**
=====================

A Tampermonkey script that helps you create custom page titles using Ctrl+S and Ctrl+P shortcuts.

**Features**

* Creates a unique filename based on the current webpage title
* Includes date information in the filename for version control purposes
* Allows you to customize the allowed characters for the filename (e.g., emojis)
* Saves the generated filename to your clipboard

**How it works**

1. The script listens for Ctrl+S and Ctrl+P key presses.
2. When a key press event is detected, the script generates a unique filename based on the current webpage title using the `string_to_filename` function.
3. The filename includes date information in the format "YYYY-MM-DD" to help with version control purposes.
4. You can customize the allowed characters for the filename by modifying the `emojis` array.

**Usage**

1. Install Tampermonkey (or similar userscript manager) on your browser.
2. Create a new user script and paste this code into it: [insert link to GitHub Gist or raw URL]
3. Save the script and reload any webpage you want to use with Ctrl+S and Ctrl+P shortcuts.

**Tips**

* You can customize the allowed characters for the filename by modifying the `emojis` array.
* The generated filename is case-insensitive, so it won't affect your file system's organization or searchability.
* This script only works on webpages that have a title attribute set. If no title is found, an empty string will be used as the default.