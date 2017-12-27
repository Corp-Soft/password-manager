'''
This module provides functions for managing all process
'''
import sys
import json
import string
import random
import os
from subprocess import getoutput
import api
from aes import aes

def get_username():
    '''Get username of Linux/Mac user using `whoami` command
    '''
    return getoutput('whoami')

def get_min_password_length():
    '''Read `min_password_length` property from json, otherwise default pass length is 10
    '''
    username = get_username()
    data = json.load(open('/home/{}/.le-chiffre/settings.json'.format(username)))
    return data['min_password_length']

def exit_if_no_default_dir(message):
    '''
    Exit process if any password is generated
    '''
    username = get_username()

    if not os.path.exists('/home/{}/.le-chiffre'.format(username)):
        print(message)
        sys.exit(0)

def make_default_dir_if_not_exists():
    '''Default directory for storing passwords is `/home/{username}/.le-chiffre`
    '''
    username = get_username()

    if not os.path.exists('/home/{}/.le-chiffre'.format(username)):
        os.makedirs('/home/{}/.le-chiffre'.format(username))

def get_aes_key():
    '''Get aes key based on storage type

    If storage is `local` - package will try to search for key in `key.enc` file

    If storage is `dropbox` - package will try to download key from cloud
    '''
    username = get_username()

    if os.path.exists('/home/{}/.le-chiffre'.format(username)):
        storage = get_storage_type()

        if storage == 'local':
            return open('/home/{}/.le-chiffre/key.enc'.format(username), 'r').read()

        elif storage == 'dropbox':
            data = json.load(open('/home/{}/.le-chiffre/settings.json'.format(username)))

            if 'token' in data:
                return api.get_key()

            else:
                print('le-chiffre: Please set token for dropbox!')
                return sys.exit(0)
    
    return sys.exit(0)

def copy_to_clipboard(password):
    '''Copy generated or found password to clipboard
    '''
    if sys.platform == 'linux' or sys.platform == 'linux2':
        os.system('echo {} | xclip -sel clip'.format(password))

    elif sys.platform == 'darwin':
        os.system('echo {} | tr -d "\n" | pbcopy'.format(password))

    print('le-chiffre: Copied password to clipboard!')

def get_storage_type():
    '''Get storage property from settings
    '''
    return json.load(open('/home/{}/.le-chiffre/settings.json'.format(get_username())))['storage']

def load_passwords():
    '''Load passwords if present from encoded file
    '''
    encrypted = open('/home/{}/.le-chiffre/passwords.enc'.format(get_username())).read()
    key = get_aes_key()
    return json.loads(aes(key).decrypt(encrypted))

def generate_password(url):
    '''
    Linux and Mac OS X basically have the same folders structure, we only need `/home/username` directory
    If storage is local - thus AES key is also stored locally
    '''
    username = get_username()

    make_default_dir_if_not_exists()

    if not os.path.exists('/home/{}/.le-chiffre/settings.json'.format(username)):
        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(username), 'w')
        settings_file.write(json.dumps(dict(
            storage='local',
            min_password_length=10
        )))
        settings_file.close()

    random_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(get_min_password_length()))

    if os.path.exists('/home/{}/.le-chiffre/passwords.enc'.format(username)):
        passwords = load_passwords()

        for i in passwords:
            if i['url'] == url:
                print('le-chiffre: Password for that url is already generated!')
                sys.exit(0)

        chiffre = dict(
            password=random_password,
            url=url
        )

        passwords.append(chiffre)
        passwords = aes(get_aes_key()).encrypt(json.dumps(passwords))

        passwords_file = open('/home/{}/.le-chiffre/passwords.enc'.format(username), 'w')
        passwords_file.write(passwords.decode('utf-8'))
        passwords_file.close()

        copy_to_clipboard(random_password)

    else:
        key = str(random.getrandbits(128))

        storage = get_storage_type()

        if storage == 'local':
            key_file = open('/home/{}/.le-chiffre/key.enc'.format(username), 'w')
            key_file.write(key)
            key_file.close()

        elif storage == 'dropbox':
            api.upload_key(key)

        passwords = list()

        chiffre = dict(
            password=random_password,
            url=url
        )

        passwords.append(chiffre)
        passwords = aes(key).encrypt(json.dumps(passwords))

        passwords_file = open('/home/{}/.le-chiffre/passwords.enc'.format(username), 'w')
        passwords_file.write(passwords.decode('utf-8'))
        passwords_file.close()

        copy_to_clipboard(random_password)

    print('le-chiffre: Generated password for {0} => {1}'.format(url, random_password))

