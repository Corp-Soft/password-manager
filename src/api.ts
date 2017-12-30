import * as fs from 'fs';
import Dropbox = require('dropbox');
import { Data, getUsername, getSettings } from './passwords';

/**
 * Read token from settings needed for dropbox client
 */
export const readToken = async (): Promise<any> => {
    const data: Data = await getSettings();

    if (data.hasOwnProperty('token')) {
        return data.token;
    } else {
        console.log('le-chiffre: Please setup token, use `set token YOUR_TOKEN`!');
        process.exit();
    }
};

/**
 * Try to download `key` file from cloud
 */
export const getKey = async (): Promise<any> => {
    const client = new Dropbox({
        accessToken: await readToken()
    });

    try {
        const res = await client.filesDownload({
            path: '/le-chiffre/key'
        });

        return (res as any).fileBinary;
    } catch (e) {
        console.log('le-chiffre: Some HTTP error occured | tried to get key from Dropbox!');
        process.exit();
    }
};

/**
 * Upload AES key to cloud
 * @param key 
 */
export const uploadKey = async (key: string): Promise<any> => {
    const client = new Dropbox({
        accessToken: await readToken()
    });

    try {
        const res = await client.filesUpload({
            path: '/le-chiffre/key',
            contents: key
        });

        if ((res as any).hasOwnProperty('id') && (res as any).hasOwnProperty('name')) {
            const username: string = await getUsername();

            fs.exists(`/home/${username}/.le-chiffre/key.enc`, (exists: boolean) => {
                if (exists) {
                    fs.unlinkSync(`/home/${username}/.le-chiffre/key.enc`);
                }
            });

            console.log('le-chiffre: Uploaded current key to cloud!');
            return true;
        }
    } catch (e) {
        console.log('le-chiffre: Some HTTP error occured | tried to upload key to Dropbox!');
        process.exit();
    }
};
