import pytest

#   TODO: Further tests to be written
class TestArtist():
    @pytest.fixture(scope="module")
    def artist_obj(self):
        import os,sys,inspect
        currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parentdir = os.path.dirname(currentdir)
        sys.path.insert(0,parentdir)

        import artist
        import helper

        proxies, headers = helper.setProxy()
        args = helper.argManager()
        return artist.Artist(proxies, headers, args, url="https://www.jiosaavn.com/artist/kuch-bhi-ho-jaye/2EvVc5JXg3I_https://www.jiosaavn.com/artist/udit-narayan-songs/kLtmb7Vh8Rs_")

    def test_getArtistID(self, artist_obj):
        artist_id = artist_obj.getArtistID()
        assert  artist_id == "455127"
        assert type(artist_id) is str

    def test_setArtistID(self, artist_obj):
        artist_obj.setArtistID("455127")
        assert artist_obj.artistID == "455127"

    def test_getArtist(self, artist_obj):
        songs_json, artist_name = artist_obj.getArtist()
        assert type(songs_json) is dict
        assert type(songs_json["songs"]) is list
        assert type(artist_name) is str