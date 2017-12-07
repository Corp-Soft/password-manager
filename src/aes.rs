pub mod aes {
    pub fn encrypt_string_to_bytes_aes(plain_text: &str, key: &str) -> () {
        if plain_text.to_string().len() == 0 {
            panic!("You must provide a string to encrypt!");
        }
    }

    pub fn decrypt_string_from_bytes_aes(plain_text: &str, key: &str) -> () {

    }
}
