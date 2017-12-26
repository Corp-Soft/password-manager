import sys, subprocess, json, string, random, os, api
from aes import aes

# Get username of Linux/Mac user using `whoami` command
def get_username():
    return subprocess.getoutput('whoami')

# read `min_password_length` property from json, otherwise default pass length is 10
def get_min_password_length():
    return json.load(open('/home/{}/.le-chiffre/settings.json'.format(get_username())))['min_password_length']

def get_aes_key():
    username = get_username()

    if os.path.exists('/home/{}/.le-chiffre'.format(username)):
        storage = get_storage_type()

        if storage == 'local':
            return open('/home/{}/.le-chiffre/key.enc'.format(get_username()), 'r').read()

        elif storage == 'dropbox':
            return api.get_key()

def copy_to_clipboard(password):
    if sys.platform == 'linux' or sys.platform == 'linux2':
        os.system('echo {} | xclip -sel clip'.format(password))

    elif sys.platform == 'darwin':
        os.system('echo {} | tr -d "\n" | pbcopy'.format(password))

    elif sys.platform == 'win32' or sys.platform == 'win64':
        os.system('echo {} | clip'.format(password))

    print('le-chiffre: Copied password to clipboard!')

def get_storage_type():
    return json.load(open('/home/{}/.le-chiffre/settings.json'.format(get_username())))['storage']

def generate_password(url):
    # Linux and Mac OS X basically have the same folders structure, we only need `/home/username` directory
    if sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin':
        # If storage is local - thus AES key is also stored locally
        username = get_username()

        if not os.path.exists('/home/{}/.le-chiffre'.format(username)):
            os.makedirs('/home/{}/.le-chiffre'.format(username))

        if not os.path.exists('/home/{}/.le-chiffre/settings.json'.format(username)):
            settings = dict(
                storage='local',
                min_password_length=10
            )

            settings_file = open('/home/{}/.le-chiffre/settings.json'.format(username), 'w')
            settings_file.write(json.dumps(settings))
            settings_file.close()

        random_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(get_min_password_length()))

        # If user generates password not the first time
        if os.path.exists('/home/{}/.le-chiffre/passwords.enc'.format(username)):
            encrypted = open('/home/{}/.le-chiffre/passwords.enc'.format(username)).read()

            key = get_aes_key()
            passwords = json.loads(aes(key).decrypt(encrypted))

            for i in passwords:
                if i['url'] == url:
                    print('le-chiffre: Password for that url is already generated!')
                    sys.exit(0)

            chiffre = dict(
                password=random_password,
                url=url
            )

            passwords.append(chiffre)
            passwords = aes(key).encrypt(json.dumps(passwords))

            passwords_file = open('/home/{}/.le-chiffre/passwords.enc'.format(username), 'w')
            passwords_file.write(passwords.decode('utf-8'))
            passwords_file.close()

            print('le-chiffre: Generated password for {0} => {1}'.format(url, random_password))
            copy_to_clipboard(random_password)

        else:
            # This key is necessary in AES algorithm
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

            # First we stringify list with dict, then we encrypt this string
            passwords = aes(key).encrypt(json.dumps(passwords))

            # Write this encrypted string to file
            passwords_file = open('/home/{}/.le-chiffre/passwords.enc'.format(username), 'w')
            passwords_file.write(passwords.decode('utf-8'))
            passwords_file.close()

            print('le-chiffre: Generated password for {0} => {1}'.format(url, random_password))
            copy_to_clipboard(random_password)

    elif sys.platform == 'win32' or sys.platform == 'win64':
        pass

# Tryna find password for given URL
def find_password(url):
    if sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin':
        print('le-chiffre: You\'re searching password for url {}'.format(url))
        username = get_username()

        if not os.path.exists('/home/{}/.le-chiffre'.format(username)):
            print('le-chiffre: You haven\'t generated any password yet to find anything!')
            sys.exit(0)

        encrypted = open('/home/{}/.le-chiffre/passwords.enc'.format(username)).read()

        key = get_aes_key()
        passwords = json.loads(aes(key).decrypt(encrypted))

        searchable_password = None

        for i in passwords:
            if i['url'] == url:
                searchable_password = i['password']

        if searchable_password is not None and len(searchable_password) > 0:
            print('le-chiffre: I\'ve found {}'.format(searchable_password))
            copy_to_clipboard(searchable_password)
        else:
            print('le-chiffre: Sorry, I haven\'t found anything for that url!')


    elif sys.platform == 'win32' or sys.platform == 'win64':
        pass

