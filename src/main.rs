extern crate clap;
extern crate rpassword;

use clap::{Arg, App};

fn main() -> () {
    let matches = App::new("le-chiffre")
        .version("0.1.0")
        .author("@overthesanity <arthurandrosovich@gmail.com>")
        .arg(
            Arg::with_name("generate")
                .short("g")
                .long("generate")
                .help("generates hash on given password and stores in buffer")
                .takes_value(true)
        )
        .arg(
            Arg::with_name("find")
                .short("f")
                .long("find")
                .help("finds password by provided url")
                .takes_value(true)
        )
        .arg(
            Arg::with_name("list")
                .short("l")
                .long("list")
                .help("lists all passwords")
                .takes_value(true)
        )
        .arg(
            Arg::with_name("config")
                .short("c")
                .long("config")
                .help("setup configuration")
                .takes_value(true)
        )
        .get_matches();

    if matches.is_present("generate") {
        let generate: &str = matches.value_of("generate").unwrap();
        println!("Generate is {}", generate);
    } else if matches.is_present("find") {
        let find: &str = matches.value_of("find").unwrap();
    } else if matches.is_present("list") {
        let list: &str = matches.value_of("list").unwrap();
        println!("List is {}", list);
    } else if matches.is_present("config") {
        let config: &str = matches.value_of("config").unwrap();
    } else {
        //print!("Введите пароль: ");
        //let pass: &str = rpassword::read_password().unwrap();
    }
}
