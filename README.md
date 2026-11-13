# cryptokit

CLI tool for classical cryptography and image steganography, built from scratch in Python. No external crypto libs — everything is hand-rolled.

![tests](https://github.com/OwksCode/nbody/actions/workflows/tests.yml/badge.svg)

## what it does

- **Caesar & Vigenère ciphers** — encrypt, decrypt them and crack Caesar with frequency analysis
- **LSB steganography** — hide text messages inside PNG images
- **RSA from scratch** — key generation, encrypt/decrypt using raw modular arithmetic

<img width="1204" height="317" alt="cryptokit-demo" src="https://github.com/user-attachments/assets/d0dc74e5-c6a8-4f96-a1d3-80b8b3a34560" />

## setup

```bash
git clone https://github.com/OwksCode/cryptokit.git
cd cryptokit
pip install -r requirements.txt
```

## usage

```bash
# caesar
python cryptokit.py caesar --encrypt "some secret message" --key 13
python cryptokit.py caesar --decrypt "fbzr frperg zrffntr" --key 13
python cryptokit.py crack-caesar "fbzr frperg zrffntr"

# vigenere
python cryptokit.py vigenere --encrypt "some secret message" --key "password"
python cryptokit.py vigenere --decrypt "..." --key "password"

# steganography
python cryptokit.py steg-hide --image input.png --message "hidden msg" --output out.png
python cryptokit.py steg-reveal --image out.png

# steganography + encryption (vigenere before hiding)
python cryptokit.py steg-hide --image input.png --message "secret" --key "pass" --output out.png
python cryptokit.py steg-reveal --image out.png --key "pass"

# steganography + encryption (RSA before hiding)
python cryptokit.py rsa-keygen
python cryptokit.py steg-hide --image input.png --message "secret" --rsa-key rsa.pub --output out.png
python cryptokit.py steg-reveal --image out.png --rsa-key rsa.priv

# rsa
python cryptokit.py rsa-keygen
python cryptokit.py rsa-keygen --bits 32
python cryptokit.py rsa-encrypt --pubkey rsa.pub --message "hello"
python cryptokit.py rsa-decrypt --privkey rsa.priv --encrypted "2081,1351,977,977,2627"
```

## running tests

```bash
python -m pytest tests/ -v
```

## project structure

```
cryptokit/
├── cryptokit.py        # cli entry point
├── crypto/
│   ├── caesar.py       # caesar cipher + frequency cracking
│   ├── vigenere.py     # vigenere cipher
│   └── rsa.py          # rsa from scratch
├── steg/
│   └── lsb.py          # least significant bit steganography
└── tests/
    ├── test_caesar.py
    ├── test_vigenere.py
    ├── test_steg.py
    └── test_rsa.py
```

## security notes

This is an educational project: don't use it to protect real data.

- **Textbook RSA, one character at a time, no padding.** Encryption is deterministic, so anyone with the public key can encrypt every possible character, build a lookup table and decrypt without the private key. Real-world RSA uses OAEP padding.
- **Tiny keys.** Primality is tested by trial division, which only works for small primes (16 bits by default), so the modulus can be factored instantly.
- **`random` is not a CSPRNG.** Key generation should use `secrets`.
- **LSB steganography is detectable** with statistical steganalysis and doesn't survive lossy compression (JPEG).

## license

MIT
