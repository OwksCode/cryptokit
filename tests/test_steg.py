"""tests for the lsb steganography module"""

import os
from PIL import Image
from steg.lsb import hide, reveal, _text_to_bits, _bits_to_text

TEST_IMG = "tests/test_image.png"
TEST_OUT = "tests/test_output.png"


def _make_test_image(width=100, height=100, color=(128, 128, 128)):
    """create a simple solid-color test image"""
    img = Image.new("RGB", (width, height), color)
    img.save(TEST_IMG)


def teardown_module():
    """clean up test images after all tests run"""
    for f in [TEST_IMG, TEST_OUT]:
        if os.path.exists(f):
            os.remove(f)


class TestBitConversion:
    def test_text_to_bits(self):
        assert _text_to_bits("A") == "01000001"

    def test_bits_to_text(self):
        assert _bits_to_text("01000001") == "A"

    def test_roundtrip(self):
        msg = "Hello, world!"
        assert _bits_to_text(_text_to_bits(msg)) == msg

    def test_empty_string(self):
        assert _text_to_bits("") == ""
        assert _bits_to_text("") == ""


class TestHideAndReveal:
    def test_basic_roundtrip(self):
        _make_test_image()
        msg = "secret message"
        hide(TEST_IMG, msg, TEST_OUT)
        assert reveal(TEST_OUT) == msg

    def test_with_special_chars(self):
        _make_test_image()
        msg = "hello! @#$% 12345"
        hide(TEST_IMG, msg, TEST_OUT)
        assert reveal(TEST_OUT) == msg

    def test_image_too_small(self):
        _make_test_image(width=1, height=1)  # only 3 bits of capacity
        try:
            hide(TEST_IMG, "this message is way too long", TEST_OUT)
            assert False, "should have raised ValueError"
        except ValueError:
            pass

    def test_no_hidden_message(self):
        _make_test_image()
        try:
            reveal(TEST_IMG)
            assert False, "should have raised ValueError"
        except ValueError:
            pass

    def test_image_looks_the_same(self):
        """pixel values should change by at most 1"""
        _make_test_image()
        hide(TEST_IMG, "test", TEST_OUT)
        original = list(Image.open(TEST_IMG).get_flattened_data())
        modified = list(Image.open(TEST_OUT).get_flattened_data())
        for orig_px, mod_px in zip(original, modified):
            for o, m in zip(orig_px, mod_px):
                assert abs(o - m) <= 1