def find_password(url):
    '''Tryna find password for given URL
    '''
    print('le-chiffre: You\'re searching password for url {}'.format(url))

    exit_if_no_default_dir('le-chiffre: You haven\'t generated any password yet to find anything!')

    passwords = load_passwords()

    searchable_password = None

    for i in passwords:
        if i['url'] == url:
            searchable_password = i['password']

    if searchable_password is not None:
        print('le-chiffre: I\'ve found {}'.format(searchable_password))
        copy_to_clipboard(searchable_password)

    else:
        print('le-chiffre: Sorry, I haven\'t found anything for that url!')

def list_passwords():
    '''List all available passwords
    '''
    print('le-chiffre: List all passwords!')

    exit_if_no_default_dir('le-chiffre: You haven\'t generated any password yet to list them!')

    passwords = load_passwords()

    if len(passwords) == 0:
        print('le-chiffre: Sorry you\'ve got zero passwords generated!')

    else:
        for i in passwords:
            password = i['password']
            url = i['url']
            print('le-chiffre: password => {0}, url => {1}'.format(password, url))

def remove_password(url):
    '''Remove password if present for given URL
    '''
    print('le-chiffre: You wanna delete password for url => {}'.format(url))
    username = get_username()

    exit_if_no_default_dir('le-chiffre: You haven\'t generated any password yet to remove any!')

    passwords = load_passwords()
    current_len = len(passwords)

    for i in range(len(passwords)):
        if passwords[i]['url'] == url:
            passwords.pop(i)

            passwords = aes(get_aes_key()).encrypt(json.dumps(passwords))

            passwords_file = open('/home/{}/.le-chiffre/passwords.enc'.format(username), 'w')
            passwords_file.write(passwords.decode('utf-8'))
            passwords_file.close()

            print('le-chiffre: Deleted password for url => {}'.format(url))

    if current_len == len(passwords):
        print('le-chiffre: Sorry, I haven\'t found anything for that url!')

def set_password_length(length):
    '''Setup min length of generated password
    '''
    if not os.path.exists('/home/{}/.le-chiffre/settings.json'.format(get_username())):
        make_default_dir_if_not_exists()

        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(get_username()), 'w')
        settings_file.write(json.dumps(dict(
            storage='local',
            min_password_length=length
        )))
        settings_file.close()

    else:
        data = json.load(open('/home/{}/.le-chiffre/settings.json'.format(get_username())))

        data['min_password_length'] = length
        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(get_username()), 'w')
        settings_file.write(json.dumps(data, sort_keys=True, indent=4))
        settings_file.close()

    print('le-chiffre: Established `min_password_length` to => {}'.format(length))

def set_storage_type(storage):
    '''Setup storage type like `local` either `dropbox`
    '''
    if not os.path.exists('/home/{}/.le-chiffre/settings.json'.format(get_username())):
        make_default_dir_if_not_exists()

        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(get_username()), 'w')
        settings_file.write(json.dumps(dict(
            storage=storage,
            min_password_length=10
        )))
        settings_file.close()

    else:
        data = json.load(open('/home/{}/.le-chiffre/settings.json'.format(get_username())))

        data['storage'] = storage
        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(get_username()), 'w')
        settings_file.write(json.dumps(data, sort_keys=True, indent=4))
        settings_file.close()

    print('le-chiffre: Established `storage` to => {}'.format(storage))

def set_token(token):
    '''Setup token if storage type is `dropbox`
    '''
    username = get_username()

    if not os.path.exists('/home/{}/.le-chiffre/settings.json'.format(username)):
        make_default_dir_if_not_exists()

        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(username), 'w')
        settings_file.write(json.dumps(dict(
            storage='dropbox',
            min_password_length=10,
            token=token
        )))
        settings_file.close()

    else:
        data = json.load(open('/home/{}/.le-chiffre/settings.json'.format(username)))

        data['token'] = token
        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(username), 'w')
        settings_file.write(json.dumps(data, sort_keys=True, indent=4))
        settings_file.close()

    if os.path.exists('/home/{}/.le-chiffre/key.enc'.format(username)):
        key = open('/home/{}/.le-chiffre/key.enc'.format(username), 'r').read()
        api.upload_key(key)

    else:
        key = str(random.getrandbits(128))
        api.upload_key(key)

    print('le-chiffre: Established `token` to => {}'.format(token))
