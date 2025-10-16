import json
import requests

from ..download_manager import Manager


class Playlist():
    def __init__(self, proxies, headers, url=None):
        self.proxies = proxies
        self.headers = headers
        self.playlistID = None
        self.songs_json = []
        self.url: str | None = url

    def getPlaylistID(self, url: str | None=None):
        if url:
            input_url = url
        elif self.url:
            input_url = self.url
        else:
            print("Please enter a valid playlist URL")
            exit()
        token = input_url.split("/")[-1]
        input_url = "https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=playlist&p=1&n=20&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0".format(token)
        try:
            res = requests.get(input_url, proxies=self.proxies, headers=self.headers)
        except Exception as e:
            print("Error accessing website error: {0}".format(e))
            exit()
        self.playlistID = res.json()["id"]
        return self.playlistID
    
    def setPlaylistID(self, playlistID=None):
        self.playlistID = playlistID

    def getPlaylist(self, playlistID=None):
        if playlistID is None:
            playlistID = self.playlistID
        response = requests.get(
            "https://www.jiosaavn.com/api.php?listid={0}&_format=json&__call=playlist.getDetails".format(playlistID), proxies=self.proxies, headers=self.headers)
        if response.status_code == 200:
            self.songs_json = [x for x in response.text.splitlines() if x.strip().startswith("{")][0]
            self.songs_json = json.loads(self.songs_json)
        return self.songs_json
    
    def downloadPlaylist(self):
        if self.playlistID is not None:
            print("Initiating Playlist Downloading")
            manager = Manager()
            manager.downloadSongs(self.getPlaylist())
    
    def start_download(self):
        self.getPlaylistID()
        self.downloadPlaylist()