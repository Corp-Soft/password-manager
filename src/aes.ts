import * as crypto from 'crypto';

const algorithm = 'aes-256-ctr';

/**
 * 
 * @param key
 * @param data
 * @return string
 */
export const encrypt = (key: string, data: string): string => {
    const cipher: crypto.Cipher = crypto.createCipher(algorithm, key);
    let crypted: string = cipher.update(data, 'utf8', 'hex');
    crypted += cipher.final('hex');
    return crypted;
};

/**
 * 
 * @param key
 * @param data
 * @return string
 */
export const decrypt = (key: string, data: string): string => {
    const decipher: crypto.Decipher = crypto.createDecipher(algorithm, key);
    let dec: string = decipher.update(data, 'hex', 'utf8');
    dec += decipher.final('utf8');
    return dec;
};
