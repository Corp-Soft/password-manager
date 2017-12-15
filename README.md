<h1 align="center">
    <img src="https://dewey.tailorbrands.com/production/brand_version_mockup_image/673/441186673_a4693e27-0973-4ad6-a875-7e165c0d8eee.png?cb=1512853920">
</h1>
<p>This tool is still in development mode.</p>
<h2>Getting started</h2>
<p>These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.</p>
<h3>Installing on UNIX</h3>
<p>First, make sure you have installed <code>xclip</code>, if not </p>

```bash
$ sudo apt install xclip
```

<p>As this is a Rust project - you should have package manager for Rust - <code>Cargo</code>, install it with</p>

```bash
$ curl -sSf https://static.rust-lang.org/rustup.sh | sh
$ cargo -V
```

<p>Once you've ready to start, you have to clone this project and do the following</p>

```bash
$ git clone https://github.com/Corp-Soft/password-manager.git
$ cd password-manager
$ cargo build --release
$ sudo cp target/release/le-chiffre ~ // or anywhere where you want execute script from
$ cd ~
$ sudo chmod +x ./le-chiffre
$ ./le-chiffre
```
