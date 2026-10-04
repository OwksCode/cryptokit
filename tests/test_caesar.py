"""tests for the caesar module"""

from crypto.caesar import encrypt, decrypt, crack, _count_frequencies


class TestEncrypt:
    def test_basic_shift(self):
        assert encrypt("abc", 3) == "def"

    def test_wraps_around(self):
        assert encrypt("xyz", 3) == "abc"

    def test_keeps_case(self):
        assert encrypt("Hello", 3) == "Khoor"

    def test_ignores_non_alpha(self):
        assert encrypt("Hello, World! 123", 3) == "Khoor, Zruog! 123"

    def test_zero_key(self):
        assert encrypt("test", 0) == "test"

    def test_full_rotation(self):
        assert encrypt("test", 26) == "test"

    def test_known_phrase(self):
        assert encrypt("attack at dawn", 5) == "fyyfhp fy ifbs"


class TestDecrypt:
    def test_basic(self):
        assert decrypt("def", 3) == "abc"

    def test_roundtrip(self):
        msg = "The quick brown fox jumps over 13 lazy dogs!"
        for k in range(26):
            assert decrypt(encrypt(msg, k), k) == msg


class TestCrack:
    def test_finds_correct_key_french(self):
        original = "la cryptographie est la science du secret"
        key = 7
        encrypted = encrypt(original, key)
        results = crack(encrypted, lang="fr")
        assert results[0]["key"] == key

    def test_returns_26_results(self):
        assert len(crack("whatever")) == 26


class TestCountFrequencies:
    def test_even_split(self):
        freqs = _count_frequencies("aabb")
        assert freqs['a'] == 50.0
        assert freqs['b'] == 50.0

    def test_skips_non_alpha(self):
        freqs = _count_frequencies("a a a 123")
        assert freqs['a'] == 100.0