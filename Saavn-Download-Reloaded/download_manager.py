from mutagen.mp4 import MP4, MP4Cover
import urllib.request
import html
import json
import base64
import logger
import os

from pySmartDL import SmartDL

from pyDes import *
from helper import setDecipher, formatFilename, argManager

class Manager():
    def __init__(self):
        self.unicode = str
        self.args = argManager()
    
    def downloadSongs(self, songs_json, album_name='songs', artist_name='Non-Artist'):
        des_cipher = setDecipher()
        for song in songs_json['songs']:
            try:
                enc_url = base64.b64decode(song['encrypted_media_url'].strip())
                dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
                # dec_url = dec_url.replace('_96.mp4', '_320.mp4')
                filename = html.unescape(song['song']) + '.m4a'
                filename = formatFilename(filename)
            except Exception as e:
                logger.error('Download Error' + str(e))
            try:
                if self.args.outFolder is None:
                    location = os.path.join(os.path.sep, os.getcwd(), artist_name, album_name, filename)
                else:
                    location = os.path.join(self.args.outFolder, artist_name, album_name, filename)
                if os.path.isfile(location):
                    print("Downloaded %s" % filename)
                else :
                    print("Downloading %s" % filename)
                    obj = SmartDL(dec_url, location)
                    obj.start()
                    try:
                        name = songs_json['name'] if ('name' in songs_json) else songs_json['listname']
                    except:
                        name = ''
                    self.addtags(location, song, name)
                    print('\n')
            except Exception as e:
                logger.error('Download Error' + str(e))
    
    def addtags(self, filename, json_data, playlist_name):
        audio = MP4(filename)
        audio['\xa9nam'] = html.unescape(self.unicode(json_data['song']))
        audio['\xa9ART'] = html.unescape(self.unicode(json_data['primary_artists']))
        audio['\xa9alb'] = html.unescape(self.unicode(json_data['album']))
        audio['aART'] = html.unescape(self.unicode(json_data['singers']))
        audio['\xa9wrt'] = html.unescape(self.unicode(json_data['music']))
        audio['desc'] = html.unescape(self.unicode(json_data['starring']))
        audio['\xa9gen'] = html.unescape(self.unicode(playlist_name))
        # audio['cprt'] = track['copyright'].encode('utf-8')
        # audio['disk'] = [(1, 1)]
        # audio['trkn'] = [(int(track['track']), int(track['maxtracks']))]
        audio['\xa9day'] = html.unescape(self.unicode(json_data['year']))
        audio['cprt'] = html.unescape(self.unicode(json_data['label']))
        # if track['explicit']:
        #    audio['rtng'] = [(str(4))]
        cover_url = json_data['image'][:-11] + '500x500.jpg'
        fd = urllib.request.urlopen(cover_url)
        cover = MP4Cover(fd.read(), getattr(MP4Cover, 'FORMAT_PNG' if cover_url.endswith('png') else 'FORMAT_JPEG'))
        fd.close()
        audio['covr'] = [cover]
        audio.save()