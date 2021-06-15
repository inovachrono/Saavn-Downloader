![Python application](https://github.com/monuyadav016/Saavn-Downloader/workflows/Python%20application/badge.svg)

# Saavn Downloader
The fullset of functionality offered are:
  - High Qualtiy - M4A (320 Kbps bitrate)
  - Songs with metadata
  - Download Individual Song
  - Download PlayList
  - Download Album
  - Download all Albums of an Artist as Albums
  - Download all Songs of an Artist as Songs
  - Download Entire PlayList from user profile
  - Download Entire Albums from user profile
  - Download Entire JioSaavn Originals and Podcasts in the user profile
  - Clone an account to a new account (Created via script)
  - Clone an account to another account
  - Create a new account
 

### Installation
```sh
$ pip3 install -r requirements.txt
```

### Usage

> ## ***Google colab link to execute all the script actions:*** [Colab Notebok](https://colab.research.google.com/drive/1xQ5GQLWkEnfK189jT41WzQ2d0YS4sVJx?usp=sharing)


#### Download Song, Playlist, Album from Web URL
```sh
$ python3 download_reloaded.py
$ Paste the URL: https://www.jiosaavn.com/album/tum-hi-aana-from-marjaavaan/j9bfphC2728_
```

#### You can also specify the url in the with -u or --url argument directly
```sh
$ python3 download_reloaded.py -u https://www.jiosaavn.com/album/tum-hi-aana-from-marjaavaan/j9bfphC2728_
```

#### If you have more than 1 url and no time to wait use the -f or --file argument to specify the absolute path to txt file with urls pasted line by line
```sh
$ python3 download_reloaded.py -f /home/monu/Desktop/urls.txt
```

#### Choose output folder path with the -o or --outFolder argument (The output path must be absolute path and not relative)
```
$ python3 download_reloaded.py -o /home/monu/Desktop/
```


### NOTE: If at any point there is an Error or the Download fails you can Retry the same command

#### Download All Albums of an Artist
```sh
$ python download_reloaded.py -album
$ Paste the URL of Artist Profile: https://www.jiosaavn.com/artist/babbal-rai-albums/pRd5ZTGrLv8_
``` 
*\*If none of the flag such as --album, --song is specified for the artist then by default the Artist music will be downloaded in Album folder structure i.e. there will be as many album folders as the number of albums an artist has on jiosaavn and not a single songs folder that you get when --song flag is specified.  


#### Download All Songs of an Artist
```sh
$ python download_reloaded.py -song
$ Paste the URL of Artist Profile: https://www.jiosaavn.com/artist/babbal-rai-albums/pRd5ZTGrLv8_
```


### Note: Before using below commands as JioSaavn user make sure you have signed into the JioSaavn Android or iOS app at least once.

#### Download All Playlist from your profile
```sh
$ python3 download_reloaded.py -user -p
$ Enter your Email: your_saavn_email
$ Enter your Password: your_saavn_password
```

#### You can also specify the username and password in the arguments using -e or --email, -pw or --password
```sh
$ python3 download_reloaded.py -user -e YOUR_EMAIL -pw YOUR_PASSWORD -p
```

#### Download All Albums from your profile
```sh
$ python3 download_reloaded.py -user -a
$ Enter your Email: your_saavn_email
$ Enter your Password: your_saavn_password
```

#### Clone songs, albums and playlists to a new account(account created by script itself)
```sh
$ python3 download_reloaded.py -user -clone -create
$ Enter original account email(FROM): from_account_email
$ Enter original account password(FROM): from_account_password
$ Enter the email for new account(TO): new_account_email
$ Enter the password for new account(TO): new_account_password
```

#### Clone songs, albums and playlists to another account(must alreay exist)
```sh
$ python3 download_reloaded.py -user -clone -copy
$ Enter original account email(FROM): from_account_email
$ Enter original account password(FROM): from_account_password
$ Enter the email of copy account(TO): to_account_email
$ Enter the password of copy account(TO): to_account_password
```

#### Create new account
```sh
$ python3 download_reloaded.py -user -create
$ Enter the email: email_you_want_to_use
$ Enter the password: password_you_want_to_use
```

### Changelog V2
  - Added download support for individual songs
  - Added command argument for input file with urls (-f, --file)
  - Added command argument for changing output directory (-o, --outFolder)
  - Added command argument for specifying jiosaavn username and password (-e, --email, -pw, --password)
  - Removed asynchronous code for artist data retrival


### Known Issues
  - Clone Functionality doesn't work with Saavn-Download-Reloaded package
  - Songs not having 320kbps don't get their meta data added
  - No Meta Data in JioSaavn Originals and Podcasts

### Development

Want to contribute? Great!


### Contributors
  - Arun ( Discovering Vulnerability in Saavn App )
  - [prabaprakash](https://github.com/prabaprakash/)
  - [monuyadav016](https://github.com/monuyadav016)


## License
This program is licensed under [MIT License](https://raw.githubusercontent.com/monuyadav016/Saavn-downloader/master/LICENSE)
