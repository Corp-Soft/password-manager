extern crate serde_json;
use serde_json::{ Value };

extern crate rand;
use rand::{ OsRng, Rng };

use std::path::Path;
use std::process::Command;
use std::fs::{ File };
use std::io::prelude::*;
use std::io::Error;

mod aes;

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

fn parse_url(url: &str) -> bool {
    let split = url.split(".");
    let vec = split.collect::<Vec<&str>>();

    if vec.len() > 1 {
        return true;
    } else {
        return false;
    }
}

fn iv_vec_to_array(vector: Vec<u8>) -> [u8; 16] {
    let mut arr = [0u8; 16];
    for (place, element) in arr.iter_mut().zip(vector.iter()) {
        *place = *element;
    }
    arr
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_parse_string_to_vec() -> () {
        let parsed_vec: Vec<u8> = parse_string_to_vec("[1, 2, 3, 4]");
        assert_eq!(vec![1, 2, 3, 4], parsed_vec);
    }

    #[test]
    fn test_key_vec_to_array() -> () {
        let array: [u8; 32] = key_vec_to_array(vec![0; 32]);
        assert_eq!([0; 32], array);
    }

    #[test]
    fn test_serde_json() -> () {
        let json_str = r#"
            {
                "url": "heroku.com",
                "password": "12345"
            }
        "#;

        let v: Value = serde_json::from_str(json_str).unwrap();

        assert_eq!("heroku.com", v["url"]);
        assert_eq!("12345", v["password"])
    }

    #[test]
    fn test_existing_directory() -> () {
        let output = Command::new("whoami").output().expect("An error occured running `whoami`");
        let mut username: String = String::from_utf8(output.stdout).unwrap();
        username = username.replace("\n", "");

        let path: &str = aes::string_to_static_str(format!("/home/{}/.le-chiffre", username));
        assert_eq!(Path::new(path).exists(), true);
    }

    #[test]
    fn test_parse_url() -> () {
        assert_eq!(parse_url("test string"), false);
        assert_eq!(parse_url("heroku.com"), true);
    }

    #[test]
    fn test_aes_algorithm() -> () {
        let test_message = "Hello, World!";

        let mut key: [u8; 32] = [0; 32];
        let mut iv: [u8; 16] = [0; 16];

        let mut rng = OsRng::new().ok().unwrap();

        rng.fill_bytes(&mut key);
        rng.fill_bytes(&mut iv);

        let encrypted_data: Vec<u8> = aes::encrypt(test_message.as_bytes(), &key, &iv).ok().unwrap();
        let decrypted_data: Vec<u8> = aes::decrypt(&encrypted_data, &key, &iv).ok().unwrap();

        assert_eq!("Hello, World!", String::from_utf8(decrypted_data).unwrap());
    }

    #[test]
    fn test_write_key_iv_to_file() -> () {
        let mut key: [u8; 32] = [0; 32];
        let mut iv: [u8; 16] = [0; 16];

        let mut rng = OsRng::new().ok().unwrap();

        rng.fill_bytes(&mut key);
        rng.fill_bytes(&mut iv);

        let output = Command::new("whoami").output().expect("An error occured running `whoami`");
        let mut username: String = String::from_utf8(output.stdout).unwrap();
        username = username.replace("\n", "");

        let path = Path::new(aes::string_to_static_str(format!("/home/{}/projects/le-chiffre/password-manager.key", username)));
        let mut file = File::create(&path).unwrap();

        let key_iv_writable = format!("{:?}\n{:?}", key, iv);

        file.write_all(key_iv_writable.as_bytes()).expect("An error occured | tried to write file!");

        let display = path.display();

        file = File::open(&path).expect("An error occured while opening file!");

        let mut s: String = String::new();

        file.read_to_string(&mut s).expect("An error occured while reading file!");

        let key_iv_data: &'static str = aes::string_to_static_str(s);

        let split_key_iv_data = key_iv_data.split("\n");
        let key_iv_vector = split_key_iv_data.collect::<Vec<&str>>();

        let key_vec: Vec<u8> = parse_string_to_vec(key_iv_vector[0]);
        let iv_vec: Vec<u8> = parse_string_to_vec(key_iv_vector[1]);

        let read_key: [u8; 32] = key_vec_to_array(key_vec);
        let read_iv: [u8; 16] = iv_vec_to_array(iv_vec);

        assert_eq!(read_key, key);
        assert_eq!(read_iv, iv);
    }
}
