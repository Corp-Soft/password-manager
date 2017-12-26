import dropbox, json, os, sys
from passwords import get_username

def read_token():
    username = get_username()

    if os.path.exists('/home/{}/.le-chiffre/settings.json'.format(username)):
        data = json.load(open('/home/{}/.le-chiffre/settings.json'.format(username)))

        if 'token' in data:
            return data['token']
            
        else:
            print('le-chiffre: Please setup token, use `set token YOUR_TOKEN`!')

def get_key():
    client = dropbox.Dropbox(read_token())

    try:
        md, res = client.files_download('/le-chiffre/key')
    except dropbox.exceptions.HttpError:
        print('le-chiffre: Some HTTP error occured | tried to get key from Dropbox!')
        return None
    
    return json.loads(res.content.decode('utf-8'))['key']

def upload_key(key):
    client = dropbox.Dropbox(read_token())

    key = json.dumps(dict(
        key=key
    )).encode()

    try:
        client.files_upload(key, '/le-chiffre/key')
    except dropbox.exceptions.HttpError:
        print('le-chiffre: Some HTTP error occured | tried to upload hash to Dropbox!')
        return False

    return True
