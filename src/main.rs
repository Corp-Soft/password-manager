extern crate clap;
extern crate rand;
extern crate rpassword; 

use clap::{Arg, App};

use std::f64;

use rand::Rng;

pub struct PublicKey {
    e: u64,
    n: u64
}

impl PublicKey {
    fn new(e: &u64, n: &u64) -> PublicKey {
        PublicKey {
            e: *e,
            n: *n
        }
    }
}

pub struct PrivateKey {
    d: u64,
    n: u64
}

impl PrivateKey {
    fn new(d: &u64, n: &u64) -> PrivateKey {
        PrivateKey {
            d: *d,
            n: *n
        }
    }
}

fn main() -> () {
    let matches = App::new("cipher")
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

    let (public_key, private_key) = generate_keys();
}

fn generate_password() -> () {

}

fn generate_keys() -> (PublicKey, PrivateKey) {
    // RSA
    // Генерируем 2 простых числа `p`, `q`
    let mut p: u64 = rand::thread_rng().gen_range(1, 30);
    let mut q: u64 = rand::thread_rng().gen_range(1, 30);

    if !is_prime(p) {
        while !is_prime(p) {
            p = rand::thread_rng().gen_range(1, 30);

            if is_prime(p) {
                break;
            }
        }
    }

    if !is_prime(q) {
        while !is_prime(q) {
            q = rand::thread_rng().gen_range(1, 30);

            if is_prime(q) {
                break;
            }
        }
    }

    println!("Сгенерировал простые числа `p` и `q`: {}, {}", p, q);

    // Вычисляем модуль n = p * q
    let n: u64 = p * q;

    println!("Сгенерировал модуль n = p * q: {}", n);

    // Вычисляем функцию Эйлера
    let euler: u64 = (p - 1) * (q - 1);

    println!("Вычислил функцию Эейлера ф(n) = (p - 1) * (q - 1): {}", euler);

    // Вычисляем открытую экспоненту `e`
    // должна лежать в интервале 1 < e < ϕ(n)
    // а также быть взаимно простым со значением ф(n)
    let mut e: u64 = rand::thread_rng().gen_range(1, 999);

    if !relatively_prime(e, euler) || e > euler {
        while !relatively_prime(e, euler) && e > euler {
            e = rand::thread_rng().gen_range(1, 999);

            if relatively_prime(e, euler) && e < euler {
                break;
            }
        }
    }

    println!("Вычислил открытую экспоненту `e`: {}", e);

    // Вычисляем секретную экспоненту `d`
    let mut d: u64 = rand::thread_rng().gen_range(1, 999);

    if (d * e) % euler != 1 {
        while (d * e) % euler != 1 {
            d = rand::thread_rng().gen_range(1, 999);

            if (d * e) % euler == 1 {
                break;
            }
        }
    }

    println!("Вычислил секретную экспоненту `d`: {}", d);

    // Пара (e, n) - открытый ключ, (d, n) - закрытый

    println!("Открытый ключ (e, n): ({}, {}), закрытый ключ (d, n): ({}, {})", e, n, d, n);

    (PublicKey::new(&e, &n), PrivateKey::new(&d, &n))
}

fn is_prime(number: u64) -> bool {
    if number == 1 {
        return false;
    }

    if number == 2 {
        return true;
    }

    if number % 2 == 0 {
        return false;
    }

    let sqrt: u64 = (number as f64).sqrt() as u64;

    let mut i: u64 = 3;

    while i <= sqrt {
        if number % i == 0 {
            return false;
        }

        i += 2;
    }

    true
}

fn relatively_prime(a: u64, b: u64) -> bool {
    gcd(a, b) == 1
}

fn gcd(mut a: u64, mut b: u64) -> u64 {
    let mut t: u64;

    while b != 0 {
        t = a;
        a = b;
        b = t % b;
    }

    a
}
