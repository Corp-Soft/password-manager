import dropbox, json, os

def read_token():
    if os.path.exists(os.getcwd() + '/settings.json'):
        return json.load(open('settings.json'))['token']
    else:
        raise Exception('le-chiffre: Please create `settings.json` file and put `token` there!')
        return None

def get_hash():
    client = dropbox.Dropbox(read_token())

    try:
        md, res = client.files_download('/le-chiffre/hash')
    except dropbox.exceptions.HttpError:
        print('le-chiffre: Some HTTP error occured | tried to get hash from Dropbox!')
        return None
    
    return json.loads(res.content.decode('utf-8'))['hash']

def upload_hash(hash):
    if type(hash) == str:
        client = dropbox.Dropbox(read_token())

        hash = json.dumps(dict(
            hash=hash
        )).encode()

        try:
            client.files_upload(hash, '/le-chiffre/hash')
        except dropbox.exceptions.HttpError:
            print('le-chiffre: Some HTTP error occured | tried to upload hash to Dropbox!')
            return False

        return True

    else:
        return False
