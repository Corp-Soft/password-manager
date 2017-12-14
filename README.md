<h1 align="center">
    <img src="https://dewey.tailorbrands.com/production/brand_version_mockup_image/673/441186673_a4693e27-0973-4ad6-a875-7e165c0d8eee.png?cb=1512853920">
</h1>
<p>This tool is still in development mode.</p>
<h2>Getting started</h2>
<p>These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.</p>
<h3>Installing on UNIX</h3>
<p>First, make sure you have installed <code>xlip</code>, if not </p>

    $ sudo apt install xlip

<p>Once you've ready to start, you have to clone this project and install package manager for Rust - <code>Cargo</code>.</p>

```bash
$ git clone https://github.com/Corp-Soft/password-manager.git
$ cd password-manager
$ cargo build --release
$ sudo cp target/release/le-chiffre /home/username // or anywhere where you want execute script from
$ cd ~/username
$ sudo chmod +x ./le-chiffre
$ ./le-chiffre
```
