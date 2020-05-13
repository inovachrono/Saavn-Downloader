import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import ast
import logger
import re
import json

from ..download_manager import Manager

class Album():
    def __init__(self, proxies, headers, url=None):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.proxies = proxies
        self.headers = headers
        self.albumID = None
        self.songs_json = []
        self.album_name = ''
        self.url = url

    def getAlbumID(self, url=None):
        if url:
            input_url = url
        else:
            input_url = self.url
        try:
            res = requests.get(input_url, proxies=self.proxies, headers=self.headers)
        except Exception as e:
            logger.error('Error accessing website error: ' + str(e))
            exit()
        soup = BeautifulSoup(res.text, 'lxml')
        try:
            self.albumID = soup.select(".play")[0]["onclick"]
            self.albumID = ast.literal_eval(re.search("\[(.*?)\]", self.albumID).group())[1]
        except:
            self.albumID = soup.select("#share-btn")[0]["onclick"]
            self.albumID = re.search('\".*id.*:.*\d+\"', self.albumID).group()
            self.albumID = re.search("\d+", self.albumID).group()
        return self.albumID
    
    def setAlbumID(self, albumID):
        self.albumID = albumID
    
    def getAlbum(self, albumID=None):
        if albumID is None:
            albumID = self.albumID
        response = requests.get(
            'https://www.jiosaavn.com/api.php?_format=json&__call=content.getAlbumDetails&albumid={0}'.format(albumID),
            verify=False, proxies=self.proxies, headers=self.headers)
        if response.status_code == 200:
            self.songs_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
            self.songs_json = json.loads(self.songs_json)
            print("Album name: ",self.songs_json["name"])
            self.album_name=self.songs_json["name"]
            self.album_name = self.album_name.replace("&quot;", "'")
        return self.songs_json, self.album_name
    
    def downloadAlbum(self, artist_name=''):
        if self.albumID is not None:
            print("Initiating Album Download")
            manager = Manager()
            self.getAlbum()
            if artist_name:
                manager.downloadSongs(self.songs_json, self.album_name, artist_name=artist_name)
            else:
                manager.downloadSongs(self.songs_json, self.album_name)
    
    def start_download(self):
        self.getAlbumID()
        self.downloadAlbum()