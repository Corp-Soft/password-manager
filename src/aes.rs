extern crate rand;
extern crate crypto;

use self::rand::{ OsRng, Rng };

use self::crypto::{ symmetriccipher, buffer, aes, blockmodes };
use self::crypto::buffer::{ ReadBuffer, WriteBuffer, BufferResult };

use std::str;
use std::io;
use std::mem;

fn string_to_static_str(s: String) -> &'static str {
    unsafe {
        let ret = mem::transmute(&s as &str);
        mem::forget(s);
        ret
    }
}

pub fn test() -> () {
    println!("Введите строку для шифрования: ");

    let mut s: String = String::new();
    io::stdin().read_line(&mut s).expect("Cannot read line");
    let message: &'static str = string_to_static_str(s);


    let mut key: [u8; 32] = [0; 32];
    let mut iv: [u8; 16] = [0; 16];

    let mut rng = OsRng::new().ok().unwrap();

    rng.fill_bytes(&mut key);
    rng.fill_bytes(&mut iv);

    let encrypted_data: Vec<u8> = encrypt(message.as_bytes(), &key, &iv).ok().unwrap();
    let decrypted_data: Vec<u8> = decrypt(&encrypted_data[..], &key, &iv).ok().unwrap();
    println!("Расшифровал: {}", str::from_utf8(&decrypted_data).unwrap());
}

fn encrypt(data: &[u8], key: &[u8], iv: &[u8]) -> Result<Vec<u8>, symmetriccipher::SymmetricCipherError> {
    let mut encryptor = aes::cbc_encryptor(
            aes::KeySize::KeySize256,
            key,
            iv,
            blockmodes::PkcsPadding);

    let mut final_result = Vec::<u8>::new();
    let mut read_buffer = buffer::RefReadBuffer::new(data);
    let mut buffer = [0; 4096];
    let mut write_buffer = buffer::RefWriteBuffer::new(&mut buffer);

    loop {
        let result = try!(encryptor.encrypt(&mut read_buffer, &mut write_buffer, true));

        final_result.extend(write_buffer.take_read_buffer().take_remaining().iter().map(|&i| i));

        match result {
            BufferResult::BufferUnderflow => break,
            BufferResult::BufferOverflow => {}
        }
    }

    Ok(final_result)
}

fn decrypt(encrypted_data: &[u8], key: &[u8], iv: &[u8]) -> Result<Vec<u8>, symmetriccipher::SymmetricCipherError> {
    let mut decryptor = aes::cbc_decryptor(
            aes::KeySize::KeySize256,
            key,
            iv,
            blockmodes::PkcsPadding);

    let mut final_result = Vec::<u8>::new();
    let mut read_buffer = buffer::RefReadBuffer::new(encrypted_data);
    let mut buffer = [0; 4096];
    let mut write_buffer = buffer::RefWriteBuffer::new(&mut buffer);

    loop {
        let result = try!(decryptor.decrypt(&mut read_buffer, &mut write_buffer, true));
        final_result.extend(write_buffer.take_read_buffer().take_remaining().iter().map(|&i| i));
        match result {
            BufferResult::BufferUnderflow => break,
            BufferResult::BufferOverflow => { }
        }
    }

    Ok(final_result)
}
