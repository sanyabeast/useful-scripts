**YTM Get Playlists**
=====================

A Tampermonkey script that retrieves playlists and their tracks from YouTube Music.

**Features**

* Retrieves playlist information (title, description, tracklist) for the current webpage
* Allows you to customize output format: JSON or plain object
* Optional parameter `oneLinersOnly` enables one-liner track descriptions only

**How it works**

1. The script extracts playlist data from the YouTube Music webpage.
2. You can choose between two output formats:
	+ Plain object (default): returns a JavaScript object with playlist and track information.
	+ JSON string: returns a JSON-formatted string containing the same data.

**Usage**

1. Install Tampermonkey (or similar userscript manager) on your browser.
2. Create a new user script and paste this code into it: [insert link to GitHub Gist or raw URL]
3. Save the script and reload any YouTube Music webpage you want to retrieve playlists from.

**Tips**

* Use `toJson=true` for JSON output, or leave blank for plain object (default).
* Set `oneLinersOnly=true` if you only need one-liner track descriptions.
* This script is designed specifically for YouTube Music; it might not work on other platforms.