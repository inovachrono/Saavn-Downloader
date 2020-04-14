from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import logger
import sys

from download_manager import Manager


class Playlist():
    def __init__(self, proxies, headers, url=None):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.proxies = proxies
        self.headers = headers
        self.playlistID = None
        self.songs_json = []
        self.url = url

    def getPlayListID(self):
        input_url = self.url
        try:
            res = requests.get(input_url, proxies=self.proxies, headers=self.headers)
        except Exception as e:
            logger.error('Error accessing website error: ' + str(e))
            exit()
        soup = BeautifulSoup(res.text, "lxml")
        self.playlistID = soup.select(".flip-layout")[0]["data-listid"]
        return self.playlistID
    
    def setPlaylistID(self, playlistID=None):
        self.playlistID = playlistID

    def getPlayList(self, playlistID=None):
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
            print("Initiating PlayList Downloading")
            manager = Manager()
            manager.downloadSongs(self.getPlayList())
            sys.exit()
    
    def start_download(self):
        self.getPlayListID()
        self.downloadPlaylist()