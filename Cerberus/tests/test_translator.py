import unittest
import os
import sys
base_dir = os.path.dirname(os.path.abspath(__file__))
pkg_dir = os.path.abspath(os.path.join(base_dir, ".."))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
from codeintel.translator import Translator


class TestTranslator(unittest.TestCase):
    def test_py_to_html(self):
        t = Translator()
        out = t.translate("def foo(a, b):\n  return a+b\n", "python", "html")
        self.assertIn("<strong>foo</strong>", out)

    def test_py_to_js(self):
        t = Translator()
        out = t.translate("def bar(x):\n  pass\n", "python", "javascript")
        self.assertIn("function bar(x)", out)


if __name__ == "__main__":
    unittest.main()
