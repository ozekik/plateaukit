from __future__ import annotations

import click

from plateaukit.config import Config


@click.command("config")
def config_cmd():
    """Show PlateauKit configuration information.

    PlateauKit の設定情報を表示します。
    """
    import importlib.metadata
    import json

    try:
        __version__ = importlib.metadata.version("plateaukit")
    except importlib.metadata.PackageNotFoundError:
        __version__ = "unknown"

    config = Config()
    click.echo(f"Version: {__version__}")
    click.echo(f"Config path: {config.path}")
    click.echo(f"Data directory: {config.data_dir}")
    click.echo(f"{json.dumps(config.datasets, indent=2, ensure_ascii=False)}")
