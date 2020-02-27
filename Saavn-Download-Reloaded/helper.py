from pyDes import *
import os
import argparse

def setProxy():
    proxy_ip = ''
    if ('http_proxy' in os.environ):
        proxy_ip = os.environ['http_proxy']
    proxies = {
        'http': proxy_ip,
        'https': proxy_ip,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'cache-control': 'private, max-age=0, no-cache'
    }
    return proxies, headers

def setDecipher():
    return des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)

def formatFilename(filename):
    filename = filename.replace("\"", "'")
    filename = filename.replace(":", "-")
    filename = filename.replace('"', "-")
    filename = filename.replace('/', "-")
    filename = filename.replace("<", "-")
    filename = filename.replace(">", "-")
    filename = filename.replace("?", "-")
    filename = filename.replace("*", "-")
    filename = filename.replace("|", "-")
    return filename

def argManager():
    parser = argparse.ArgumentParser()
    parser.add_argument("-artist", "--artist", action="store_true", help="Download for an Artist")
    parser.add_argument("-song", "--song", action="store_true", help="Download Songs")
    parser.add_argument("-album", "--album", action="store_true", help="Download Albums")
    parser.add_argument("-fast", "--fast", action="store_true", help="Get details asynchronously")

    parser.add_argument("-user", "--user", action="store_true", help="Signin as JioSaavn user")
    parser.add_argument("-p", "--p", action="store_true", help="Download Playlists by signing in")
    parser.add_argument("-a", "--a", action="store_true", help="Download Albums by signing in")
    parser.add_argument("-s", "--s", action="store_true", help="Download Shows by signing in")

    parser.add_argument("-clone", "--clone", action="store_true", help="Clone songs,albums,playlists to new account")
    parser.add_argument("-create", "--create", action="store_true", help="To create new account for cloning")
    parser.add_argument("-copy", "--copy", action="store_true", help="To copy to another account")
    args = parser.parse_args()
    return args