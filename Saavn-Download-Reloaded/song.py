import requests
from bs4 import BeautifulSoup
from pySmartDL import SmartDL
import json
import base64
import html
import os

from pyDes import *
from helper import setProxy, setDecipher, formatFilename, argManager
from download_manager import Manager

class Song():
    def __init__(self, proxies, headers, url=None):
        self.session = requests.session()
        self.session.headers.update(headers)
        self.session.proxies.update(proxies)
        self.payload = {
                '_marker': '0',
                'cc': '',
                'pids': None,
                'ctx': 'android',
                'network_operator': '',
                'v': '224',
                'app_version': '6.8.2',
                'build': 'Pro',
                'api_version': '4',
                'network_type': 'WIFI',
                '_format': 'json',
                '__call': 'song.getDetails',
                'manufacturer': 'Samsung',
                'readable_version': '6.8.2',
                'network_subtype': '',
                'model': 'Samsung Galaxy S10'
            }
        self.args = argManager()
        self.url = url
        self.songID = None
        self.song_json = None

    def setSongID(self, song_id):
        self.songID = song_id

    def getSongID(self):
        if self.url:
            input_url = self.url
        else:
            input_url = input("Enter the URL : ")
        response = self.session.get(input_url)
        try:
            soup = BeautifulSoup(response.content, "lxml")
            song_json = soup.select(".hide.song-json")[0]
            song_json = json.loads(song_json.text)
            self.songID = song_json["songid"]
            return self.songID
        except Exception as e:
            print("Unable to get the song from URL")
            print(e)
            exit()

    def getSong(self, song_id=None):
        if song_id is None:
            self.payload["pids"] = self.getSongID()
        else:
            self.payload["pids"] = song_id
        url = "https://www.jiosaavn.com/api.php" # POST request
        response = self.session.post(url, data=self.payload)
        try:
            song_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
            self.song_json = json.loads(song_json)
        except Exception as e:
            print("An error occured getting the song information")
            print(e)
        finally:
            return self.song_json

    def downloadSong(self, album_name='songs', artist_name='Non-Artist'):
        des_cipher = setDecipher()
        song = self.song_json[self.songID]
        try:
            enc_url = base64.b64decode(song["more_info"]['encrypted_media_url'].strip())
            dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
            dec_url = dec_url.replace('_96.mp4', '_320.mp4')
            filename = html.unescape(song['title']) + '.m4a'
            filename = formatFilename(filename)
        except Exception as e:
            print('Download Error : {0}'.format(e))
        try:
            if self.args.outFolder is None:
                location = os.path.join(os.getcwd(), artist_name, album_name, filename)
            else:
                location = os.path.join(self.args.outFolder, artist_name, album_name, filename)
            if os.path.isfile(location):
                print("Downloaded {0}".format(filename))
            else :
                print("Downloading {0}".format(filename))
                obj = SmartDL(dec_url, location)
                obj.start()
                try:
                    name = song['subtitle']
                except:
                    name = ''
                manager = Manager()
                try:
                    song["song"] = song["title"]
                    song["primary_artists"] = song["more_info"]["artistMap"]["primary_artists"][0]["name"]
                    song["album"] = song["more_info"]["album"]
                    song["singers"] = ", ".join([artist["name"] for artist in song["more_info"]["artistMap"]["primary_artists"]])
                    song["music"] = song["more_info"]["music"]
                    song["starring"] = ""
                    song["label"] = song["more_info"]["label"]
                except Exception as e:
                    print("Error creating song tag information")
                    print(e)
                manager.addtags(location, song, name)
                print('\n')
        except Exception as e:
            print('Download Error : {0}'.format(e))

    def start_download(self):
        self.getSongID()
        self.getSong()
        self.downloadSong()


if __name__ == '__main__':
    pass