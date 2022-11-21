// ==UserScript==
// @name         Rundavou Youtube
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://www.youtube.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=youtube.com
// @grant    GM_setClipboard
// ==/UserScript==

(function () {
    'use strict';
    console.log(1);

    let max_filename_length = 255;
    let ellipsis = '…'
    let emojis = [''];
    console.log(emojis)
    let symbols = []
    function get_random_allowed_symbol() { return emojis[Math.floor(Math.random() * emojis.length)] }
    function clog() { console.log("%c[rundavou-yt] [i]", 'color: #ff9800;', ...arguments) }
    function string_to_filename(v) { return v.replace(/[^a-z^A-Z^а-я^А-Я^0-9^_,. іІїЇєЄҐґ]/gmi, get_random_allowed_symbol()).replace(/ +(?= )/g, '') }
    let elements = {
        get video_title() { return document.querySelector('h1.ytd-watch-metadata yt-formatted-string'); },
        get channel_author_name() { return document.querySelector('div.ytd-channel-name a'); },
    };

    let scenarios = [
        {
            name: 'copy_video_name_formatted',
            check: (el, event_name, evt) => {
                return event_name === 'copy' && (el === elements.video_title || elements.video_title.contains(el));
            },
            handle: (el, event_name, evt) => {
                evt.preventDefault()
                let title = elements.video_title.innerText;
                let artist = elements.channel_author_name.innerText;
                console.log(elements.channel_author_name)
                let video_name = `${string_to_filename(artist.toUpperCase())} - ${string_to_filename(title)}`;
                if (video_name.length > max_filename_length) {
                    video_name = video_name.substring(0, max_filename_length) + ellipsis;
                }
                clog(`computed video name: ${video_name}`)
                GM_setClipboard(video_name)
            }
        }
    ];

    let event_names = ['mousedown', 'contextmenu', 'copy']
    event_names.forEach((event_name) => {
        window.addEventListener(event_name, (evt) => {
            if (!evt.shiftKey) {
                scenarios.forEach((scenario, index) => {
                    clog(`checking conditions for scenario "${scenario.name}"`)
                    if (scenario.check(evt.target, event_name, evt)) {
                        clog(`running scenario "${scenario.name}"`)
                        scenario.handle(evt.target, event_name, evt);
                    }
                })
            }
        }, false)
    });

    // Your code here...
})();