from __future__ import annotations

import click
from prettytable import PrettyTable

from plateaukit.config import Config
from plateaukit.installer import install_dataset, uninstall_dataset
from plateaukit.prebuild import prebuild


def list_available_datasets(is_all=False):
    from plateaukit.download import city_list

    table = PrettyTable()
    table.field_names = ["id", "name", "version", "spec", "homepage"]
    # table.add_row(["all", "(全都市)", "", ""])
    for city in city_list:
        if city.get("latest", False) or is_all:
            table.add_row(
                [
                    city["dataset_id"],
                    city["city_name"],
                    city["version"],
                    f"v{city['spec']}",
                    city["homepage"],
                ]
            )
    print(table)


@click.command("list")
@click.option(
    "--local", is_flag=True, default=False, help="Show installed datasets only."
)
@click.option(
    "--all",
    is_flag=True,
    default=False,
    help="Show all versions of datasets including old ones.",
)
def list_cmd(local, all):
    """List available and installed PLATEAU datasets.

    利用可能およびインストール済みのデータセットを表示します。
    """
    from plateaukit.download import city_list

    config = Config()

    if local:
        table = PrettyTable()
        table.field_names = ["id", "name", "homepage", "formats"]
        for dataset_id, record in config.datasets.items():
            city = next(
                filter(lambda x: x["dataset_id"] == dataset_id, city_list), None
            )
            if not city:
                continue
            table.add_row(
                [
                    dataset_id,
                    city["city_name"],
                    city["homepage"],
                    " ".join(
                        [x for x in ["citygml", "3dtiles", "gpkg"] if x in record]
                    ),
                ]
            )
        print(table)
        return
    else:
        list_available_datasets(is_all=all)
        return


@click.command("install")
@click.argument("dataset_id", nargs=1, required=False)
@click.option(
    "--format",
    type=click.Choice(["citygml", "3dtiles"], case_sensitive=False),
    default="citygml",
)
@click.option("--local", help="Install local file. (without copying)")
@click.option(
    "--prebuild", "run_prebuild", is_flag=True, default=True, help="Prebuild dataset."
)
@click.option("--force", is_flag=True, default=False, help="Force install.")
@click.option("--download-only", is_flag=True, default=False)
@click.option("-l", "--list", is_flag=True, help="List all latest available datasets.")
@click.option(
    "--list-all", is_flag=True, help="List all available datasets including old ones."
)
@click.option("-v", "is_verbose", is_flag=True, help="Verbose mode.")
def install_cmd(
    dataset_id,
    format,
    local,
    run_prebuild,
    force,
    download_only,
    list,
    list_all,
    is_verbose,
):
    """Download and install PLATEAU datasets.

    PLATEAU データセットをダウンロード・インストールします。
    """
    if not dataset_id and not (list or list_all):
        raise click.UsageError("Missing argument/option: dataset_id or -l/--list")

    if list or list_all:
        list_available_datasets(is_all=list_all)
        return

    if dataset_id:
        try:
            install_dataset(dataset_id, format=format, local=local, force=force)
        except Exception as e:
            raise click.UsageError(str(e))

    if run_prebuild and not download_only:
        prebuild(dataset_id, simple_output=False if is_verbose else True)


@click.command("uninstall")
@click.argument("dataset_id", nargs=1, required=False)
@click.option(
    "--format",
    "-f",
    "formats",
    type=click.Choice(
        ["citygml", "3dtiles", "gpkg"],
        case_sensitive=False,
    ),
    default=None,
    multiple=True,
)
@click.option("--keep-files", is_flag=True, default=False)
def uninstall_cmd(dataset_id, formats: list[str], keep_files):
    """Uninstall PLATEAU datasets.

    PLATEAU データセットをアンインストールします。
    """
    if not dataset_id:
        raise Exception("Missing argument")

    config = Config()
    formats = formats or list(config.datasets[dataset_id].keys())

    # TODO: Fix duplicated code in uninstall_dataset
    if not keep_files:
        paths = []
        for format in formats:
            path = config.datasets[dataset_id].get(format)
            if not path:
                raise RuntimeError(f"Missing files in record for '{format}'")
            paths.append(path)
        click.echo("Would remove:")
        for path in paths:
            click.echo(f"  {path}")
        if click.confirm("Proceed?"):
            uninstall_dataset(dataset_id, formats, keep_files=False)
    else:
        uninstall_dataset(dataset_id, formats, keep_files=True)
