from __future__ import annotations

from plateaukit.cli.base import cli
from plateaukit.cli.commands.config import config_cmd
from plateaukit.cli.commands.export import (
    export_cityjson_cmd,
    export_geojson_cmd,
    export_qmesh_cmd,
)
from plateaukit.cli.commands.info import info_cmd
from plateaukit.cli.commands.install import install_cmd, list_cmd, uninstall_cmd
from plateaukit.cli.commands.prebuild import prebuild_cmd

cli.add_command(list_cmd)
cli.add_command(install_cmd)
cli.add_command(uninstall_cmd)
cli.add_command(prebuild_cmd)
cli.add_command(export_geojson_cmd)
cli.add_command(export_cityjson_cmd)
cli.add_command(export_qmesh_cmd)
cli.add_command(info_cmd)
cli.add_command(config_cmd)

if __name__ == "__main__":
    cli()
