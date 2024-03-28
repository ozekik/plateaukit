from __future__ import annotations

import click

from plateaukit.prebuild import prebuild


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
    "--split", default=10, help="Split the output into specified number of files."
)
@click.option("-v", "is_verbose", is_flag=True, default=False, help="Verbose")
def prebuild_cmd(dataset_id, format, split, is_verbose):
    """Prebuild PLATEAU datasets.

    PLATEAU データセットを事前ビルドします。
    """

    prebuild(
        dataset_id,
        format=format,
        split=split,
        simple_output=False if is_verbose else True,
    )
