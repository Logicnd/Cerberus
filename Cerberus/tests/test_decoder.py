import unittest
import os
import sys
base_dir = os.path.dirname(os.path.abspath(__file__))
pkg_dir = os.path.abspath(os.path.join(base_dir, ".."))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
from codeintel.decoder import Decoder


class TestDecoder(unittest.TestCase):
    def test_hex(self):
        d = Decoder()
        out = d.hex_decode("68656c6c6f")
        self.assertIn("hello", out)

    def test_base64(self):
        d = Decoder()
        out = d.base64_decode("aGVsbG8=")
        self.assertIn("hello", out)

    def test_rot13(self):
        d = Decoder()
        out = d.rot13("uryyb")
        self.assertEqual(out, "hello")

    def test_xor(self):
        d = Decoder()
        enc = "".join(chr(ord(c) ^ ord("k")) for c in "data")
        out = d.xor_decode(enc, "k")
        self.assertEqual(out, "data")


if __name__ == "__main__":
    unittest.main()
