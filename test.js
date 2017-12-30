import test from 'ava';
import crypto from 'crypto';

const algorithm = 'aes-256-ctr';

function encrypt(key, data) {
    const cipher = crypto.createCipher(algorithm, key);
    let crypted = cipher.update(data, 'utf8', 'hex');
    crypted += cipher.final('hex');
    return crypted;
}

function decrypt(key, data) {
    const decipher = crypto.createDecipher(algorithm, key);
    let dec = decipher.update(data, 'hex', 'utf8');
    dec += decipher.final('utf8');
    return dec;
}

test('aes algorithm', t => {
    const message = 'Hello, World!';
    const key = crypto.randomBytes(32).toString();
    const encrypted = encrypt(key, message);
    const decrypted = decrypt(key, encrypted);
    t.is(decrypted, message);
});
