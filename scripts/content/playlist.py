import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json

from ..download_manager import Manager


class Playlist():
    def __init__(self, proxies, headers, url=None):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.proxies = proxies
        self.headers = headers
        self.playlistID = None
        self.playlistTitle = None
        self.playlistObj = []
        self.songs_json = []
        self.url = url

    def getPlaylistObj(self, url=None):
        if url:
            input_url = url
        else:
            input_url = self.url
        token = input_url.split("/")[-1]
        input_url = "https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=playlist&p=1&n=20&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0".format(token)
        try:
            res = requests.get(input_url, proxies=self.proxies, headers=self.headers)
        except Exception as e:
            print('Error accessing website error: {0}'.format(e))
            exit()
        self.playlistObj = res.json()
        self.playlistID = res.json()["id"]
        self.playlistTitle = res.json()["title"]
        return self.playlistObj
    
    def setPlaylistID(self, playlistID=None):
        self.playlistID = playlistID

    def getPlaylistDetails(self, playlistID=None):
        if playlistID is None:
            playlistID = self.playlistID
        response = requests.get(
            'https://www.jiosaavn.com/api.php?listid={0}&_format=json&__call=playlist.getDetails'.format(playlistID), verify=False, proxies=self.proxies, headers=self.headers)
        if response.status_code == 200:
            self.songs_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
            self.songs_json = json.loads(self.songs_json)
        return self.songs_json
    
    def downloadPlaylist(self):
        if self.playlistID is not None:
            print("Initiating Playlist Downloading of:" + self.playlistTitle)
            manager = Manager()
            manager.downloadSongs(self.playlistTitle, self.getPlaylistDetails())
    
    def start_download(self):
        self.getPlaylistObj()
        # self.getPlaylistObj()
        # print(self.playlistObj)
        self.downloadPlaylist()