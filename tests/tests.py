import unittest, os, sys, random, subprocess, string, json
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

from src.aes import aes

def parse_url(url):
    url = url.split('.')
    return len(url) > 1

def parse_config(args):
    option = args[1]
    argument = args[2]
    return option, argument

class TestLeChiffrePackage(unittest.TestCase):
    def test_aes_algorithm(self):
        message = 'Hello, World!'
        hash = str(random.getrandbits(128))

        cipher = aes(hash).encrypt(message)
        message_decrypted = aes(hash).decrypt(cipher)

        self.assertEqual(message, message_decrypted)

    def test_parse_config(self):
        self.assertEqual(parse_config(['le-chiffre', 'generate', 'vk.com']), ('generate', 'vk.com'))

    def test_parse_url(self):
        self.assertTrue(parse_url('heroku.com'))
        self.assertFalse(parse_url('test'))

    def test_dropbox_package(self):
        import dropbox
        self.assertTrue(dropbox.__version__ is not None)
        self.assertTrue(type(dropbox.__version__) == str)

    def test_generate_password(self):
        random_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        hash = str(random.getrandbits(128))

        passwords = list()

        chiffre = dict(
            password=random_password,
            url='heroku.com'
        )

        passwords.append(chiffre)

        self.assertEqual(len(passwords), 1)

        passwords = aes(hash).encrypt(json.dumps(passwords))

        passwords = json.loads(aes(hash).decrypt(passwords))

        self.assertEqual(type(passwords), list)
        self.assertEqual(len(passwords), 1)
        self.assertEqual(passwords[0]['url'], 'heroku.com')
        self.assertEqual(passwords[0]['password'], random_password)

if __name__ == '__main__':
    unittest.main()
