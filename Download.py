import ast
import base64
import html
import json
import os
import re
import urllib.request
import sys
import argparse

import logger
import requests
import urllib3.request
from bs4 import BeautifulSoup
from mutagen.mp4 import MP4, MP4Cover
from pySmartDL import SmartDL
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from pyDes import *

from aiohttp import ClientSession
import asyncio

# Pre Configurations
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
unicode = str
raw_input = input


def argManager():
    parser = argparse.ArgumentParser()
    parser.add_argument("-artist", "--artist", action="store_true", help="Download for an Artist")
    parser.add_argument("-song", "--song", action="store_true", help="Download Songs")
    parser.add_argument("-album", "--album", action="store_true", help="Download Albums")
    parser.add_argument("-user", "--user", action="store_true", help="Signin as JioSaavn user")
    parser.add_argument("-p", "--p", action="store_true", help="Download Playlists by signing in")
    parser.add_argument("-a", "--a", action="store_true", help="Download Albums by signing in")
    parser.add_argument("-s", "--s", action="store_true", help="Download Shows by signing in")
    parser.add_argument("-fast", "--fast", action="store_true", help="Get details asynchronously")
    args = parser.parse_args()
    return args


# Start of functions related to Asynchronously getting all album IDs of an artist 
async def fetch(url, session):
    async with session.get(url) as response:
        html_text = await response.text()
        return html_text


async def run(artistId, total_requests):
    url = 'https://www.saavn.com/api.php?_marker=0&_format=json&__call=artist.getArtistPageDetails&artistId={0}&n_album=10&page={1}'
    tasks = []
    async with ClientSession(headers=headers) as session:
        for n_album_page in range(total_requests):
            task = asyncio.ensure_future(fetch(url.format(artistId, n_album_page), session))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        # processArtistAlbumsID(responses)
        return responses


def main(artistId, total_requests):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(artistId, total_requests))
    # loop.run_until_complete(future)
    return  loop.run_until_complete(future)


def getArtistAlbumsIDsFast(artistId, artist_json):
    album_IDs_artist = []
    try:
        artist_name = artist_json['name']
        total_albums = artist_json['topAlbums']['total']
        print('Total Albums of the Artist: {0}'.format(total_albums))
        if total_albums % 10 != 0:
            total_requests = (total_albums // 10) + 1
        else:
            total_requests = total_albums // 10
        print('Total requests: {}'.format(total_requests))
        responses = main(artistId, total_requests)
        for response in responses:
            artist_json = [x for x in response.splitlines() if x.strip().startswith('{')][0]
            artist_json = json.loads(artist_json)
            n_albums_in_page = len(artist_json['topAlbums']['albums'])
            for i in range(n_albums_in_page):
                albumId = artist_json['topAlbums']['albums'][i]['albumid']
                album_IDs_artist.append(albumId)
    except Exception as e:
        print(str(e))
        print('No albums found for the artist')
        print('You can try without --fast parameter')
        exit()
    print('Total Number of Albums found: {0}'.format(len(album_IDs_artist)))
    return (album_IDs_artist, artist_name)
# End of functions relating to asynchronous call


def getLibrary():
    url = "https://www.jiosaavn.com/api.php?__call=user.login&_marker=0"
    username = input("Enter your email for jiosaavn: ").strip()
    password = input("Enter your password for jiosaavn: ").strip()
    payload = { "username": username, "password": password }
    session = requests.Session()
    session.post(url, data=payload)
    response = session.get("https://www.jiosaavn.com/api.php?_format=json&__call=library.getAll")
    # library_json has ['song', 'show', 'artist', 'album', 'playlist', 'user'] as keys all of which have the id's as their value
    library_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
    library_json = json.loads(library_json)
    return library_json


def addtags(filename, json_data, playlist_name):
    audio = MP4(filename)
    audio['\xa9nam'] = html.unescape(unicode(json_data['song']))
    audio['\xa9ART'] = html.unescape(unicode(json_data['primary_artists']))
    audio['\xa9alb'] = html.unescape(unicode(json_data['album']))
    audio['aART'] = html.unescape(unicode(json_data['singers']))
    audio['\xa9wrt'] = html.unescape(unicode(json_data['music']))
    audio['desc'] = html.unescape(unicode(json_data['starring']))
    audio['\xa9gen'] = html.unescape(unicode(playlist_name))
    # audio['cprt'] = track['copyright'].encode('utf-8')
    # audio['disk'] = [(1, 1)]
    # audio['trkn'] = [(int(track['track']), int(track['maxtracks']))]
    audio['\xa9day'] = html.unescape(unicode(json_data['year']))
    audio['cprt'] = html.unescape(unicode(json_data['label']))
    # if track['explicit']:
    #    audio['rtng'] = [(str(4))]
    cover_url = json_data['image'][:-11] + '500x500.jpg'
    fd = urllib.request.urlopen(cover_url)
    cover = MP4Cover(fd.read(), getattr(MP4Cover, 'FORMAT_PNG' if cover_url.endswith('png') else 'FORMAT_JPEG'))
    fd.close()
    audio['covr'] = [cover]
    audio.save()


def setProxy():
    proxy_ip = ''
    if ('http_proxy' in os.environ):
        proxy_ip = os.environ['http_proxy']
    proxies = {
        'http': proxy_ip,
        'https': proxy_ip,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
    }
    return proxies, headers


def setDecipher():
    return des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)


