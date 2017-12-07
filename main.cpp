#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <ctime>
#include <cstdlib>
#include <cmath>
#include <utility>
using namespace std;

struct PublicKey {
    unsigned int e;
    unsigned int n;
};

struct PrivateKey {
    unsigned int d;
    unsigned int n;
};

char* get_os();
pair<PublicKey, PrivateKey> generate_RSA_keys();
bool is_prime(int);
bool relatively_prime(int, int);
int gcd(int, int);

int main(int argc, char* argv[]) {
    if (argc == 1) {
        
    }

    for (;;) {
        const int c = getopt(argc, argv, "g:f:l:c:");
        if (c == -1) {
            break;
        }

        const char command = static_cast<char>(c);

        switch (command) {
            case 'g':
                //const char* argument = argv[argc - 1];

                break;
            case 'f':
                //const char* argument = argv[argc - 1];
                break;
            case 'l':
                break;
            case 'c':
                break;
            default:
                break;
        }
    }
}

char* get_os() {
    #ifdef _WIN32
        return "Windows";
    #elif _WIN64
        return "Windows";
    #elif __unix || __unix__
        return "Unix";
    #elif __APPLE__ || __MACH__
        return "Mac OSX";
    #elif __linux__
        return "Linux";
    #elif __FreeBSD__
        return "FreeBSD";
    #endif
}

pair<PublicKey, PrivateKey> generate_RSA_keys() {
    srand(static_cast<int>(time(NULL)));

    // RSA
    // Generate 2 prime numbers `p`, `q`
    unsigned int p = rand() % 1 + 30;
    unsigned int q = rand() % 1 + 30;
    
    if (!is_prime(p)) {
        while (!is_prime(p)) {
            p = rand() % 1 + 30;

            if (is_prime(p)) {
                break;
            }
        }
    }

    if (!is_prime(q)) {
        while (!is_prime(q)) {
            q = rand() % 1 + 30;

            if (is_prime(q)) {
                break;
            }
        }
    }

    // Calculate module n = p * q
    const unsigned int n = p * q;

    // Calculate Euler function
    const unsigned int euler = (p - 1) * (q - 1);

    // Calculate open exponent `e`
    // should be in then interval 1 < e < ϕ(n)
    // and also be relatively prime to the value φ (n)
    unsigned int e = rand() % 1 + 999;

    if (!relatively_prime(e, euler) || e > euler) {
        while (!relatively_prime(e, euler) && e > euler) {
            e = rand() % 1 + 999;

            if (relatively_prime(e, euler) && e < euler) {
                break;
            }
        }
    }

    // Calculate secret exponent `d`
    unsigned int d = rand() % 1 + 999;

    if ((d * e) % euler != 1) {
        while ((d * e) % euler != 1) {
            d = rand() % 1 + 999;

            if ((d * e) % euler == 1) {
                break;
            }
        }
    }

    // Pair (e, n) - public key, (d, n) - private

    PublicKey public_key;
    public_key.e = e;
    public_key.n = n;

    PrivateKey private_key;
    private_key.d = d;
    private_key.n = n;

    return make_pair(public_key, private_key);
}

bool is_prime(int number) {
    if (number == 1) {
        return false; // Special case: 1 is not a prime
    }

    if (number == 2) {
        return true; // Special case: 2 is the only even prime
    }

    if (number % 2 == 0) {
        return false; // All other even numbers are not prime
    }

    const int range = static_cast<int>(floor(sqrt(number)));
    for (unsigned int i = 3; i <= range; i += 3) {
        if (number % i == 0) {
            return false; // Found a divisor; candidate is not a prime
        }
    }

    return true;
}

bool relatively_prime(int a, int b) {
    return gcd(a, b) == 1;
}

int gcd(int a, int b) {
    int t;

    while (b != 0) {
        t = a;
        a = b;
        b = t % b;
    }

    return a;
}
