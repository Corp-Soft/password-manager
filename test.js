import test from 'ava';
import crypto from 'crypto';
import fs from 'fs';
import generator from 'generate-password';
import util from 'util';
const exec = util.promisify(require('child_process').exec);

const algorithm = 'aes-256-cbc';

function encrypt(key, data) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(algorithm, key, iv);
    let encrypted = cipher.update(new Buffer(data));
    encrypted = Buffer.concat([encrypted, cipher.final()]);
    return iv.toString('hex') + ':' + encrypted.toString('hex');
}

function decrypt(key, data) {
    let textParts = data.split(':');
    const iv = new Buffer(textParts.shift(), 'hex');
    const encryptedText = new Buffer(textParts.join(':'), 'hex');
    const decipher = crypto.createDecipheriv(algorithm, new Buffer(key), iv);
    let decrypted = decipher.update(encryptedText);
    decrypted = Buffer.concat([decrypted, decipher.final()]);
    return decrypted.toString();
}

async function getUsername() {
    const { stdout } = await exec('whoami');
    return stdout.replace('\n', '');
}

test('aes algorithm', t => {
    const message = 'Hello, World!';
    const key = generator.generate({
        length: 32,
        numbers: true
    });

    const encrypted = encrypt(key, message);
    const decrypted = decrypt(key, encrypted);
    t.is(decrypted, message);
});

test('creating settings', async t => {
    const username = await getUsername();
    let data = {
        storage: 'local',
        minPasswordLength: 10
    };

    const defaultDir = `/home/${username}/.le-chiffre`;
    const exists = fs.existsSync(defaultDir)

    if (exists) {
        fs.rmdirSync(defaultDir);
    }

    fs.mkdirSync(`/home/${username}/.le-chiffre`);

    fs.writeFileSync(`${defaultDir}/settings.json`, JSON.stringify(data));

    data = JSON.parse(fs.readFileSync(`${defaultDir}/settings.json`, 'utf8'));

    t.is(data.minPasswordLength, 10);
    t.is(data.storage, 'local');
});
