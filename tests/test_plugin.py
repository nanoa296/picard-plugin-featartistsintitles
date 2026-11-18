import functools
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("plugin", Path(__file__).resolve().parents[1] / "__init__.py")
plugin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plugin)


class PluginTests(unittest.TestCase):
    def track(self, data):
        plugin.move_track_featartists(None, None, data, {})
        return data

    def test_credit_spellings(self):
        for marker in ("feat.", "FEAT.", "featuring", "Featuring"):
            with self.subTest(marker=marker):
                data = self.track(dict(artist=f"Main {marker} Guest", artistsort=f"Main, A {marker} Guest, B", title="Song"))
                self.assertEqual(data, dict(artist="Main", artistsort="Main, A", title="Song (feat. Guest)"))

    def test_album(self):
        data = dict(albumartist="Main feat. Guest", albumartistsort="Main feat. Guest", album="Record")
        plugin.move_album_featartists(None, None, data, {})
        self.assertEqual(data, dict(albumartist="Main", albumartistsort="Main", album="Record (feat. Guest)"))

    def test_no_credit(self):
        for artist in ("Normal", "Little Feat", "Main featuring", "Main feat. "):
            data = dict(artist=artist, title="Song")
            self.assertEqual(self.track(data.copy()), data)

    def test_missing_fields(self):
        self.assertEqual(self.track({}), {})
        self.assertEqual(self.track(dict(artist="Main feat. Guest")), dict(artist="Main feat. Guest"))

    def test_idempotent_and_multiple_guests(self):
        data = dict(artist="Main feat. Guest feat. Other", title="Song")
        self.track(data)
        self.assertEqual(data, dict(artist="Main", title="Song (feat. Guest feat. Other)"))
        self.assertEqual(self.track(data.copy()), data)

    def test_existing_suffix(self):
        data = self.track(dict(artist="Main feat. Guest", title="Song (feat. Guest)"))
        self.assertEqual(data["title"], "Song (feat. Guest)")
        self.assertEqual(data["artist"], "Main")

    def test_unicode_and_unrelated_fields(self):
        data = self.track(dict(artist="Björk featuring 宇多田ヒカル", title="Song", artists=["Björk", "宇多田ヒカル"], musicbrainz_artistid=["a", "b"]))
        self.assertEqual(data["title"], "Song (feat. 宇多田ヒカル)")
        self.assertEqual(data["artists"], ["Björk", "宇多田ヒカル"])
        self.assertEqual(data["musicbrainz_artistid"], ["a", "b"])

    def test_api_registration_and_injection(self):
        class Api:
            def register_album_metadata_processor(self, callback):
                self.album = functools.partial(callback, self)
            def register_track_metadata_processor(self, callback):
                self.track = functools.partial(callback, self)
        api = Api()
        plugin.enable(api)
        data = dict(artist="Main feat. Guest", title="Song")
        api.track(None, data, {}, None)
        self.assertEqual(data["artist"], "Main")
        data = dict(albumartist="Main feat. Guest", album="Album")
        api.album(None, data, {})
        self.assertEqual(data["album"], "Album (feat. Guest)")


if __name__ == "__main__":
    unittest.main()
