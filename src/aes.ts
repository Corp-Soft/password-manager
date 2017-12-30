import * as crypto from 'crypto';

const algorithm = 'aes-256-cbc';

/**
 * 
 * @param key
 * @param data
 * @return string
 */
export const encrypt = (key: string, data: string): string => {
    const iv: Buffer = crypto.randomBytes(16);
    const cipher: crypto.Cipher = crypto.createCipheriv(algorithm, key, iv);
    let encrypted: Buffer = cipher.update(new Buffer(data));
    encrypted = Buffer.concat([encrypted, cipher.final()]);
    return iv.toString('hex') + ':' + encrypted.toString('hex');
};

/**
 * 
 * @param key
 * @param data
 * @return string
 */
export const decrypt = (key: string, data: string): string => {
    let textParts: Array<any> = data.split(':');
    const iv: Buffer = new Buffer(textParts.shift(), 'hex');
    const encryptedText: Buffer = new Buffer(textParts.join(':'), 'hex');
    const decipher: crypto.Decipher = crypto.createDecipheriv(algorithm, new Buffer(key), iv);
    let decrypted: Buffer = decipher.update(encryptedText);
    decrypted = Buffer.concat([decrypted, decipher.final()]);
    return decrypted.toString();
};
