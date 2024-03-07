import subprocess
import sys
import unittest


class CLITest(unittest.TestCase):
    def test_cli(self):
        if sys.platform == "win32":
            cp = subprocess.run("tests\\test_cli.bat", shell=True)
        else:
            cp = subprocess.run("tests/test_cli.sh", shell=True)

        self.assertEqual(cp.returncode, 0)


if __name__ == "__main__":
    unittest.main()
