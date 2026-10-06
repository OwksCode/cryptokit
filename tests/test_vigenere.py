"""tests for the vigenere module"""

from crypto.vigenere import encrypt, decrypt


class TestEncrypt:
    def test_basic(self):
        assert encrypt("hello", "abc") == "hfnlp"

    def test_single_char_key(self):
        # key "d" = shift of 3, should behave like caesar with key 3
        assert encrypt("hello", "d") == "khoor"

    def test_keeps_case(self):
        assert encrypt("Hello", "abc") == "Hfnlp"

    def test_ignores_non_alpha(self):
        # key index should NOT advance on spaces/punctuation
        assert encrypt("hi there!", "abc") == "hj vhfte!"

    def test_key_longer_than_message(self):
        assert encrypt("hi", "abcdef") == "hj"

    def test_key_wraps(self):
        # "abc" repeats: a,b,c,a,b,c,a...
        assert encrypt("aaaaaaa", "abc") == "abcabca"


class TestDecrypt:
    def test_basic(self):
        assert decrypt("hfnlp", "abc") == "hello"

    def test_roundtrip(self):
        msg = "The quick brown fox jumps over 13 lazy dogs!"
        for key in ["secret", "a", "xyz", "longerkeyword"]:
            assert decrypt(encrypt(msg, key), key) == msg

    def test_keeps_non_alpha(self):
        msg = "hello, world! 42"
        assert decrypt(encrypt(msg, "key"), "key") == msg