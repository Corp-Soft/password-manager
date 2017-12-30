import * as program from 'commander';
import {
    generatePassword,
    findPassword,
    listPasswords,
    removePassword
} from './passwords';

import {
    setPasswordLength,
    setStorageType,
    setToken
} from './settings';

program
    .version('le-chiffre version 1.0.0')
    .description('Fast and secure command line tool for generating random passwords');

program
    .command('generate <url>')
    .alias('g')
    .description('Generate random hash, store in encrypted file and copy to clipboard')
    .action(async (url: string) => {
        await generatePassword(url);
    });

program
    .command('find <url>')
    .alias('f')
    .description('Find necessary password for given URL and copy to clipboard')
    .action(async (url: string) => {
        await findPassword(url);
    });

program
    .command('list')
    .alias('l')
    .description('List all available passwords')
    .action(async () => {
        await listPasswords();
    });

program
    .command('remove')
    .alias('r')
    .description('Remove password for given URL')
    .action(async (url: string) => {
        await removePassword(url);
    });

program
    .command('set-length <length>')
    .description('Set minimum password length')
    .action(async (length: string) => {
        await setPasswordLength(parseInt(length, 10));
    });

program
    .command('set-storage <type>')
    .description('Set storage where to store AES key')
    .action(async (type: string) => {
        await setStorageType(type.trim());
    });

program
    .command('set-token <token>')
    .description('Set token if you chose dropbox storage')
    .action(async (token: string) => {
        await setToken(token.trim());
    });

program.parse(process.argv);
