'''
Functions in this module are basically helpers to work with dropbox
'''
import json
import os
from subprocess import getoutput
import sys
import dropbox

def read_token():
    '''Read token from settings needed for dropbox client
    '''
    username = getoutput('whoami')

    if os.path.exists('/home/{}/.le-chiffre/settings.json'.format(username)):
        data = json.load(open('/home/{}/.le-chiffre/settings.json'.format(username)))

        if 'token' in data:
            return data['token']
            
        else:
            print('le-chiffre: Please setup token, use `set token YOUR_TOKEN`!')
            sys.exit(0)
            return None

    return None

def get_key():
    '''Try to download `key` file from cloud
    '''
    client = dropbox.Dropbox(read_token())

    try:
        md, res = client.files_download('/le-chiffre/key')
    except dropbox.exceptions.HttpError:
        print('le-chiffre: Some HTTP error occured | tried to get key from Dropbox!')
        return None
    
    return json.loads(res.content.decode('utf-8'))['key']

def upload_key(key):
    '''Upload AES key to cloud
    '''
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
