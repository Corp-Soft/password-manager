<h1 align="center">
    <img src="https://dewey.tailorbrands.com/production/brand_version_mockup_image/673/441186673_a4693e27-0973-4ad6-a875-7e165c0d8eee.png?cb=1512853920">
</h1>
<p>This tool is still in development mode.</p>
<h2>Getting started</h2>
<p>These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.</p>
<h3>Installing on UNIX</h3>
<p>First, you have to create application on Dropbox, go to <a href="https://www.dropbox.com/developers/apps">apps</a>, click <code>Create app</code>, call it <code>le-chiffre</code>, then click <code>Generate token</code>, you will get access token, next create file somewhere <code>settings.json</code>, and pass token there, e.g.</p>

```json
{
    "token": "YOUR ACCESS TOKEN"
}
```

<p>Make sure you have installed <code>xclip</code>, if not</p>

```bash
$ sudo apt install xclip
```

<p>Be sure to use python 3.x version and also install <code>pip</code> package manager specially for python 3.x</p>

```bash
$ sudo apt install python3-pip
```

<p>Once you've ready to start, you have to clone this project and do the following</p>

```bash
$ git clone https://github.com/Corp-Soft/password-manager.git
$ cd password-manager
$ sudo pip3 install pyinstaller
$ pyinstaller le-chiffre/le-chiffre.py // this will bundle python app and its dependencies into a single package
$ sudo mv dist/main/le-chiffre ~ // move built package to home directory or anywhere you wanna execute it from
$ cd ~ 
$ sudo chmod +x ./le-chiffre
$ ./le-chiffre // run package
```
