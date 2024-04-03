from __future__ import annotations

import click
from rich.console import Console

from plateaukit.config import Config, _get_data_items


@click.command("info")
@click.argument("dataset_id", nargs=1, required=True)
def info_cmd(dataset_id):
    """Show PLATEAU dataset information.

    PLATEAU データセットの情報を表示します。
    """
    from plateaukit.download import city_list
    from plateaukit.formats.citygml import CityGMLDataset, constants

    config = Config()

    remote_info = next(filter(lambda x: x["dataset_id"] == dataset_id, city_list), None)

    if not remote_info:
        raise click.UsageError(f"Unknown dataset: {dataset_id}")

    console = Console(highlight=False)

    console.print(f"[b]{dataset_id}[/b]")
    console.print(f"[u]{remote_info['homepage']}")
    console.print(f"[b]Name:[/b] {remote_info['city_name']}")
    console.print(f"[b]Version:[/b] {remote_info['version']}")

    record = config.datasets.get(dataset_id, None)

    if not record:
        console.print("[b]Installed Files:[/b]\n  (None)")
        return

    # COMPAT: Default to v2
    spec_version = record.get("_spec", "2")
    if spec_version == "2":
        data_type_display_names = constants.data_type_display_names_v2
    elif spec_version == "3":
        data_type_display_names = constants.data_type_display_names_v3
    else:
        raise RuntimeError(f"Unknown spec version: {spec_version}")

    console.print(f"[b]PLATEAU CityGML Spec:[/b] v{spec_version}")

    console.print("[b]Installed Files:[/b]")
    for format, path in _get_data_items(record).items():
        console.print(f"  {format}: {path}")

    dataset = CityGMLDataset(dataset_id)
    udx_dirs = dataset.udx_dirs()

    console.print("[b]Data Types:[/b]")
    for udx_type, path in udx_dirs.items():
        type_name = data_type_display_names.get(udx_type, {}).get("ja", udx_type)
        console.print(f"  {type_name} ({udx_type}): {path}")

    console.print("[b]Attributes:[/b]")

    with console.status(
        "[bold]Processing...", spinner="simpleDotsScrolling"
    ) as _status:
        for udx_type in udx_dirs.keys():
            type_name = data_type_display_names.get(udx_type, {}).get("ja", udx_type)
            console.print(f"  [b]{type_name} ({udx_type}):[/b]")
            for attr in dataset.scan_attributes(udx_type):
                console.print(f"    {attr.get('name')} ({attr['tag']})")
