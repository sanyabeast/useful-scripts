// ==UserScript==
// @name         Page Title Maker
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        */*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=chezzo.com
// @grant    GM_setClipboard
// ==/UserScript==

(function () {
    'use strict';
    let max_filename_length = 255;
    let ellipsis = '…'
    let emojis = [''];
    console.log(emojis)
    let symbols = []
    function get_random_allowed_symbol() { return emojis[Math.floor(Math.random() * emojis.length)] }
    function string_to_filename(v) { return v.replace(/[^a-z^A-Z^а-я^А-Я^0-9^_,. іІїЇєЄҐґ]/gmi, get_random_allowed_symbol()).replace(/ +(?= )/g, '') }
    function get_date_string() { return (new Date()).toDateString().split(' ').splice(1, 4).join(' ').toLowerCase() };

    window.addEventListener('keydown', (evt) => {
        if (evt.keyCode === 80 && evt.ctrlKey) {
            GM_setClipboard(`${window.location.host.toLowerCase()} - ${string_to_filename(document.title).toUpperCase().substring(0, 64)} [${get_date_string()}]`);
        }
    })
    // Your code here...
})();