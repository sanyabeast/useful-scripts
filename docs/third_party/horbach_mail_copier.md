# horbach_mail_copier.js

## HorbachMailCopier - README

This script, designed for use with Tampermonkey or similar user script managers, adds a convenient 'copy' button to each row of the Mailchimp Customer Journey analysis table. This allows users to quickly copy key metrics (open rate, click rate, sends, revenue, and revenue received) into spreadsheets or other documents.

### Overview

The `HorbachMailCopier` script enhances the Mailchimp Customer Journey report by adding a 'copy' button next to each row. Clicking this button copies a formatted string containing key metrics for that row to the user's clipboard, streamlining data extraction and analysis.

### Main Components & Logic

1.  **Initialization:** The script checks if it has already been initialized and verifies that the current URL matches the expected Mailchimp Customer Journey report URL. This prevents multiple instances of the script from running on the same page.
2.  **Table Identification:** It searches for the 'Journey analysis' table within the DOM using `document.querySelectorAll('div')` and checks for a header element with text content equal to 'Journey analysis'.
3.  **Copy Button Creation:** For each row in the identified table, it creates a copy button (`<div>`) containing an image icon.
4.  **Data Extraction & Formatting:** When the copy button is clicked, the script extracts the values for sends, open rate, click rate, revenue, and revenue received from the corresponding cells of the current row using `querySelector` with nth-child selectors. These values are then formatted into a string based on the `ROW_TEMPLATE`.
5.  **Clipboard Copying:** The formatted string is copied to the user's clipboard using `GM_setClipboard`. This function is provided by Tampermonkey and allows user scripts to interact with system functionalities like the clipboard.
6.  **Tooltip Display:** A temporary tooltip appears briefly near the copy button, confirming that the data has been copied to the clipboard.

### Assumptions, Requirements & Limitations

*   **Mailchimp Customer Journey Report:** The script is specifically designed for the Mailchimp Customer Journey report page. It relies on specific HTML structure and class names present only in this section of Mailchimp's interface.
*   **Tampermonkey (or equivalent):**  The script requires a user script manager like Tampermonkey, Greasemonkey, or Violentmonkey to be installed in the browser.
*   **GM_setClipboard:** The `GM_setClipboard` function is essential for copying data to the clipboard. This function is provided by Tampermonkey and other compatible user script managers.
*   **HTML Structure Dependency:**  The script's functionality depends on the HTML structure of the Mailchimp Customer Journey report remaining consistent. Changes to Mailchimp's website could break the script.
*   **Data Parsing:** The `parse_float` function is used to extract numeric values from text content, handling potential formatting issues (e.g., commas as decimal separators).  It assumes that the data in the table cells can be parsed as floating-point numbers.

### Example Use Cases

*   **Data Export:** Quickly copy row data for import into spreadsheets (Google Sheets, Microsoft Excel) or other analysis tools.
*   **Reporting:** Generate custom reports by extracting key metrics from multiple rows and combining them in a document.
*   **Automation:** Integrate the copied data into automated workflows using external scripts or applications.

### Usage Instructions

1.  **Install Tampermonkey (or equivalent):** If you don't already have one, install a user script manager like Tampermonkey for your browser.
2.  **Create a New User Script:** In Tampermonkey, create a new user script.
3.  **Copy and Paste the Code:** Copy the entire code of `horbach_mail_copier.js` and paste it into the newly created user script editor.
4.  **Save the Script:** Save the user script.
5.  **Navigate to Mailchimp Customer Journey Report:** Open the Mailchimp Customer Journey report page in your browser (e.g., `admin.mailchimp.com/customer-journey`).
6.  **Observe the Copy Buttons:** The script will automatically add a 'copy' button next to each row of the table.
7.  **Click the Copy Button:** Click the copy button on the desired row to copy the formatted data to your clipboard.

### Configuration Options (Advanced Users)

The following constants can be modified at the beginning of the script to customize its behavior:

*   `ROW_TEMPLATE`: Defines the format string for the copied data.  The placeholders (`open_rate%`, `click_rate%`, etc.) are replaced with the actual values extracted from the table row.
*   `ROW_SPLIT_SYMBOl`: Specifies the separator character used to separate the values in the formatted string.
*   `COPY_ICON_IMAGE`:  Defines the base64 encoded image data for the copy button icon. You can replace this with a URL to an external image if desired.

### Troubleshooting

*   **Script Not Running:** Ensure that Tampermonkey is enabled and that the script has not been disabled by any browser extensions or security settings.
*   **Incorrect Table Identified:** Verify that the Mailchimp Customer Journey report's HTML structure hasn't changed.  If it has, you may need to update the table identification logic in the script.
*   **Data Not Copied:** Check for JavaScript errors in the browser console (usually accessible by pressing F12). The error messages might provide clues about what went wrong.

### Disclaimer

The author is not responsible for any data loss or unexpected behavior caused by using this script. Use it at your own risk and always back up important data before running user scripts.
