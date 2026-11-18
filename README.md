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

The supplied directory is already a local Git repository with a committed v1.0.0 tag.
If using the ZIP, extract it first; the ZIP includes the hidden `.git` directory.
Keep the extracted directory if you want to reinstall or update from it later.

1. Open Picard 3's Options/Preferences → Plugins → Install Plugin….
2. Select the local repository tab.
3. Browse to the extracted `picard-plugin-featartistsintitles` folder (the folder containing MANIFEST.toml), not an individual Python file or the ZIP.
4. Select version `v1.0.0` if prompted, and install. New installations are enabled automatically.
5. Load or refresh a MusicBrainz release to run the plugin. Inspect the proposed metadata, then Save when satisfied.

This processes metadata loaded from MusicBrainz, like the original plugin; merely opening an unmatched local file does not run it. No audio files have been modified during development.

## Compatibility and changes

Targets plugin API `3.0`. Later Picard versions can use it while they support that API; compatibility with all future versions cannot be guaranteed.

The port uses `MANIFEST.toml`, an `enable(api)` entry point, and API registration methods. Album callbacks now accept `(api, album, metadata, release)`; track callbacks accept `(api, track, metadata, track_node, release=None)`. Picard handles unregistration when disabled.

The original 0.5 plugin recognized only `feat.`. This version also recognizes `featuring`, case-insensitively, and formats both as `(feat. Guest)`. It moves everything after the first marker, trims surrounding credit whitespace, avoids adding an identical trailing suffix, and leaves the artist unchanged if the destination title is empty. Artist sort cleanup remains independent, as in the original.

It expects unparenthesized artist credits such as `Main feat. Guest`; it does not parse every possible credit notation. Separate multi-value `artists` fields and MusicBrainz IDs are unchanged, matching the original scope.

## Validation

Eight unit tests pass, including callback registration with simulated API injection. The manifest was validated with Picard's own standalone validator. Callback signatures and registration were checked against upstream Picard source commit `7b6587886b8d84e3e79c0e77b72667eb755b6a82`.

This has not been tested in the running Picard GUI or against audio files.

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

The original file does not declare a specific license. The repository README says new plugins should use GPL version 2 or a compatible license, which does not identify this particular file's license. No specific upstream license has been invented in the manifest.
