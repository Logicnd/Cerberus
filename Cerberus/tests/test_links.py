import unittest
import os
import sys
base_dir = os.path.dirname(os.path.abspath(__file__))
pkg_dir = os.path.abspath(os.path.join(base_dir, ".."))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
from codeintel.links import LinkFinder


class TestLinks(unittest.TestCase):
    def test_urls(self):
        lf = LinkFinder()
        data = lf.find("fetch('https://example.com/api/v1') // 10.0.0.1")
        self.assertTrue(data["urls"])
        self.assertTrue(data["api_paths"])
        self.assertTrue(data["ips"])


if __name__ == "__main__":
    unittest.main()
