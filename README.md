<p align="center">
    <img src="https://dewey.tailorbrands.com/production/brand_version_mockup_image/365/463755365_f7ec8898-66d6-4a47-82db-9dc74f75c367.png?cb=1514282278">
</p>
<p align="center">
    Easily generate passwords, store them in encrypted file using AES algorithm and save key on Dropbox :closed_lock_with_key:
</p>

<hr>

<p>
<a href="https://github.com/Corp-Soft/password-manager/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg">
</a>

<a href="https://travis-ci.org/Corp-Soft/password-manager">
    <img src="https://travis-ci.org/Corp-Soft/password-manager.svg">
</a>

<a href="https://scrutinizer-ci.com/g/Corp-Soft/password-manager">
    <img src="https://scrutinizer-ci.com/g/Corp-Soft/password-manager/badges/quality-score.png?b=master">
</a>

<a href="https://badges.frapsoft.com/typescript/awesome/typescript.png?v=100">
    <img src="https://badges.frapsoft.com/typescript/awesome/typescript.png?v=100">
</a>
</p>

<p align="center">
    <img src="https://i.imgur.com/5eBSKM7.png">
</p>

<h2>Operating system support</h2>
<p><code>le-chiffre</code> can be run on Linux and Mac OS X.</p>

<h3>Installing</h3>

<h4>Linux / Mac OS X</h4>
<p>A binary package is available from the community repository.</p>

```bash
sudo curl -L https://github.com/Corp-Soft/password-manager/releases/download/1.0.0/le-chiffre-x86_64 -o /usr/local/bin/le-chiffre
sudo chmod +x /usr/local/bin/le-chiffre
```

<p>Alternatively, you can manually assemble this package</p>

<ul>
    <li>Clone repository and change directory:</li>
</ul>

```bash
git clone https://github.com/Corp-Soft/password-manager
cd password-manager
```

<ul>
    <li>Be sure to install <code>typescript</code> globally:</li>
</ul>

```bash
npm i -g typescript@latest
```

<ul>
    <li>Install necessary dependencies for this project also <code>nexe</code> bundler:</li>
</ul>

```bash
yarn install
# or if you don't use yarn
npm install
```

<ul>
    <li>Bundle this application and its dependencies into a single package:</li>
</ul>

```bash
yarn build
# or
npm run build
```

<ul>
    <li>You will get binary file in the root of folder:</li>
</ul>

```bash
sudo mv ./le-chiffre /usr/local/bin/le-chiffre
sudo chmod +x /usr/local/bin/le-chiffre
./le-chiffre
```
<h2>Usage</h2>

<p>You can decide what storage to use for AES key - local or cloud, local storage is default, if you wanna use Dropbox:</p>

```bash
le-chiffre set-storage dropbox
```

<p>Next, you should create an application on Dropbox, go to <a href="https://www.dropbox.com/developers/apps" rel="nofollow">apps</a>, click <code>Create app</code>, call it <code>le-chiffre</code>, then click <code>Generate token</code>, you will get access token, set this token to <code>le-chiffre</code> settings:</p>

```bash
le-chiffre set-token YOUR_TOKEN
```

<p>Since now your key will be uploaded to cloud and stored there.</p>

```bash
le-chiffre --help
```

<p>You can find all possible blueprints in the table below:</p>

| Description | Usage |
| ----------- | ----- |
| Generate random hash, store in encrypted file and copy to clipboard | <code>le-chiffre -g OR generate {URL}</code> |
| Find necessary password for given URL and copy to clipboard | <code>le-chiffre -f OR find {URL}</code> |
| List all available passwords | <code>le-chiffre -l OR list</code> |
| Remove password for given URL | <code>le-chiffre -r OR remove {URL}</code> |
| Print version information and quit | <code>le-chiffre -v OR version</code> |
| Set minimum password length | <code>le-chiffre set-length {number}</code> |
| Set storage type | <code>le-chiffre set-storage {local OR dropbox}</code> |
| Set token for cloud | <code>le-chiffre set-token {TOKEN}</code> |
