import * as fs from 'fs';
import * as util from 'util';
const exec: Function = util.promisify(require('child_process').exec);
import * as clipboardy from 'clipboardy';
import * as generator from 'generate-password';

import {
    encrypt,
    decrypt
} from './aes';

export type Data = {
    storage: string,
    minPasswordLength: number,
    token?: string
};

type Chiffre = {
    url: string,
    password: string
};

/**
 * Get username of Linux/Mac user using `whoami` command
 */
export async function getUsername(): Promise<string> {
    const { stdout, stderr } = await exec('whoami');
    return stdout.replace('\n', '');
}

/**
 * 
 */
export async function getSettings(): Promise<Data> {
    const username: string = await getUsername();
    return JSON.parse(fs.readFileSync(`/home/${username}/.le-chiffre/settings.json`, 'utf8'));
}

/**
 * Get aes key based on storage type
 * If storage is `local` - package will try to search for key in `key.enc` file
 * If storage is `dropbox` - package will try to download key from cloud
 */
async function getAESKey(): Promise<string> {
    const username: string = await getUsername();
    const exists: boolean = fs.existsSync(`/home/${username}/.le-chiffre`);

    if (exists) {
        const data: Data = await getSettings();

        if (data.storage === 'local') {
            return fs.readFileSync(`/home/${username}/.le-chiffre/key.enc`, 'utf8');
        } else {
            if (data.hasOwnProperty('token')) {
                return '123';
            } else {
                console.log('le-chiffre: Please set token for dropbox!');
                process.exit();
            }
        }
    }
}

/**
 * Load passwords if present from encoded file
 */
async function getPasswords(): Promise<Array<Chiffre>> {
    const username: string = await getUsername();
    const encrypted: string = fs.readFileSync(`/home/${username}/.le-chiffre/passwords.enc`, 'utf8');
    const key: string = await getAESKey();
    return JSON.parse(decrypt(key, encrypted));
}

/**
 * 
 */
export async function makeDefaultDir(): Promise<void> {
    const username: string = await getUsername();

    fs.exists(`/home/${username}/.le-chiffre`, (exists: boolean) => {
        if (!exists) {
            fs.mkdirSync(`/home/${username}/.le-chiffre`);
            console.log('le-chiffre: Created default directory!');
        }
    });
}

/**
 * Exit process if any password is generated
 */
async function exitIfNoDefaultDir(message: string): Promise<void> {
    const username: string = await getUsername();

    fs.exists(`/home/${username}/.le-chiffre`, (exists: boolean) => {
        if (!exists)  {
            console.log(message);
            process.exit();
        }
    });
}

/**
 * Copy generated or found password to clipboard
 * @param password 
 */
function copyToClipboard(password: string): void {
    clipboardy.writeSync(password);
    console.log('le-chiffre: Copied password to clipboard!');
}

/**
 * Linux and Mac OS X basically have the same folders structure, we only need `/home/username` directory,
 * if storage is local - thus AES key is also stored locally
 * @param url
 * @return Promise<void>
 */
