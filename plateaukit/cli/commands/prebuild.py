from __future__ import annotations

import click

from plateaukit.prebuild import prebuild
from plateaukit.logger import set_log_level


@click.command("prebuild")
@click.argument("dataset_id", nargs=1, required=True)
@click.option(
    "--format",
    type=click.Choice(
        ["parquet", "gpkg"],
        case_sensitive=False,
    ),
    default="parquet",
    help="Internal output format.",
)
@click.option(
    "--type",
    "-t",
    "types",
    type=click.Choice(
        ["bldg", "brid", "tran"],
        case_sensitive=True,
    ),
    default=["bldg"],
    multiple=True,
)
@click.option(
    "--split", default=10, help="Split the output into specified number of files."
)
@click.option("-v", "verbose", count=True, default=0, help="Verbose")
def prebuild_cmd(dataset_id: str, format, types: list[str], split: int, verbose: int):
    """Prebuild PLATEAU datasets.

    PLATEAU データセットを事前ビルドします。
    """

    if verbose >= 2:
        set_log_level("DEBUG")

    prebuild(
        dataset_id,
        format=format,
        types=types,
        split=split,
        simple_output=False if verbose else True,
    )
