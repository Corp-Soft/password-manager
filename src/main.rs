extern crate rpassword;
extern crate rand;

use std::env;
use std::str;
use std::fs::File;
use std::io::prelude::*;
use std::fmt;

use rand::{ OsRng, Rng };

mod aes;

fn main() -> () {
    let args: Vec<String> = env::args().collect();

    match args.len() {
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

        3 => {
            let (query, argument) = parse_config(&args);

            match query {
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

fn parse_config(args: &[String]) -> (&str, &str) {
    let query = &args[1];
    let argument = &args[2];

    (query, argument)
}

fn parse_url(url: &str) -> bool {
    let split = url.split(".");
    let vec = split.collect::<Vec<&str>>();

    if vec.len() > 1 {
        return true;
    } else {
        return false;
    }
}

fn read_key_iv_file() -> ([u8; 32], [u8; 16]) {
    let key_iv_data: &'static str = aes::string_to_static_str(read_file("password-manager.key"));

    let split_key_iv_data = key_iv_data.split("\n");
    let key_iv_vector = split_key_iv_data.collect::<Vec<&str>>();

    let key_vec: Vec<u8> = parse_string_to_vec(key_iv_vector[0]);
    let iv_vec: Vec<u8> = parse_string_to_vec(key_iv_vector[1]);

    let key: [u8; 32] = key_vec_to_array(key_vec);
    let iv: [u8; 16] = iv_vec_to_array(iv_vec);

    (key, iv)
}

fn parse_string_to_vec(string: &str) -> Vec<u8> {
    let skip_braces = string.to_string().replace("[", "").replace("]", "");
    let string_vec: Vec<String> = skip_braces.split(", ").map(|s| s.to_string()).collect();
    let parsed_vec: Vec<u8> = string_vec.to_vec().iter().map(|s| s.parse::<u8>().unwrap()).collect();
    parsed_vec
}

fn key_vec_to_array(vector: Vec<u8>) -> [u8; 32] {
    let mut arr = [0u8; 32];
    for (place, element) in arr.iter_mut().zip(vector.iter()) {
        *place = *element;
    }
    arr
}

fn iv_vec_to_array(vector: Vec<u8>) -> [u8; 16] {
    let mut arr = [0u8; 16];
    for (place, element) in arr.iter_mut().zip(vector.iter()) {
        *place = *element;
    }
    arr
}

fn create_key_iv_file() -> () {
    let mut file = File::create("password-manager.key").unwrap();

    let mut key: [u8; 32] = [0; 32];
    let mut iv: [u8; 16] = [0; 16];

    let mut rng = OsRng::new().ok().unwrap();

    rng.fill_bytes(&mut key);
    rng.fill_bytes(&mut iv);

    let key_iv_writable = format!("{:?}\n{:?}", key, iv);

    file.write_all(key_iv_writable.as_bytes());;
}

fn read_file(filename: &str) -> String {
    let mut file = File::open(filename).expect("le-chiffre: File not found!");

    let mut file_content: String = String::new();
    file.read_to_string(&mut file_content).expect("le-chiffre: Woops, some shit happened while reading file!");

    file_content
}
