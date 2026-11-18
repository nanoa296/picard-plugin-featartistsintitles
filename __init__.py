"""Move featured artist credits into titles using Picard's plugin API 3.0.

Based on Feat. Artists in Titles 0.5 by Lukas Lalinsky, Michael Wiencek,
Bryan Toth, and JeromyNix (NobahdiAtoll). See README.md for provenance.
"""

import re

# Split at the first marker so repeated featured credits move together.
_FEAT_RE = re.compile(r"^(.+?)\s+(?:feat\.|featuring)\s*(\S.*)$", re.IGNORECASE | re.DOTALL)


def _move_credit(metadata, artist_key, sort_key, title_key):
    match = _FEAT_RE.match(metadata.get(artist_key, ""))
    if match and metadata.get(title_key, ""):
        main, guest = (part.strip() for part in match.groups())
        suffix = f" (feat. {guest})"
        title = metadata[title_key]
        if not title.casefold().endswith(suffix.casefold()):
            metadata[title_key] = title + suffix
        metadata[artist_key] = main
    match = _FEAT_RE.match(metadata.get(sort_key, ""))
    if match:
        metadata[sort_key] = match.group(1).strip()


def move_album_featartists(api, album, metadata, release):
    _move_credit(metadata, "albumartist", "albumartistsort", "album")


def move_track_featartists(api, track, metadata, track_node, release=None):
    _move_credit(metadata, "artist", "artistsort", "title")


def enable(api):
    """Picard automatically unregisters these processors on disable."""
    api.register_album_metadata_processor(move_album_featartists)
    api.register_track_metadata_processor(move_track_featartists)
