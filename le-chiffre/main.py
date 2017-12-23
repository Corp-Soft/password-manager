import sys
import os
import subprocess
import json
import api
import random
import string
from aes import aes

usage = '''le-chiffre 0.1.0
@overthesanity <arthurandrosovich@gmail.com>

Usage: le-chiffre COMMAND

Fast and secure command line tool for generating random passwords

Options:
    -g, generate <url>    Generate random hash, store in encrypted file and copy to clipboard
    -f, find <url>        Find necessary password for given URL and copy to clipboard 
    -l, list              List all available passwords   
    -v, version           Print version information and quit'''

version = 'le-chiffre version 0.0.1@alpha'

# Get option and argument from list of arguments
def parse_config(args):
    option = args[1]
    argument = args[2]
    return option, argument

# Check if programme was called with valid URL
def parse_url(url):
    url = url.split('.')
    return len(url) > 1

def copy_to_clipboard(password):
    if sys.platform == 'linux' or sys.platform == 'linux2':
        os.system('echo {} | xclip -sel clip'.format(password))
    
    elif sys.platform == 'darwin':
        pass

    elif sys.platform == 'win32' or sys.platform() == 'win64':
        pass

    print('le-chiffre: Copied password to clipboard!')

# Get username if programme is running on Linux either Mac
def get_username():
    return subprocess.getoutput('whoami')

# Main password generation process
def generate_password(url):
    username = get_username()
    random_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

    if os.path.exists('/home/{}/.le-chiffre'.format(username)):
        encrypted = open('/home/{}/.le-chiffre/passwords.enc'.format(username)).read()

        hash = api.get_hash()
        passwords = json.loads(aes(hash).decrypt(encrypted))

        if type(passwords) == list:
            for i in passwords:
                if i['url'] == url:
                    print('le-chiffre: Password for that url is already generated!')
                    sys.exit(0)

            chiffre = dict(
                password=random_password,
                url=url
            )

            passwords.append(chiffre)
            passwords = aes(hash).encrypt(json.dumps(passwords))

            passwords_file = open('/home/{}/.le-chiffre/passwords.enc'.format(username), 'w')
            passwords_file.write(passwords.decode('utf8'))
            passwords_file.close()

            print('le-chiffre: Generated password for {0} => {1}'.format(url, random_password))
            copy_to_clipboard(random_password)

    else:
        # this hash is necessary in AES algorithm
        hash = str(random.getrandbits(128))
        # upload hash needed for decryption to Dropbox cloud
        api.upload_hash(hash)
        # create empty list because it doesn't exist yet
        passwords = list()

        # create chiffre
        chiffre = dict(
            password=random_password,
            url=url
        )

        passwords.append(chiffre)
        # first we stringifying list with dict, then we encrypt this string
        passwords = aes(hash).encrypt(json.dumps(passwords))

        os.makedirs('/home/{}/.le-chiffre'.format(username))
        # write this encrypted string to file
        passwords_file = open('/home/{}/.le-chiffre/passwords.enc'.format(username), 'w')
        passwords_file.write(passwords.decode('utf8'))
        passwords_file.close()

        print('le-chiffre: Generated password for {0} => {1}'.format(url, random_password))
        copy_to_clipboard(random_password)

# Tryna find password for given URL in encrypted `passwords` file
def find_password(url):
    print('le-chiffre: You\'re searching password for url {}'.format(url))
    username = get_username()

    if os.path.exists('/home/{}/.le-chiffre'.format(username)):
        encrypted = open('/home/{}/.le-chiffre/passwords.enc'.format(username)).read()

        hash = api.get_hash()
        passwords = json.loads(aes(hash).decrypt(encrypted))

        if type(passwords) == list:
            searchable_password = None

            for i in passwords:
                if i['url'] == url:
                    searchable_password = i['password']

            if searchable_password is not None and len(searchable_password) > 0:
                print('le-chiffre: I\'ve found {}'.format(searchable_password))
                copy_to_clipboard(searchable_password)
            else:
                print('le-chiffre: Sorry, I haven\'t found anything for that url!')

    else:
        print('le-chiffre: You haven\'t generated any password yet to find anything!')

# List all available passwords
def list_passwords():
    username = get_username()

    if os.path.exists('/home/{}/.le-chiffre'.format(username)):
        print('le-chiffre: List all passwords!')

        encrypted = open('/home/{}/.le-chiffre/passwords.enc'.format(username)).read()

        hash = api.get_hash()
        passwords = json.loads(aes(hash).decrypt(encrypted))

        if type(passwords) == list:
            print('\n')
            for i in passwords:
                password = i['password']
                url = i['url']
                print('le-chiffre: password => {0}, url => {1}'.format(password, url))

    else:
        print('le-chiffre: You haven\'t generated any password yet to list them!')

def main(): 
    args = sys.argv

    if len(args) == 1:
        print(usage)

    # Check if one option was given in command line
    elif len(args) == 2:
        if args[1] == '-l' or args[1] == 'list':
            list_passwords()

        elif args[1] == '-v' or args[1] == 'version':
            print(version)

        else:
            print('le-chiffre: Invalid option!')

    # Check if 2 options were given in command line
    # e.g. le-chiffre generate <url>
    # name of executed file is always the first argument
    elif len(args) == 3:
        option, argument = parse_config(args)

        if option == '-g' or option == 'generate':
            if parse_url(argument):
                generate_password(argument)
            else:
                print('le-chiffre: You\'ve provided invalid url!')

        elif option == '-f' or option == 'find':
            if parse_url(argument):
                find_password(argument)
            else:
                print('le-chiffre: You\'ve provided invalid url!')

        else:
            print('le-chiffre: You\'ve provided incorrent option!')

if __name__ == '__main__':
    main()
