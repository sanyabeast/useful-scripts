**InstaClear: Remove Instagram Image & Video Overlays**
=====================================================

A lightweight JavaScript script that monitors your Instagram journey and removes annoying overlays from images and videos, allowing you to right-click and save them without any extra steps.

**Features**

* Removes overlay divs covering images and videos on Instagram
* Allows right-click saving of high-resolution images

**How it works**

1. InstaClear uses a MutationObserver to monitor changes in the Instagram page's DOM.
2. When an image or video element is detected, the script checks if there are any overlay divs covering them.
3. If overlays are found, they are removed from the DOM using JavaScript.

**Usage**

1. Install Tampermonkey (or similar userscript manager) on your browser.
2. Create a new user script and paste this code into it: [insert link to GitHub Gist or raw URL]
3. Save the script and reload Instagram.com in your browser.
4. Right-click on images and videos to save them without any overlay divs.