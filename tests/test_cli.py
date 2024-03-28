import subprocess
import sys
import unittest

from click.testing import CliRunner

from plateaukit.cli.cli import cli


class CLITest(unittest.TestCase):
    def test_shell_cli(self):
        if sys.platform == "win32":
            cp = subprocess.run("tests\\test_cli.bat", shell=True)
        else:
            cp = subprocess.run("tests/test_cli.sh", shell=True)

        self.assertEqual(cp.returncode, 0)

    def test_list(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        # assert "..." in result.output

    def test_config(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0

    def test_info(self):
        runner = CliRunner()
        # TODO: Installed case

        # Case for datasets not installed
        result = runner.invoke(cli, ["info", "plateau-28225-asago-shi-2022"])
        assert result.exit_code == 0


if __name__ == "__main__":
    unittest.main()