def searchSongs(query):
    songs_json = []
    albums_json = []
    playLists_json = []
    topQuery_json = []
    response = requests.get(
        'https://www.jiosaavn.com/api.php?_format=json&query={0}&__call=autocomplete.get'.format(query))
    if response.status_code == 200:
        response_json = json.loads(response.text.splitlines()[6])
        albums_json = response_json['albums']['data']
        songs_json = response_json['songs']['data']
        playLists_json = response_json['playlists']['data']
        topQuery_json = response_json['topquery']['data']
    return {"albums_json": albums_json,
            "songs_json": songs_json,
            "playLists_json": playLists_json,
            "topQuery_json": topQuery_json}


def getPlayList(listId):
    songs_json = []
    response = requests.get(
        'https://www.jiosaavn.com/api.php?listid={0}&_format=json&__call=playlist.getDetails'.format(listId), verify=False)
    if response.status_code == 200:
        songs_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
        songs_json = json.loads(songs_json)
    return songs_json


def getAlbum(albumId):
   songs_json = []
   response = requests.get(
       'https://www.jiosaavn.com/api.php?_format=json&__call=content.getAlbumDetails&albumid={0}'.format(albumId),
       verify=False)
   if response.status_code == 200:
       songs_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
       songs_json = json.loads(songs_json)
       print("Album name: ",songs_json["name"])
       album_name=songs_json["name"]
   return songs_json, album_name


