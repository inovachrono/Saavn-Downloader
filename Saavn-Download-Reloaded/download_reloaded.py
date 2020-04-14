from bs4 import BeautifulSoup
import requests
import logger
import sys

from helper import argManager, setProxy, scan_url
from playlist import Playlist
from album import Album
from artist import Artist
from saavnaccount import Account

class Download():
    def __init__(self):
        pass

    def run(self):
        args = argManager()
        album_name="songs"
        proxies, headers = setProxy()

        # Manage for jio saavn users
        if args.user:
            if args.email and args.password:
                email = args.email
                password = args.password
            else:
                email = input('Enter your email for jiosaavn: ').strip()
                password = input("Enter your password for jiosaavn: ").strip()
            account = Account(proxies=proxies, headers=headers, email=email, password=password)
            if args.p:
                account.start_download_playlist()
            elif args.a:
                account.start_download_album()
            elif args.clone:
                account.get_details_n_clone(args.clone, args.create, args.copy)
            elif args.create:
                account.create_user(email, password)
        
        # Manage for all default downloads
        # Note: Passing the url parameter to the contructor of Playlist, Album and Artist is must
        else:
            if args.url is None:
                dl_url = input("Enter the URL : ").strip()
            else:
                dl_url = args.url
            
            dl_type = scan_url(url=dl_url)
            if dl_type == 'playlist':      
                playlist = Playlist(proxies, headers, dl_url)
                playlist.start_download()
            elif dl_type == 'album':
                album = Album(proxies, headers, dl_url)
                album.start_download()
            elif dl_type == 'artist':
                artist = Artist(proxies, headers, args, dl_url)
                artist.start_download()
        print('DONE\n')


if __name__ == '__main__':
    obj = Download()
    obj.run()