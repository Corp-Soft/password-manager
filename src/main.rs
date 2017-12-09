extern crate rpassword;

use std::env;

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
}

fn parse_config(args: &[String]) -> (&str, &str) {
    let query = &args[1];
    let argument = &args[2];

    (query, argument)
}

fn parse_url(url: &str) -> bool {
    let mut split = url.split(".");
    let vec = split.collect::<Vec<&str>>();

    if vec.len() > 1 {
        return true;
    } else {
        return false;
    }
}
