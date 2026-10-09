"""tests for the rsa module"""

import os
from crypto.rsa import (
    is_prime, generate_prime, gcd, mod_inverse,
    keygen, encrypt, decrypt, save_keys, load_key
)

PUB_FILE = "tests/test_pub.key"
PRIV_FILE = "tests/test_priv.key"


def teardown_module():
    for f in [PUB_FILE, PRIV_FILE]:
        if os.path.exists(f):
            os.remove(f)


class TestIsPrime:
    def test_small_primes(self):
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
            assert is_prime(p), f"{p} should be prime"

    def test_not_prime(self):
        for n in [0, 1, 4, 6, 8, 9, 15, 21, 100]:
            assert not is_prime(n), f"{n} should not be prime"

    def test_negative(self):
        assert not is_prime(-7)

    def test_larger_prime(self):
        assert is_prime(7919)

    def test_larger_composite(self):
        assert not is_prime(7917)  # 3 * 2639


class TestGeneratePrime:
    def test_is_actually_prime(self):
        for _ in range(10):
            p = generate_prime(16)
            assert is_prime(p)

    def test_correct_bit_length(self):
        p = generate_prime(16)
        assert p >= 2**15
        assert p < 2**16


class TestGcd:
    def test_basic(self):
        assert gcd(12, 8) == 4

    def test_coprime(self):
        assert gcd(17, 3120) == 1

    def test_same_number(self):
        assert gcd(7, 7) == 7

    def test_one_is_zero(self):
        assert gcd(5, 0) == 5


class TestModInverse:
    def test_known_value(self):
        d = mod_inverse(17, 3120)
        assert (d * 17) % 3120 == 1

    def test_common_e(self):
        # e=65537 with a typical phi
        phi = 3120
        if gcd(65537, phi) == 1:
            d = mod_inverse(65537, phi)
            assert (d * 65537) % phi == 1

    def test_not_coprime_raises(self):
        try:
            mod_inverse(6, 12)
            assert False, "should have raised ValueError"
        except ValueError:
            pass


class TestKeygen:
    def test_keys_share_n(self):
        pub, priv = keygen()
        assert pub["n"] == priv["n"]

    def test_keys_have_right_fields(self):
        pub, priv = keygen()
        assert "n" in pub and "e" in pub
        assert "n" in priv and "d" in priv

    def test_e_and_d_are_inverses(self):
        pub, priv = keygen()
        p_q_product = pub["n"]
        # we can't easily get phi back, but we can test via encrypt/decrypt
        for char in "ABCxyz019":
            m = ord(char)
            c = pow(m, pub["e"], pub["n"])
            assert pow(c, priv["d"], priv["n"]) == m


class TestEncryptDecrypt:
    def test_roundtrip_short(self):
        pub, priv = keygen()
        msg = "Hello"
        assert decrypt(encrypt(msg, pub), priv) == msg

    def test_roundtrip_with_special_chars(self):
        pub, priv = keygen()
        msg = "test @#$! 123"
        assert decrypt(encrypt(msg, pub), priv) == msg

    def test_encrypt_returns_list_of_ints(self):
        pub, priv = keygen()
        result = encrypt("AB", pub)
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(x, int) for x in result)

    def test_empty_string(self):
        pub, priv = keygen()
        assert decrypt(encrypt("", pub), priv) == ""


class TestSaveLoadKeys:
    def test_save_and_load_roundtrip(self):
        pub, priv = keygen()
        save_keys(pub, priv, PUB_FILE, PRIV_FILE)

        loaded_pub = load_key(PUB_FILE)
        loaded_priv = load_key(PRIV_FILE)

        assert loaded_pub["n"] == pub["n"]
        assert loaded_priv["n"] == priv["n"]