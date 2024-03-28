from __future__ import annotations

import click

from plateaukit.cli.commands.config import config_cmd
from plateaukit.cli.commands.generate import (
    generate_cityjson_cmd,
    generate_geojson_cmd,
    generate_qmesh_cmd,
)
from plateaukit.cli.commands.info import info_cmd
from plateaukit.cli.commands.install import install_cmd, list_cmd, uninstall_cmd
from plateaukit.cli.commands.prebuild import prebuild_cmd
from plateaukit.logger import set_log_level


# https://alexdelorenzo.dev/notes/click.html
class OrderCommands(click.Group):
    def list_commands(self, ctx):
        return list(self.commands)


@click.group(
    cls=OrderCommands,
    context_settings=dict(help_option_names=["-h", "--help"], show_default=True),
    no_args_is_help=True,
)
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Enable verbose mode."
)
def cli(verbose):
    if verbose:
        set_log_level("DEBUG")


cli.add_command(list_cmd)
cli.add_command(install_cmd)
cli.add_command(uninstall_cmd)
cli.add_command(prebuild_cmd)
cli.add_command(generate_geojson_cmd)
cli.add_command(generate_cityjson_cmd)
cli.add_command(generate_qmesh_cmd)
cli.add_command(info_cmd)
cli.add_command(config_cmd)

if __name__ == "__main__":
    cli()
