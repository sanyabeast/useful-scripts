// ==UserScript==
// @name         Copy as Filename
// @author       @sanyabeast
// @version      1.0
// @grant        GM_registerMenuCommand
// @grant        GM_setClipboard
// @match        *://*/*
// ==/UserScript==

/**
 * Copies the selected text as a sanitized filename to the clipboard.
 */
function copySelectedAsFilename() {
    // Get the selected text
    const selectedText = window.getSelection().toString();

    // Remove disallowed symbols and replace them with '-'
    const sanitizedText = selectedText.replace(/[<>:"\/\\|?*\x00-\x1F]/g, "");

    // Copy the sanitized text to the clipboard
    GM_setClipboard(sanitizedText);
}

// Register the menu command for Ctrl+Alt+C
GM_registerMenuCommand("Copy Field Name", copySelectedAsFilename);

/**
 * Event listener for the keydown event to capture Ctrl+Alt+C shortcut.
 * @param {KeyboardEvent} evt - The keyboard event object.
 */
window.addEventListener('keydown', (evt) => {
    if (evt.ctrlKey && evt.altKey && evt.key === 'c') {
        copySelectedAsFilename();
    }
});