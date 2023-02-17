import atexit
import importlib.resources
import platform
import subprocess
from contextlib import ExitStack
from pathlib import Path

import click

CITYGML_TOOLS_VERSION = "2.0.0"
CITYGML_TOOLS_DIR = f"external/citygml-tools-{CITYGML_TOOLS_VERSION}"


def _get_citygml_tools_path():
    file_manager = ExitStack()
    atexit.register(file_manager.close)
    filename = (
        "citygml-tools.bat" if platform.system() == "Windows" else "citygml-tools"
    )
    ref = Path(
        importlib.resources.files("plateaukit").parent, CITYGML_TOOLS_DIR, filename
    )
    path = file_manager.enter_context(importlib.resources.as_file(ref))
    return str(path)


def cityjson_from_gml(infiles, vertex_precision=16):
    citygml_tools_path = _get_citygml_tools_path()
    args = [
        citygml_tools_path,
        "to-cityjson",
        f"--vertex-precision={vertex_precision}",
    ]
    args.extend(infiles)
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.echo(
            "STDOUT from citygml-tools:\n{}\n".format(e.stdout.decode("utf-8")),
            err=True,
        )
        click.echo(
            "STDERR from citygml-tools:\n{}\n".format(e.stderr.decode("utf-8")),
            err=True,
        )
        raise
    except:
        raise