export const generatePassword = async (url: string): Promise<void> => {
    const username: string = await getUsername();

    await makeDefaultDir();

    fs.exists(`/home/${username}/.le-chiffre/settings.json`, (exists: boolean) => {
        if (!exists) {
            const data: Data = {
                storage: 'local',
                minPasswordLength: 10
            };

            fs.writeFileSync(`/home/${username}/.le-chiffre/settings.json`, JSON.stringify(data));
        }
    });

    const data: Data = await getSettings();

    const randomPassword: string = generator.generate({
        length: data.minPasswordLength,
        numbers: true
    });

    fs.exists(`/home/${username}/.le-chiffre/passwords.enc`, async (exists: boolean) => {
        if (exists) {
            const passwords: Array<Chiffre> = await getPasswords();

            for (const password of passwords) {
                if (password.url === url) {
                    console.log('le-chiffre: Password for that url is already generated!');
                    process.exit(0);
                }
            }

            const chiffre: Chiffre = {
                password: randomPassword,
                url: url
            };

            passwords.push(chiffre);
            const encrypted: string = encrypt(await getAESKey(), JSON.stringify(passwords));

            fs.writeFile(`/home/${username}/.le-chiffre/passwords.enc`, encrypted, (err: NodeJS.ErrnoException) => {
                if (!err) {
                    console.log(`le-chiffre: Generated password for ${url} => ${randomPassword}`);
                    copyToClipboard(randomPassword);
                }
            });
        } else {
            const keyExists: boolean = fs.existsSync(`/home/${username}/.le-chiffre/key.enc`);
            let key: string | undefined = undefined;

            if (keyExists) {
                key = fs.readFileSync(`/home/${username}/.le-chiffre/key.enc`, 'utf8');
            } else {
                key = Math.random().toString(36).substring(2);

                const data: Data = await getSettings();

                if (data.storage === 'local') {
                    fs.writeFileSync(`/home/${username}/.le-chiffre/key.enc`, key);
                }
            }

            const passwords: Array<Chiffre> = [];
            const chiffre: Chiffre = {
                password: randomPassword,
                url: url
            };

            passwords.push(chiffre);
            const encrypted: string = encrypt(key, JSON.stringify(passwords));

            fs.writeFile(`/home/${username}/.le-chiffre/passwords.enc`, encrypted, (err: NodeJS.ErrnoException) => {
                if (!err) {
                    console.log(`le-chiffre: Generated password for ${url} => ${randomPassword}`);
                    copyToClipboard(randomPassword);
                }
            });
        }
    });
};

/**
 * Tryna find password for given URL
 * @param url
 */
export const findPassword = async (url: string): Promise<void> => {
    console.log(`le-chiffre: You\'re searching password for url ${url}`);

    const username: string = await getUsername();

    await exitIfNoDefaultDir('le-chiffre: You haven\'t generated any password yet to find anything!');

    const passwords: Array<Chiffre> = await getPasswords();
    let searchablePassword: string | null = null;
    
    for (const password of passwords) {
        if (password.url === url) {
            searchablePassword = password.password;
        }
    }

    if (searchablePassword !== null) {
        console.log(`le-chiffre: I\'ve found ${searchablePassword}`);
        copyToClipboard(searchablePassword);
    } else {
        console.log('le-chiffre: Sorry, I haven\'t found anything for that url!');
    }
};

/**
 * List all available passwords
 */
export const listPasswords = async (): Promise<void> => {
    console.log('le-chiffre: List all passwords!');

    await exitIfNoDefaultDir('le-chiffre: You haven\'t generated any password yet to list them!');

    const passwords: Array<Chiffre> = await getPasswords();

    if (passwords.length === 0) {
        console.log('le-chiffre: Sorry you\'ve got zero passwords generated!');
    } else {
        for (const password of passwords) {
            console.log(`le-chiffre: password => ${password.url}, url => ${password.password}`);
        }
    }
};

/**
 * Remove password if present for given URL
 * @param url 
 */
export const removePassword = async (url: string): Promise<void> => {
    console.log(`le-chiffre: You wanna remove password for url => ${url}`);

    await exitIfNoDefaultDir('le-chiffre: You haven\'t generated any password yet to remove any!');

    const username: string = await getUsername();
    const passwords: Array<Chiffre> = await getPasswords();

    if (passwords.length === 0) {
        console.log('le-chiffre: Sorry you\'ve got zero passwords generated!');
    } else {
        for (let i = 0; i < passwords.length; i++) {
            const password: Chiffre = passwords[i];

            if (password.url === url) {
                passwords.splice(passwords.indexOf(password), 1);

                const key: string = await getAESKey();
                const encrypted: string = encrypt(key, JSON.stringify(passwords));

                fs.writeFileSync(`/home/${username}/.le-chiffre/passwords.enc`, encrypted);
                console.log(`le-chiffre: Removed password for url => ${url}`);
            }
        }
    }
};
