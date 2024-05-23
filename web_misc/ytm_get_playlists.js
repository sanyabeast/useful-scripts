/**
 * Retrieves playlists and their tracks from the document.
 * 
 * @param {boolean} [toJson=false] - If true, returns the playlists as a JSON string.
 * @param {boolean} [oneLinersOnly=false] - If true, only returns one-liner track descriptions.
 * @returns {Object|string} - The playlists object or its JSON string representation.
 */
function getPlaylists(toJson = false, oneLinersOnly = false) {
    // Initialize the playlists object
    const playlists = {
        playlists: []
    };

    // Select all containers that hold the playlists
    const listContainers = document.querySelectorAll('#contents');

    // Iterate through each list container
    listContainers.forEach(list => {
        // Initialize a playlist object for each container
        const playlist = {
            tracks: [],
            oneLiners: []
        };

        // Select all items within the container
        const items = list.querySelectorAll('ytmusic-responsive-list-item-renderer');

        // Iterate through each item to extract track information
        items.forEach(item => {
            const title = item.querySelector('.title-column a').textContent;
            const artist = item.querySelector('.secondary-flex-columns .flex-column').textContent;
            const album = item.querySelector('.secondary-flex-columns .flex-column + .flex-column').textContent;

            // Add a one-liner description of the track
            playlist.oneLiners.push(`${artist} - ${title} (${album})`);

            // Add detailed track information if one-liners only is not requested
            if (!oneLinersOnly) {
                playlist.tracks.push({
                    title,
                    artist,
                    album
                });
            }
        });

        // Add the playlist to the playlists array if it contains any tracks
        if (playlist.oneLiners.length > 0) {
            playlists.playlists.push(playlist);
        }
    });

    // Return the playlists object or its JSON string representation based on the toJson parameter
    return toJson ? JSON.stringify(playlists) : playlists;
}

// Example usage: Retrieve playlists as a JSON string with detailed track information
getPlaylists(true, false);