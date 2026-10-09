"""
RSA from scratch — keygen, encrypt, decrypt.
No external crypto libs, just modular arithmetic and prime numbers.

Keys are dicts:
  public  = {"n": ..., "e": ...}
  private = {"n": ..., "d": ...}
"""

import random
import math

# --- math helpers ---

def is_prime(n: int) -> bool:
    if n == 2:
        return True
    if n < 2 or n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_prime(bits: int = 16) -> int:
    n = random.randint(2**(bits - 1), 2**bits - 1)
    if n % 2 == 0:
        n += 1
    while not is_prime(n):
        n += 2
    return n


def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(e: int, phi: int) -> int:
    old_r, r = phi, e
    old_s, s = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s

    if old_r != 1:
        raise ValueError("not coprime")
    return old_s % phi

# --- RSA core ---

def keygen(bits: int = 16) -> tuple[dict, dict]:
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    for e in [65537, 17, 3]:
        if gcd(e, phi) == 1:
            break

    d = mod_inverse(e, phi)
    return ({"n": n, "e": e}, {"n": n, "d": d})


def encrypt(plaintext: str, public_key: dict) -> list[int]:
    encrypted = []
    for char in plaintext:
        encrypted.append(pow(ord(char), public_key["e"], public_key["n"]))
    return encrypted


def decrypt(ciphertext: list[int], private_key: dict) -> str:
    result = ""
    for number in ciphertext:
        result += chr(pow(number, private_key["d"], private_key["n"]))
    return result


def save_keys(public_key: dict, private_key: dict, pub_path: str, priv_path: str) -> None:
    with open(pub_path, "w") as f:
        f.write(f"{public_key['n']}\n{public_key['e']}")
    with open(priv_path, "w") as f:
        f.write(f"{private_key['n']}\n{private_key['d']}")


def load_key(path: str) -> dict:
    with open(path) as f:
        lines = f.read().split("\n")
    return {"n": int(lines[0]), "value": int(lines[1])}