def getArtistAlbumsIDs(artistId, artist_json):
    album_IDs_artist = []
    try:
        artist_name = artist_json['name']
        total_albums = artist_json['topAlbums']['total']
        print('Total Albums of the Artist: {0}'.format(total_albums))
        if total_albums % 10 != 0:
            total_requests = (total_albums // 10) + 1
        else:
            total_requests = total_albums // 10
        print('Total requests: {}'.format(total_requests))
        for n_album_page in range(total_requests):
            print('Getting Album page: {0}'.format(n_album_page))
            url = 'https://www.saavn.com/api.php?_marker=0&_format=json&__call=artist.getArtistPageDetails&artistId={0}&n_album=10&page={1}'.format(artistId, n_album_page)
            response = requests.get(url)
            artist_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
            artist_json = json.loads(artist_json)
            n_albums_in_page = len(artist_json['topAlbums']['albums'])
            for i in range(n_albums_in_page):
                albumId = artist_json['topAlbums']['albums'][i]['albumid']
                album_IDs_artist.append(albumId)
    except Exception as e:
        print(str(e))
        print('No albums found for the artist')
        exit()
    print('Total Number of Albums found: {0}'.format(len(album_IDs_artist)))
    return (album_IDs_artist, artist_name)


def getShow(showId):
    show_homepage_json = []
    show_json = {}
    response = requests.get(
                'https://www.jiosaavn.com/api.php?_format=json&show_id={}&__call=show.getHomePage'.format(showId))
    show_homepage_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
    show_homepage_json = json.loads(show_homepage_json)
    no_of_seasons = len(show_homepage_json['seasons'])
    for season in range(no_of_seasons):   # Note that season value starts from 0 for the program but from 1 for the url
        no_of_episodes = show_homepage_json['seasons'][season]['more_info']['numEpisodes']
        response = requests.get(
            'https://www.jiosaavn.com/api.php?season_number={}&show_id={}&n={}&_format=json&__call=show.getAllEpisodes&sort_order=asc'.format(season+1, showId, no_of_episodes))
        season_json = [x for x in response.text.splitlines() if x.strip().startswith('[')][0]
        season_json = json.loads(season_json)  # A list containing all the episodes in the season
        show_json[season] = season_json   # To build a dictionary containg all the season in the show
    return show_json


# This function doesn't work yet
def addtagsShow(filename, json_data):
    audio = MP4(filename)
    audio['\xa9nam'] = html.unescape(unicode(json_data['title']))
    try:
        audio['\xa9ART'] = ""
        for artist in json_data['more_info']['artistMap']['primary_artists']:
            audio['\xa9ART'] = audio['\xa9ART'] + ', ' + html.unescape(unicode(artist['name']))
    except:
        pass
    audio['\xa9alb'] = html.unescape(unicode(json_data['more_info']['show_title']))
    # audio['\xa9gen'] = html.unescape(unicode(playlist_name))
    audio['\xa9day'] = html.unescape(unicode(json_data['year']))
    audio['cprt'] = html.unescape(unicode(json_data['more_info']['label']))

    cover_url = json_data['image'][:-11] + '500x500.jpg'
    fd = urllib.request.urlopen(cover_url)
    cover = MP4Cover(fd.read(), getattr(MP4Cover, 'FORMAT_PNG' if cover_url.endswith('png') else 'FORMAT_JPEG'))
    fd.close()
    audio['covr'] = [cover]
    audio.save()


def downloadShow(show_json):
    show_name = show_json.get(0)[0]['more_info']['show_title']
    print("Show Name: {}".format(show_name))
    for season, season_json in show_json.items():
        season_name = 'Season {}'.format(season+1)
        print("Season: {}".format(season_name))
        des_cipher = setDecipher()
        for episode in season_json:
            try:
                enc_url = base64.b64decode(episode['more_info']['encrypted_media_url'].strip())
                dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
                # dec_url = dec_url.replace('_96.mp4', '_320.mp4')   # Change in url gives invalid xml
                filename = html.unescape(episode['title']) + '.m4a'
                filename = filename.replace("\"", "'")
                filename = filename.replace(":", "-")
                filename = filename.replace("<", "-")
                filename = filename.replace(">", "-")
                filename = filename.replace("?", "-")
                filename = filename.replace("*", "-")
                filename = filename.replace("|", "-")
            except Exception as e:
                logger.error('Download Error' + str(e))
            try:
                location = os.path.join(os.path.sep, os.getcwd(), show_name, season_name, filename)
                if os.path.isfile(location):
                   print("Downloaded Show: {} - Season: {} - Episode: {}".format(show_name, season_name, filename))
                else :
                    print("Downloading Episode: {}".format(filename))
                    obj = SmartDL(dec_url, location)
                    obj.start()
                    # TODO: addtags will not work for shows
                    # addtagsShow(filename, episode)
                    # name = songs_json['name'] if ('name' in songs_json) else songs_json['listname']
                    # addtags(location, song, name)
                    print('\n')
            except Exception as e:
                 logger.error('Download Error' + str(e))


def downloadAllPlayList(library_json):
    playListIDs = library_json.get('playlist')
    if playListIDs is not None:
        print("Playlists found: {}".format(len(playListIDs)))
        for playList in playListIDs:
            playListID = playList['id']
            downloadSongs(getPlayList(playListID))


def downloadAllAlbums(library_json):
    albumIDs = library_json.get('album')
    if albumIDs is not None:
        print("Albums found: {}".format(len(albumIDs)))
        for albumId in albumIDs:
            try:
                downloadAlbum(albumId)
            except:
                print('Error getting album with ID: {}'.format(albumId))


def downloadArtistAllAlbums(album_IDs_artist, artist_name):
    if album_IDs_artist:
        for albumId in album_IDs_artist:
            try:
                downloadAlbum(albumId, artist_name)
            except:
                print('Error getting album with ID: {}'.format(albumId))


def downloadArtistAllSongs(artistId, artist_json):
    try:
        artist_name = artist_json['name']
        total_songs = artist_json['topSongs']['total']
        print('Total Songs of the Artist: {0}'.format(total_songs))
        if total_songs % 10 != 0:
            total_requests = (total_songs // 10) + 1
        else:
            total_requests = total_songs // 10
        print('Total requests: {}'.format(total_requests))
        for n_song_page in range(total_requests):
            print('Getting Song page: {0}'.format(n_song_page))
            url = 'https://www.saavn.com/api.php?_marker=0&_format=json&__call=artist.getArtistPageDetails&artistId={0}&n_song=10&page={1}'.format(artistId, n_song_page)
            response = requests.get(url)
            artist_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
            artist_json = json.loads(artist_json)
            songs_json = artist_json['topSongs']   # A dict with key songs having at most 10 songs
            downloadSongs(songs_json, artist_name=artist_name)
    except Exception as e:
        print(str(e))
        print('No songs found for the artist')


def dowloadAllShows(library_json):
    if library_json.get('show') is not None:
        for showId in library_json['show']:
            # TODO download the show
            downloadShow(getShow(showId))


def getSong(songId):
    songs_json = []
    response = requests.get(
        'http://www.jiosaavn.com/api.php?songid={0}&_format=json&__call=song.getDetails'.format(songId), verify=False)
    if response.status_code == 200:
        print(response.text)
        songs_json = json.loads(response.text.splitlines()[5])
    return songs_json


def getHomePage():
    playlists_json = []
    response = requests.get(
        'https://www.jiosaavn.com/api.php?__call=playlist.getFeaturedPlaylists&_marker=false&language=tamil&offset=1&size=250&_format=json',
        verify=False)
    if response.status_code == 200:
        playlists_json = json.loads(response.text.splitlines()[2])
        playlists_json = playlists_json['featuredPlaylists']
    return playlists_json


def downloadAlbum(albumId, artist_name=''):
    print("Initiating Album Downloading")
    json_data, album_nm=getAlbum(albumId)
    album_name = album_nm.replace("&quot;", "'")
    if artist_name:
        downloadSongs(json_data, album_name, artist_name=artist_name)
    else:
        downloadSongs(json_data, album_name)


def downloadSongs(songs_json, album_name='songs', artist_name='Non-Artist'):
    des_cipher = setDecipher()
    for song in songs_json['songs']:
        try:
            enc_url = base64.b64decode(song['encrypted_media_url'].strip())
            dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
            dec_url = dec_url.replace('_96.mp4', '_320.mp4')
            filename = html.unescape(song['song']) + '.m4a'
            filename = filename.replace("\"", "'")
            filename = filename.replace(":", "-") 
            filename = filename.replace("<", "-") 
            filename = filename.replace(">", "-") 
            filename = filename.replace("?", "-") 
            filename = filename.replace("*", "-") 
            filename = filename.replace("|", "-")
        except Exception as e:
            logger.error('Download Error' + str(e))
        try:
            location = os.path.join(os.path.sep, os.getcwd(), artist_name, album_name, filename)
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
                addtags(location, song, name)
                print('\n')
        except Exception as e:
             logger.error('Download Error' + str(e))


if __name__ == '__main__':
    args = argManager()
    album_name="songs"

    if args.user:
        if args.p:
            downloadAllPlayList(getLibrary())
        elif args.a:
            downloadAllAlbums(getLibrary())
        elif args.s:
            dowloadAllShows(getLibrary())
    elif args.artist:
        try:
            user_in_url = input('Enter the artist URL: ')
            proxies, headers = setProxy()
            response = requests.get(user_in_url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            artistId = soup.select('.actions.clr')[0].find('a')['data-id']   # Gets Artist ID from follow button

            url = 'https://www.jiosaavn.com/api.php?_marker=0&_format=json&__call=artist.getArtistPageDetails&artistId={0}'.format(artistId)
            response = requests.get(url)
            artist_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
            artist_json = json.loads(artist_json)
        except Exception as e:
            print(str(e))
            print('Please check that the entered URL links to an Artist')
            exit()
        if args.album:
            print('Downloading all artist albums')
            if args.fast:
                album_IDs_artist, artist_name = getArtistAlbumsIDsFast(artistId, artist_json)
                downloadArtistAllAlbums(album_IDs_artist, artist_name)
            else:
                album_IDs_artist, artist_name = getArtistAlbumsIDs(artistId, artist_json)
                downloadArtistAllAlbums(album_IDs_artist, artist_name)
        elif args.song:
            print('Downloading all artist songs')
            downloadArtistAllSongs(artistId, artist_json)
    else:
        input_url = input('Enter the url: ').strip()
        try:
            proxies, headers = setProxy()
            res = requests.get(input_url, proxies=proxies, headers=headers)
        except Exception as e:
            logger.error('Error accessing website error: ' + e)

        soup = BeautifulSoup(res.text, "lxml")

        try:
            getPlayListID = soup.select(".flip-layout")[0]["data-listid"]
            if getPlayListID is not None:
                print("Initiating PlayList Downloading")
                downloadSongs(getPlayList(getPlayListID))
                sys.exit()
        except Exception as e:
            print('...')
        try:
            getAlbumID = soup.select(".play")[0]["onclick"]
            getAlbumID = ast.literal_eval(re.search("\[(.*?)\]", getAlbumID).group())[1]
            if getAlbumID is not None:
                downloadAlbum(getAlbumID)
                
        except Exception as e:
            print('...')
            print("Please paste link of album or playlist")

# getSongID = soup.select(".current-song")[0]["data-songid"]
# if getSongID is not None:
#    print(getPlayListID)
#    sys.exit()
# for playlist in getHomePage():
#     print(playlist)
#     id = raw_input()
#     if id is "1":
#       downloadSongs(getPlayList(playlist['listid']))
# queryresults = searchSongs('nannare')
# print(json.dumps(getSong(queryresults['topQuery_json'][0]['id']), indent=2))
# response = requests.head(dec_url)
# if os.path.isfile(location) if (os.stat(location).st_size >  int(response.headers["Content-Length"])) else False: