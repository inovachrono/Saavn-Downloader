import requests
import json

headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9.1; Samsung S10 Build/LMY47O)',
            'Host': 'www.saavn.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

def createAccount(email, password):
    headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9.1; Samsung S10 Build/LMY47O)',
            'Host': 'www.saavn.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    payload = {
            'password': password,
            '_marker': '0',
            'cc': '',
            'ctx': 'android',
            'network_operator': '',
            'email': email,
            'state': 'logout',
            'v': '224',
            'app_version': '6.8.2',
            'build': 'Pro',
            'api_version': '4',
            'network_type': 'WIFI',
            'username': email,
            '_format': 'json',
            '__call': 'user.createV2',
            'manufacturer': 'Samsung',
            'readable_version': '6.8.2',
            'network_subtype': '',
            'model': 'Samsung Galaxy S10'
    }

    url = 'https://www.saavn.com/api.php'

    session = requests.Session()
    response = session.post(url, headers=headers, data=payload)
    data = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
    data = json.loads(data)
    # print(data)
    if data.get('error'):
        return False
    elif data.get('data').get('uid'):
        return True
    else:
        return False

def activateLibrary(email, password):
    # Function to Emualate android signin and activate library

    payload = {
            'password': password,
            '_marker': '0',
            'cc': '',
            'ctx': 'android',
            'network_operator': '',
            'email': email,
            'state': 'logout',
            'v': '224',
            'app_version': '6.8.2',
            'build': 'Pro',
            'api_version': '4',
            'network_type': 'WIFI',
            'username': email,
            '_format': 'json',
            '__call': 'user.login',
            'manufacturer': 'Samsung',
            'readable_version': '6.8.2',
            'network_subtype': '',
            'model': 'Samsung Galaxy S10'
    }
    url = 'https://www.saavn.com/api.php'

    session = requests.Session()
    response = session.post(url, headers=headers, data=payload)
    data = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
    data = json.loads(data)
    # print(data)
    if data.get('error'):
        return False
    elif data.get('data').get('uid'):
        try:
            response = session.get("https://www.saavn.com/api.php?_marker=0&cc=&ctx=android&state=login&v=224&app_version=6.8.2&api_version=4&_format=json&__call=library.getAll")
            library_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
            library_json = json.loads(library_json)
            # print(library_json)
            logout(session, url, headers)
            return True
        except Exception as e:
            print(str(e))
            return False
    else:
        return False

def getLibrarySession(email, password):
    # Function to Emualate android signin and activate library and return library_json and session instance

    payload = {
            'password': password,
            '_marker': '0',
            'cc': '',
            'ctx': 'android',
            'network_operator': '',
            'email': email,
            'state': 'logout',
            'v': '224',
            'app_version': '6.8.2',
            'build': 'Pro',
            'api_version': '4',
            'network_type': 'WIFI',
            'username': email,
            '_format': 'json',
            '__call': 'user.login',
            'manufacturer': 'Samsung',
            'readable_version': '6.8.2',
            'network_subtype': '',
            'model': 'Samsung Galaxy S10'
    }

    url = 'https://www.saavn.com/api.php'

    session = requests.Session()
    response = session.post(url, headers=headers, data=payload)
    data = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
    data = json.loads(data)
    # print(data)
    if data.get('error'):
        return False
    elif data.get('data').get('uid'):
        try:
            response = session.get("https://www.saavn.com/api.php?_marker=0&cc=&ctx=android&state=login&v=224&app_version=6.8.2&api_version=4&_format=json&__call=library.getAll", headers=headers)
            library_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
            library_json = json.loads(library_json)
            # print(library_json)
            return (library_json, session)
        except Exception as e:
            print(str(e))
            return False
    else:
        return False

def logout(session, url, headers):
    payload = {
            '_marker': '0',
            'cc': '',
            'ctx': 'android',
            'network_operator': '',
            'state': 'logout',
            'v': '224',
            'app_version': '6.8.2',
            'build': 'Pro',
            'api_version': '4',
            'network_type': 'WIFI',
            '_format': 'json',
            '__call': 'user.logout',
            'manufacturer': 'Samsung',
            'readable_version': '6.8.2',
            'network_subtype': '',
            'model': 'Samsung Galaxy S10'
    }

    response = session.post(url, headers=headers, data=payload)
    print(response.text)

