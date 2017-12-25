<p align="center">
    <img src="https://dewey.tailorbrands.com/production/brand_version_mockup_image/673/441186673_a4693e27-0973-4ad6-a875-7e165c0d8eee.png?cb=1512853920">
</p>
<p align="center">A command line tool for generating random passwords</p>

<hr>

<p align="center">
    <a href="https://github.com/Corp-Soft/password-manager/blob/master/LICENSE">
        <img src="https://img.shields.io/badge/License-MIT-green.svg">
    </a>
</p>

<h2>Operating system support</h2>
<p><code>le-chiffre</code> can be run on Linux, Windows and Mac OS X.</p>

<h2>Dependencies</h2>
<ul>
    <li>
        <a href="http://sourceforge.net/projects/xclip/" rel="nofollow">xclip</a> for clipboard support
    </li>
</ul>

<h3>Installing</h3>
<p>First of all, you should create an application on Dropbox, go to <a href="https://www.dropbox.com/developers/apps" rel="nofollow">apps</a>, click <code>Create app</code>, call it <code>le-chiffre</code>, then click <code>Generate token</code>, you will get access token, next create file somewhere you will execute package from<code>settings.json</code>, and pass token there, e.g.</p>

```json
{
    "token": "YOUR ACCESS TOKEN"
}
```

<h4>Linux / Mac OS X</h4>
<p>A binary package is available from the community repository.</p>

```bash
curl -L https://github.com/Corp-Soft/password-manager/releases/download/1.0.0/le-chiffre/le-chiffre-{Linux || Darwin}-x86_64 -o /usr/local/bin/le-chiffre
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
    <li>Be sure to use python 3.x version and also install pip package manager specially for python 3.x:</li>
</ul>

```bash
sudo apt install python3-pip
```

<ul>
    <li>Install <code>pyinstaller</code> tool to bundle this package:</li>
</ul>

```bash
sudo pip3 install pyinstaller
```

<ul>
    <li>Bundle this application and its dependencies into a single package:</li>
</ul>

```bash
pyinstaller --onefile src/le-chiffre.py
```

<ul>
    <li>You will get binary file in <code>dist</code> folder, just change mode for execution and run:</li>
</ul>

```bash
sudo chmod +x dist/le-chiffre
dist/le-chiffre
```
<h2>Usage</h2>

```bash
le-chiffre
```

<p>You can find all possible blueprints in the table below:</p>

<table>
    <thead>
        <tr>
            <th>Description</th>
            <th>Usage</th>
        </tr>
    </thead>

    <tbody>
        <tr>
            <td>Generate random hash, store in encrypted file and copy to clipboard</td>
            <td><code>le-chiffre -g || generate {URL}</code></td>
        </tr>
        <tr>
            <td>Find necessary password for given URL and copy to clipboard</td>
            <td><code>le-chiffre -f || find {URL}</code></td>
        </tr>
        <tr>
            <td>List all available passwords</td>
            <td><code>le-chiffre -l || list</code></td>
        </tr>
        <tr>
            <td>Remove password for given URL</td>
            <td><code>le-chiffre -r || remove {URL}</code></td>
        </tr>
        <tr>
            <td>Print version information and quit</td>
            <td><code>le-chiffre -v || version</code></td>
        </tr>
        <tr>
            <td>Set minimum password length</td>
            <td><code>le-chiffre set min_password_length {number}</code></td>
        </tr>
    </tbody>
</table>
