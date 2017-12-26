import sys, os, subprocess, json, api, random, string
from aes import aes
import passwords

usage = '''le-chiffre 1.0.0
@overthesanity <arthurandrosovich@gmail.com>

Usage: le-chiffre COMMAND

Fast and secure command line tool for generating random passwords

Options:
    -g, generate <url>               Generate random hash, store in encrypted file and copy to clipboard
    -f, find <url>                   Find necessary password for given URL and copy to clipboard
    -l, list                         List all available passwords
    -r, remove <url>                 Remove password for given URL
    -v, version                      Print version information and quit
    set min_password_length <number> Set minimum password length'''

version = 'le-chiffre version 1.0.0'

# Get option and argument from list of arguments
def parse_config(args):
    option = args[1]
    argument = args[2]
    return option, argument

# Check if package was called with valid URL
def parse_url(url):
    url = url.split('.')
    return len(url) > 1

def main(): 
    args = sys.argv

    if len(args) == 1:
        print(usage)

    # Check if one option was given in command line
    elif len(args) == 2:
        if args[1] == '-l' or args[1] == 'list':
            passwords.list_passwords()

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
                passwords.generate_password(argument)
            else:
                print('le-chiffre: You\'ve provided invalid url!')

        elif option == '-f' or option == 'find':
            if parse_url(argument):
                passwords.find_password(argument)
            else:
                print('le-chiffre: You\'ve provided invalid url!')

        elif option == '-r' or option == 'remove':
            if parse_url(argument):
                passwords.remove_password(argument)
            else:
                print('le-chiffre: You\'ve provided invalid url!')

        else:
            print('le-chiffre: You\'ve provided incorrent option!')

    # Length of arguments for configuration
    elif len(args) == 4:
        option, argument = parse_config(args[-3:])

        if option == 'min_password_length':
            passwords.set_password_length(int(argument))

        elif option == 'storage':
            passwords.set_storage_type(argument)

        elif option == 'token':
            passwords.set_token(argument)

if __name__ == '__main__':
    main()