def cloneAccount(oEmail, oPassword, nEmail, nPassword, createNewAcc):
    #Function to clone songs, albums and playlists to another account
    if createNewAcc:
        up_success = createAccount(nEmail, nPassword)
    else:
        up_success = True
    if up_success:
        n_account = getLibrarySession(nEmail, nPassword)
        o_account = getLibrarySession(oEmail, oPassword)
    else:
        print('Account creation failed !!!')
        return False
    if n_account and o_account:
        olibrary_json = o_account[0]
        o_session = o_account[1]
        nlibrary_json = n_account[0]
        n_session = n_account[1]

        np_data = {}
        np = nlibrary_json.get('playlist')
        for playlist in np:
            songs_json = []
            response = requests.get(
                'https://www.jiosaavn.com/api.php?listid={0}&_format=json&__call=playlist.getDetails'.format(playlist['id']))
            if response.status_code == 200:
                songs_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
                songs_json = json.loads(songs_json)
            np_data[songs_json['listname']] = playlist['id']

        url = "https://www.jiosaavn.com/api.php?__call=user.login&_marker=0"
        payload = { "username": nEmail, "password": nPassword }
        session = requests.Session()
        session.post(url, data=payload)   #Getting browser session for easy song and album addition

        print('Adding songs to new account')
        songs = olibrary_json.get('song')
        for song in songs:
            session.get('https://www.saavn.com/api.php?_marker=0&entity_type=song&entity_ids={0}&_format=json&__call=library.add'.format(song))
        print('Adding adding albums to new account')
        albums = olibrary_json.get('album')
        for album in albums:
            session.get('https://www.saavn.com/api.php?_marker=0&entity_type=album&entity_ids={0}&_format=json&__call=library.add'.format(album))
        print('Adding playlists to new account')
        playlists = olibrary_json.get('playlist')
        for playlist in playlists:
            songs_json = []
            response = requests.get(
                'https://www.jiosaavn.com/api.php?listid={0}&_format=json&__call=playlist.getDetails'.format(playlist['id']))
            if response.status_code == 200:
                songs_json = [x for x in response.text.splitlines() if x.strip().startswith('{')][0]
                songs_json = json.loads(songs_json)
            else:
                print('Unable to get playlist details from original')

            p_copy = {
                '_marker': '0',
                'ctx': 'android',
                'network_operator': '',
                'state': 'login',
                'v': '224',
                'app_version': '6.8.2',
                'build': 'Pro',
                'api_version': '4',
                'network_type': 'WIFI',
                '_format': 'json',
                '__call': 'playlist.copyPlaylist',
                'destListName': songs_json['listname'],
                'srcListId': playlist['id'],
                'manufacturer': 'Samsung',
                'readable_version': '6.8.2',
                'network_subtype': '',
                'model': 'Samsung Galaxy S10'
            }
            res = n_session.post('https://www.jiosaavn.com/api.php', headers=headers, data=p_copy)
            print(res.text.strip().replace('\n', ''))
        print('Logging out of both accounts')
        logout(o_session, 'https://www.saavn.com/api.php', headers)
        logout(n_session, 'https://www.saavn.com/api.php', headers)
        return True
    else:
        return False

def getDetailsNClone(clone, create, copy):
    if clone:
        if not create and not copy:
            print('Invalid parameters entered !!!')
            return
        oEmail = input('Enter original account email(FROM): ')
        oPassword = input('Enter original account password(FROM): ')
        if create:
            nEmail = input('Enter the email for new account(TO): ')
            nPassword = input('Enter the password for new account(TO): ')
            success = cloneAccount(oEmail, oPassword, nEmail, nPassword, True)
        elif copy:
            nEmail = input('Enter the email of copy account(TO): ')
            nPassword = input('Enter the password of copy account(TO): ')
            success = cloneAccount(oEmail, oPassword, nEmail, nPassword, False)

        if success:
            print('The email for clone is: {0}'.format(nEmail))
            print('The password for clone is: {0}'.format(nPassword))
        else:
            print('Error: Failed to clone account')