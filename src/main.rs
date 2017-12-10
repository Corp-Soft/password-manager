extern crate rpassword;
extern crate rand;

#[macro_use]
extern crate serde_derive;

extern crate serde;
extern crate serde_json;

use std::env;
use std::str;
use std::fs::File;
use std::io::prelude::*;
use std::fmt;
use std::error::Error;
use std::path::Path;

use rand::{ OsRng, Rng };

mod aes;

struct Chiffre {
    url: String,
    password: String
}

fn main() -> () {
    let args: Vec<String> = env::args().collect();

    match args.len() {
        // Check if 1 option was given in command line
        2 => {
            let query: &str = &args[1] as &str;
            
            match query {
                "list" => {

                }

                _ => {
                    println!("le-chiffre: Invalid option!");
                }
            }
        }

        // Check if 2 options were given in command line
        // e.g. le-chiffre generate <url>
        // name of executed file is always the first argument
        3 => {
            let (option, argument) = parse_config(&args);

            match option {
                "generate" => {
                    if parse_url(argument) {

                    } else {
                        println!("le-chiffre: You've provided invalid url!");
                    }
                }

                _ => {
                    println!("le-chiffre: You've provided incorrent option!");
                }
            }
        }

        // If programme was called w/e any argument
        // just print information
        _ => {
            println!("le-chiffre 0.1.0");
            println!("@overthesanity <arthurandrosovich@gmail.com>");
            println!("\nUSAGE:");
            println!("  le-chiffre [OPTIONS]");
            println!("\nOPTIONS:");
            println!("  generate <url>");
            println!("  find <url>");
            println!("  list");
            println!("  config <config>");
        }
    }

    let message = "hello world";

    create_key_iv_file();
    let (key, iv) = read_key_iv_file();

    let encrypted_data: Vec<u8> = aes::encrypt(message.as_bytes(), &key, &iv).ok().unwrap();
    let decrypted_data: Vec<u8> = aes::decrypt(&encrypted_data[..], &key, &iv).ok().unwrap();
    println!("{}", String::from_utf8_lossy(&decrypted_data));
}

// Get option and argument from array of arguments
fn parse_config(args: &[String]) -> (&str, &str) {
    let option = &args[1];
    let argument = &args[2];

    (option, argument)
}

// Check if programme was called with valid URL
fn parse_url(url: &str) -> bool {
    let split = url.split(".");
    let vec = split.collect::<Vec<&str>>();

    if vec.len() > 1 {
        return true;
    } else {
        return false;
    }
}

// We store key and initializing vector in file called `password-manager.key`
// that's the point of using AES algorithm tho
fn read_key_iv_file() -> ([u8; 32], [u8; 16]) {
    let path = Path::new("/home/overthesanity/projects/le-chiffre/password-manager.key");
    let display = path.display();

    let mut file = match File::open(&path) {
        Err(why) => {
            panic!("le-chiffre: Couldn't open {}: {}", display, why.description())
        }

        Ok(file) => file
    };

    let mut s: String = String::new();

    match file.read_to_string(&mut s) {
        Err(why) => panic!("couldn't read {}: {}", display, why.description()),
        Ok(_) => ()
    }

    let key_iv_data: &'static str = aes::string_to_static_str(s);

    let split_key_iv_data = key_iv_data.split("\n");
    let key_iv_vector = split_key_iv_data.collect::<Vec<&str>>();

    let key_vec: Vec<u8> = parse_string_to_vec(key_iv_vector[0]);
    let iv_vec: Vec<u8> = parse_string_to_vec(key_iv_vector[1]);

    let key: [u8; 32] = key_vec_to_array(key_vec);
    let iv: [u8; 16] = iv_vec_to_array(iv_vec);

    (key, iv)
}

// Everything that is stored in file is string, even if looks like
// vector or array e.g. [1, 2, 3, 4] <= String
// thus we have to parse this string to real vector
// we remove those braces `[` and `]` then we split string by `, `
fn parse_string_to_vec(string: &str) -> Vec<u8> {
    let skip_braces = string.to_string().replace("[", "").replace("]", "");
    let string_vec: Vec<String> = skip_braces.split(", ").map(|s| s.to_string()).collect();
    let parsed_vec: Vec<u8> = string_vec.to_vec().iter().map(|s| s.parse::<u8>().unwrap()).collect();
    parsed_vec
}

// Rust crypto library uses arrays not vectors
// these are different types in Rust
// array is a data structure with fixed size
// either vector has dynamic size
fn key_vec_to_array(vector: Vec<u8>) -> [u8; 32] {
    let mut arr = [0u8; 32];
    for (place, element) in arr.iter_mut().zip(vector.iter()) {
        *place = *element;
    }
    arr
}

// We can't declare one method for converting vec to array unfortunately
fn iv_vec_to_array(vector: Vec<u8>) -> [u8; 16] {
    let mut arr = [0u8; 16];
    for (place, element) in arr.iter_mut().zip(vector.iter()) {
        *place = *element;
    }
    arr
}

// We generate `key` and `initializing vector` arrays
// `key` array is 32 size and `iv` is 16
// we fill those arrays with random bytes and store in file
// in the nearby future we will use these arrays for encryption and vice versa
fn create_key_iv_file() -> () {
    let path = Path::new("/home/overthesanity/projects/le-chiffre/password-manager.key");
    let mut file = File::create(&path).unwrap();

    let mut key: [u8; 32] = [0; 32];
    let mut iv: [u8; 16] = [0; 16];

    let mut rng = OsRng::new().ok().unwrap();

    rng.fill_bytes(&mut key);
    rng.fill_bytes(&mut iv);

    let key_iv_writable = format!("{:?}\n{:?}", key, iv);

    file.write_all(key_iv_writable.as_bytes());;
}
