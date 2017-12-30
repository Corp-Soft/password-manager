import * as fs from 'fs';

import {
    Data,
    getUsername,
    getSettings,
    makeDefaultDir
} from './passwords';

import {
    uploadKey
} from './api';

export const setPasswordLength = async (length: number): Promise<void> => {
    const username: string = await getUsername();
    const exists: boolean = fs.existsSync(`/home/${username}/.le-chiffre/settings.json`);

    if (exists) {
        const data: Data = await getSettings();
        data.minPasswordLength = length;

        fs.writeFileSync(`/home/${username}/.le-chiffre/settings.json`, JSON.stringify(data));
    } else {
        await makeDefaultDir();

        const data: Data = {
            storage: 'local',
            minPasswordLength: length
        };

        fs.writeFileSync(`/home/${username}/.le-chiffre/settings.json`, JSON.stringify(data));
    }

    console.log(`le-chiffre: Established 'minPasswordLength' to => ${length}`);
};

export const setStorageType = async (type: string): Promise<void> => {
    const username: string = await getUsername();
    const exists: boolean = fs.existsSync(`/home/${username}/.le-chiffre/settings.json`);

    if (exists) {
        const data: Data = await getSettings();
        data.storage = type;

        fs.writeFileSync(`/home/${username}/.le-chiffre/settings.json`, JSON.stringify(data));
    } else {
        await makeDefaultDir();

        const data: Data = {
            storage: type,
            minPasswordLength: 10
        };

        fs.writeFileSync(`/home/${username}/.le-chiffre/settings.json`, JSON.stringify(data));
    }

    console.log(`le-chiffre: Established 'storage' to => ${type}`);
};

export const setToken = async (token: string): Promise<void> => {
    const username: string = await getUsername();
    const exists: boolean = fs.existsSync(`/home/${username}/.le-chiffre/settings.json`);

    if (exists) {
        const data: Data = await getSettings();
        data.token = token;

        fs.writeFileSync(`/home/${username}/.le-chiffre/settings.json`, JSON.stringify(data));
    } else {
        await makeDefaultDir();

        const data: Data = {
            storage: 'dropbox',
            minPasswordLength: 10,
            token: token
        };

        fs.writeFileSync(`/home/${username}/.le-chiffre/settings.json`, JSON.stringify(data));
    }

    const keyExists: boolean = fs.existsSync(`/home/${username}/.le-chiffre/key.enc`);
    let key: string | undefined = undefined;

    if (keyExists) {
        key = fs.readFileSync(`/home/${username}/.le-chiffre/key.enc`, 'utf8');
    } else {
        key = Math.random().toString(36).substring(2);
    }

    uploadKey(key);

    console.log(`le-chiffre: Established 'token' to => ${token}`);
};
