from bs4 import BeautifulSoup
import requests
import logger
import sys

from helper import argManager, setProxy
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
        
        # playlist = Playlist(proxies, headers)
        # playlist.start_download()

        # album = Album(proxies, headers)
        # album.start_download()

        # artist = Artist(proxies, headers, args)
        # artist.start_download()

        # email = input('Enter original account email(FROM): ')
        # password = input('Enter original account password(FROM): ')
        
        # account = Account(proxies=proxies, headers=headers, email=email, password=password)
        # print(account.getLibrarySession())
        # print(account.activateLibrary())
        # print(account.createAccount())
        # print(account.cloneAccount(nEmail='harry062@gmail.com', nPassword='Igot100%', createNewAcc=True))
        # print(account.cloneAccount(nEmail='harry049@gmail.com', nPassword='Igot100%', createNewAcc=False))
        # account.start_download_playlist()
        # account.start_download_album()
        # account.create_user()
        # account.get_details_n_clone(args.clone, args.create, args.copy)
        print()


if __name__ == '__main__':
    obj = Download()
    obj.run()