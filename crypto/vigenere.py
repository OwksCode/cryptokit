"""
Vigenere cipher.
Like Caesar but the shift changes for each letter based on a keyword.
"""

def encrypt(plaintext: str, key: str) -> str:
    result = ""
    ki = 0
    for char in plaintext:
        shift = ord(key[ki % len(key)].lower()) - 97
        if char.islower():
            result += chr((ord(char) - 97 + shift) % 26 + 97)
            ki += 1
        elif char.isupper():
            result += chr((ord(char) - 65 + shift) % 26 + 65)
            ki += 1
        else:
            result += char
    return result


def decrypt(ciphertext: str, key: str) -> str:
    result = ""
    ki = 0
    for char in ciphertext:
        shift = ord(key[ki % len(key)].lower()) - 97
        if char.islower():
            result += chr((ord(char) - 97 - shift) % 26 + 97)
            ki += 1
        elif char.isupper():
            result += chr((ord(char) - 65 - shift) % 26 + 65)
            ki += 1
        else:
            result += char
    return result