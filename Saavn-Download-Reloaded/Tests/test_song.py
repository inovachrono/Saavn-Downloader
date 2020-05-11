import pytest

#   TODO: Further tests to be written
class TestSong():
    @pytest.fixture(scope="module")
    def song_obj(self):
        import os,sys,inspect
        currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parentdir = os.path.dirname(currentdir)
        sys.path.insert(0,parentdir)

        import song
        import helper

        proxies, headers = helper.setProxy()
        return song.Song(proxies, headers, url="https://www.jiosaavn.com/song/dekha-ek-khwab/QVsJYCJYAV0")

    def test_getSongID(self, song_obj):
        song_id = song_obj.getSongID()
        assert song_id == "13bQVh6n"
        assert isinstance(song_id, str)

    def test_setSongID(self, song_obj):
        song_obj.setSongID("13bQVh6n")
        assert song_obj.songID == "13bQVh6n"

    def test_getSong(self, song_obj):
        song_json = song_obj.getSong()
        assert isinstance(song_json, dict)
        assert song_obj.songID in song_json
        assert song_json[song_obj.songID].get("more_info", None) is not None