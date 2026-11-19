# Feat. Artists in Titles — Picard 3 port

Moves featured artist credits when Picard loads MusicBrainz album/track metadata:

| Field | Before | After |
| --- | --- | --- |
| artist | Main feat. Guest | Main |
| title | Song | Song (feat. Guest) |
| albumartist | Main featuring Guest | Main |
| album | Record | Record (feat. Guest) |

Also removes the featured suffix from `artistsort` and `albumartistsort`.

## Install

1. Open Picard 3's Options/Preferences → Plugins → Install Plugin….
2. Select the URL tab and enter `https://github.com/nanoa296/picard-plugin-featartistsintitles`.
3. Select version `v1.0.1` and install. New installations are enabled automatically.
4. Load or refresh a MusicBrainz release, inspect the proposed metadata, then Save.

For development, clone this repository and select its directory in the local repository tab instead.
A GitHub source ZIP alone is not a Git repository; use the repository URL or a Git clone.

This processes metadata loaded from MusicBrainz, like the original plugin; merely opening an unmatched local file does not run it.

## Compatibility and changes

Targets plugin API 3.0, and all Picard versions supporting that API.

The port uses `MANIFEST.toml`, an `enable(api)` entry point, and API registration methods. Album callbacks now accept `(api, album, metadata, release)`; track callbacks accept `(api, track, metadata, track_node, release=None)`. Picard handles unregistration when disabled.

The original 0.5 plugin recognized only `feat.`. This version also recognizes `featuring`, case-insensitively, and formats both as `(feat. Guest)`. It moves everything after the first marker, trims surrounding credit whitespace, avoids adding an identical trailing suffix, and leaves the artist unchanged if the destination title is empty. Artist sort cleanup remains independent, as in the original.

It expects unparenthesized artist credits such as `Main feat. Guest`; it does not parse every possible credit notation. Separate multi-value `artists` fields and MusicBrainz IDs are unchanged, matching the original scope.

## Validation

Run tests from this folder with:

```sh
python3 -m unittest discover -s tests -v
```

## Developer documentation

- [Picard v2-to-v3 migration guide](https://github.com/metabrainz/picard/blob/master/docs/Plugin2to3MigrationGuide.md)
- [Plugin API reference](https://github.com/metabrainz/picard/blob/master/docs/PLUGINSV3/API.md)
- [Manifest and development guide](https://github.com/metabrainz/picard/blob/master/docs/PLUGINSV3/MANIFEST.md)
- [Installation documentation](https://picard-docs.musicbrainz.org/en/latest/config/options_plugins.html)

## Attribution

Adapted from [Feat. Artists in Titles 0.5](https://github.com/metabrainz/picard-plugins/blob/2.0/plugins/featartistsintitles/featartistsintitles.py) by Lukas Lalinsky, Michael Wiencek, Bryan Toth, and JeromyNix (NobahdiAtoll). The original source is preserved in `original-v0.5.py.txt`.

This is an independently developed third-party plugin, with no affiliation to the original authors or the MusicBrainz Picard project.

## License

[MIT](LICENSE) © 2026 nanoa296.
