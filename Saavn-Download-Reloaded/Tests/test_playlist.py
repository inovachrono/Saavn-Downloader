import pytest

#   TODO: Further tests to be written
class TestPlaylist():
    @pytest.fixture(scope="module")
    def playlist_obj(self):
        import os,sys,inspect
        currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parentdir = os.path.dirname(currentdir)
        sys.path.insert(0,parentdir)

        import playlist
        import helper

        proxies, headers = helper.setProxy()
        return playlist.Playlist(proxies, headers, url="https://www.jiosaavn.com/featured/90s-king---kumar-sanu/QeBmhG7Y1uE_")

    def test_getPlaylistID(self, playlist_obj):
        playlist_id = playlist_obj.getPlaylistID()
        assert  playlist_id == "39416670"
        assert type(playlist_id) is str

    def test_setPlaylistID(self, playlist_obj):
        playlist_obj.setPlaylistID("39416670")
        assert playlist_obj.playlistID == "39416670"

    def test_getPlaylist(self, playlist_obj):
        songs_json = playlist_obj.getPlaylist()
        assert type(songs_json) is dict
        assert type(songs_json["songs"]) is list