extern crate rand;

use std::f64;

pub mod rsa {
    pub use rand::Rng;

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

    pub fn generate_RSA_keys() -> (PublicKey, PrivateKey) {
        // RSA
        // Generate 2 prime numbers `p`, `q`
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

        // Calculate module n = p * q
        let n: u64 = p * q;

        // Calculate Euler function
        let euler: u64 = (p - 1) * (q - 1);

        // Calculate open exponent `e`
        // should be in then interval 1 < e < ϕ(n)
        // and also be relatively prime to the value φ (n)
        let mut e: u64 = rand::thread_rng().gen_range(1, 999);

        if !relatively_prime(e, euler) || e > euler {
            while !relatively_prime(e, euler) && e > euler {
                e = rand::thread_rng().gen_range(1, 999);

                if relatively_prime(e, euler) && e < euler {
                    break;
                }
            }
        }

        // Calculate secret exponent `d`
        let mut d: u64 = rand::thread_rng().gen_range(1, 999);

        if (d * e) % euler != 1 {
            while (d * e) % euler != 1 {
                d = rand::thread_rng().gen_range(1, 999);

                if (d * e) % euler == 1 {
                    break;
                }
            }
        }

        // Pair (e, n) - public key, (d, n) - private

        (PublicKey::new(&e, &n), PrivateKey::new(&d, &n))
    }

    pub fn is_prime(number: u64) -> bool {
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

    pub fn relatively_prime(a: u64, b: u64) -> bool {
        gcd(a, b) == 1
    }

    pub fn gcd(mut a: u64, mut b: u64) -> u64 {
        let mut t: u64;

        while b != 0 {
            t = a;
            a = b;
            b = t % b;
        }

        a
    }
}
