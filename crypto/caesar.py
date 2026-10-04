"""
Caesar cipher — encrypt, decrypt, and crack by frequency analysis.

Shifts every letter in the alphabet by a fixed number of positions.
With key=3: A->D, B->E, C->F, etc. Simplest cipher there is,
but a good starting point before moving on to Vigenere.
"""

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# letter frequencies (%) — used for cracking
# grabbed these from wikipedia, close enough for our purposes

FREQ_FR = {
    'a': 8.11, 'b': 0.81, 'c': 3.38, 'd': 3.69, 'e': 17.26, 'f': 1.12,
    'g': 1.23, 'h': 0.74, 'i': 7.31, 'j': 0.18, 'k': 0.02, 'l': 5.99,
    'm': 2.29, 'n': 7.68, 'o': 5.28, 'p': 2.92, 'q': 0.83, 'r': 6.43,
    's': 8.87, 't': 7.44, 'u': 5.23, 'v': 1.28, 'w': 0.06, 'x': 0.53,
    'y': 0.26, 'z': 0.12
}

FREQ_EN = {
    'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70, 'f': 2.23,
    'g': 2.02, 'h': 6.09, 'i': 6.97, 'j': 0.15, 'k': 0.77, 'l': 4.03,
    'm': 2.41, 'n': 6.75, 'o': 7.51, 'p': 1.93, 'q': 0.10, 'r': 5.99,
    's': 6.33, 't': 9.06, 'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15,
    'y': 1.97, 'z': 0.07
}


def encrypt(plaintext: str, key: int) -> str:
    result = ""
    for char in plaintext:
        if char.islower():
            result += chr((ord(char) - 97 + key) % 26 + 97)
        elif char.isupper():
            result += chr((ord(char) - 65 + key) % 26 + 65)
        else:
            result += char
    return result

def decrypt(ciphertext: str, key: int) -> str:
    return encrypt(ciphertext, -key)

def crack(ciphertext: str, lang: str = "fr") -> list[dict]:
    freq_table = FREQ_FR if lang == "fr" else FREQ_EN
    guesses = []

    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        freq = _count_frequencies(plaintext)

        chi2 = 0
        for letter in ALPHABET:
            observed = freq.get(letter, 0)
            expected = freq_table[letter]
            if expected > 0:
                chi2 += (observed - expected) ** 2 / expected

        guesses.append({
            "key": key,
            "score": chi2,
            "preview": plaintext[:30]
        })

    guesses.sort(key=lambda g: g["score"])
    return guesses

def _count_frequencies(text: str) -> dict[str, float]:
    counts = {}
    total = 0

    for char in text:
        if char.isalpha():
            lower = char.lower()
            counts[lower] = counts.get(lower, 0) + 1
            total += 1

    if total == 0:
        return {}

    return {letter: count / total * 100 for letter, count in counts.items()}