# List all available passwords
def list_passwords():
    if sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin':
        username = get_username()

        if not os.path.exists('/home/{}/.le-chiffre'.format(username)):
            print('le-chiffre: You haven\'t generated any password yet to list them!')
            sys.exit(0)

        print('le-chiffre: List all passwords!')

        encrypted = open('/home/{}/.le-chiffre/passwords.enc'.format(username)).read()

        key = get_aes_key()
        passwords = json.loads(aes(key).decrypt(encrypted))

        if len(passwords) == 0:
            print('le-chiffre: Sorry you\'ve got zero passwords generated!')

        else:
            for i in passwords:
                password = i['password']
                url = i['url']
                print('le-chiffre: password => {0}, url => {1}'.format(password, url))

    elif sys.platform == 'win32' or sys.platform == 'win64':
        pass

# Remove password if present for given URL
def remove_password(url):
    if sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin':
        print('le-chiffre: You wanna delete password for url => {}'.format(url))
        username = get_username()

        if not os.path.exists('/home/{}/.le-chiffre'.format(username)):
            print('le-chiffre: You haven\'t generated any password yet to remove any!')
            sys.exit(0)

        encrypted = open('/home/{}/.le-chiffre/passwords.enc'.format(username)).read()
        key = get_aes_key()

        passwords = json.loads(aes(key).decrypt(encrypted))
        current_len = len(passwords)

        for i in range(len(passwords)):
            if passwords[i]['url'] == url:
                passwords.pop(i)

                passwords = aes(key).encrypt(json.dumps(passwords))

                passwords_file = open('/home/{}/.le-chiffre/passwords.enc'.format(username), 'w')
                passwords_file.write(passwords.decode('utf-8'))
                passwords_file.close()

                print('le-chiffre: Deleted password for url => {}'.format(url))

        if current_len == len(passwords):
            print('le-chiffre: Sorry, I haven\'t found anything for that url!')

    elif sys.platform == 'win32' or sys.platform == 'win64':
        pass

# Setup min length of generated password
def set_password_length(length):
    username = get_username()

    if not os.path.exists('/home/{}/.le-chiffre/settings.json'.format(username)):
        if not os.path.exists('/home/{}/.le-chiffre'.format(username)):
            os.makedirs('/home/{}/.le-chiffre'.format(username))

        settings = dict(
            storage='local',
            min_password_length=length
        )

        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(username), 'w')
        settings_file.write(json.dumps(settings))
        settings_file.close()

    else:
        data = json.load(open('/home/{}/.le-chiffre/settings.json'.format(username)))

        data['min_password_length'] = length
        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(username), 'w')
        settings_file.write(json.dumps(data, sort_keys=True, indent=4))
        settings_file.close()

    print('le-chiffre: Established `min_password_length` to => {}'.format(length))

# Setup storage type like `local` either `dropbox`
def set_storage_type(storage):
    username = get_username()

    if not os.path.exists('/home/{}/.le-chiffre/settings.json'.format(username)):
        if not os.path.exists('/home/{}/.le-chiffre'.format(username)):
            os.makedirs('/home/{}/.le-chiffre'.format(username))

        settings = dict(
            storage=storage,
            min_password_length=10
        )

        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(username), 'w')
        settings_file.write(json.dumps(settings))
        settings_file.close()

    else:
        data = json.load(open('/home/{}/.le-chiffre/settings.json'.format(username)))

        data['storage'] = storage
        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(username), 'w')
        settings_file.write(json.dumps(data, sort_keys=True, indent=4))
        settings_file.close()

    print('le-chiffre: Established `storage` to => {}'.format(storage))

# Setup token if storage type is `dropbox`
def set_token(token):
    username = get_username()

    if not os.path.exists('/home/{}/.le-chiffre/settings.json'.format(username)):
        if not os.path.exists('/home/{}/.le-chiffre'.format(username)):
            os.makedirs('/home/{}/.le-chiffre'.format(username))

        settings = dict(
            storage='dropbox',
            min_password_length=10,
            token=token
        )

        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(username), 'w')
        settings_file.write(json.dumps(settings))
        settings_file.close()

    else:
        data = json.load(open('/home/{}/.le-chiffre/settings.json'.format(username)))

        data['token'] = token
        settings_file = open('/home/{}/.le-chiffre/settings.json'.format(username), 'w')
        settings_file.write(json.dumps(data, sort_keys=True, indent=4))
        settings_file.close()

    if os.path.exists('/home/{}/.le-chiffre/key.enc'.format(username))
        key = open('/home/{}/.le-chiffre/key.enc'.format(username), 'r').read()
        api.upload_key(key)

    else:
        key = str(random.getrandbits(128))
        api.upload_key(key)

    print('le-chiffre: Established `token` to => {}'.format(token))
