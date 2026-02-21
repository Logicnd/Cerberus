import unittest
import os
import sys
base_dir = os.path.dirname(os.path.abspath(__file__))
pkg_dir = os.path.abspath(os.path.join(base_dir, ".."))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
from codeintel.analysis import Analyzer


class TestAnalysis(unittest.TestCase):
    def test_python_analysis(self):
        code = "import os\nfrom sys import argv\nif True:\n  pass\n"
        a = Analyzer()
        out = a.static_analysis(code, "python")
        self.assertIn("dependencies", out)
        self.assertTrue(out["dependencies"])
        self.assertIn("complexity", out)
        self.assertIn("vulnerabilities", out)


if __name__ == "__main__":
    unittest.main()
