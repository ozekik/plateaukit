from __future__ import annotations

import click
from prettytable import PrettyTable
from rich.console import Console

from plateaukit import generators
from plateaukit.config import Config
from plateaukit.core.dataset import load_dataset
from plateaukit.installer import install_dataset, uninstall_dataset
from plateaukit.logger import logger, set_log_level
from plateaukit.prebuild import prebuild


def list_available_datasets(is_all=False):
    from plateaukit.download import city_list

    table = PrettyTable()
    table.field_names = ["id", "name", "version", "homepage"]
    table.add_row(["all", "(全都市)", "", ""])
    for city in city_list:
        if city.get("latest", False) or is_all:
            table.add_row(
                [
                    city["dataset_id"],
                    city["city_name"],
                    city["version"],
                    city["homepage"],
                ]
            )
    print(table)


# https://alexdelorenzo.dev/notes/click.html
class OrderCommands(click.Group):
    def list_commands(self, ctx):
        return list(self.commands)


@click.group(
    cls=OrderCommands,
    context_settings=dict(help_option_names=["-h", "--help"]),
    no_args_is_help=True,
)
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Enable verbose mode."
)
def cli(verbose):
    if verbose:
        set_log_level("DEBUG")


@cli.command("list")
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


@cli.command("install")
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


@cli.command("uninstall")
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


@cli.command("prebuild")
@click.argument("dataset_id", nargs=1, required=True)
@click.option(
    "--split", default=10, help="Split the output into specified number of files"
)
@click.option("-v", "is_verbose", is_flag=True, default=False, help="Verbose")
def prebuild_cmd(dataset_id, split, is_verbose):
    """Prebuild PLATEAU datasets.

    PLATEAU データセットを事前ビルドします。
    """

    prebuild(dataset_id, split=split, simple_output=False if is_verbose else True)


@cli.command("generate-cityjson")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
@click.option("--dataset", "dataset_id", help='Dataset ID (e.g. "plateau-tokyo23ku")')
@click.option(
    "--type",
    "-t",
    "types",
    type=click.Choice(
        ["bldg", "brid", "dem", "fld", "frn", "lsld", "luse", "tran", "urf"],
        case_sensitive=True,
    ),
    default=["bldg"],
    multiple=True,
)
@click.option(
    "--split", default=1, help="Split the output into specified number of files"
)
@click.option(
    "--ground", is_flag=True, default=False, help="Shift objects to the ground level"
)
@click.option(
    "--target-epsg", default=None, help="EPSG code for the output CityJSON file"
)
# # @click.option(
# #     "--precision",
# #     help="Number of decimal places to keep for geometry vertices (default: 16).",
# )
def generate_cityjson(infiles, outfile, dataset_id, types, split, ground, target_epsg):
    """Generate CityJSON from PLATEAU datasets.

    PLATEAU データセットから CityJSON を生成します。
    """

    if not infiles and not dataset_id:
        raise click.UsageError("Missing argument/option: infiles or --dataset")

    if infiles and dataset_id:
        raise click.UsageError("Too many argument")

    params = {}

    # if precision:
    #     params["precision"] = precision

    # obj_types_map = {
    #     "bldg": ["Building"],
    #     "brid": ["Bridge"],
    #     "tran": ["Road"],
    #     # "dem": ["ReliefFeature"],
    #     # "fld": ["LandUse"],
    #     # "frn": ["WaterBody"],
    #     # "lsld": ["TransportationComplex"],
    #     # "luse": ["LandUse"],
    #     # "urf": ["CityFurniture"],
    # }

    # obj_types = sum([obj_types_map[type] for type in types], [])
    # logger.debug(obj_types)

    if dataset_id:
        dataset = load_dataset(dataset_id)
        dataset.to_cityjson(
            outfile,
            types=types,
            split=split,
            ground=ground,
            target_epsg=target_epsg,
            **params,
        )

    else:
        generators.cityjson.cityjson_from_citygml(infiles, outfile, **params)


def _generate_geojson(
    infiles, outfile, dataset_id: str, types: list[str], split: int, **kwargs
):
    """Generate GeoJSON from PLATEAU datasets."""

    if not infiles and not dataset_id:
        raise click.UsageError("Missing argument: infiles or dataset")

    if infiles and dataset_id:
        raise click.UsageError("Too many arguments")

    if dataset_id:
        dataset = load_dataset(dataset_id)
        dataset.to_geojson(outfile, types=types, split=split, **kwargs)
    else:
        generators.geojson.geojson_from_citygml(
            infiles, outfile, types=types, split=split, **kwargs
        )


@cli.command("generate-geojson")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
@click.option("--dataset", "dataset_id", help='Dataset ID (e.g. "plateau-tokyo23ku")')
@click.option(
    "--type",
    "-t",
    "types",
    type=click.Choice(
        ["bldg", "brid", "dem", "fld", "frn", "lsld", "luse", "tran", "urf"],
        case_sensitive=True,
    ),
    default=["bldg"],
    multiple=True,
)
@click.option("--split", default=1)
def generate_geojson(infiles, outfile, dataset_id: str, types: list[str], split: int):
    """Generate GeoJSON from PLATEAU datasets.

    PLATEAU データセットから GeoJSON を生成します。
    """

    _generate_geojson(infiles, outfile, dataset_id, types=types, split=split)


@cli.command("generate-qmesh")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
def generate_qmesh(infiles, outfile):
    """Generate Quantized Mesh from PLATEAU datasets. (Requires `pip install 'plateaukit[quantized_mesh]'`)

    PLATEAU データセットから Quantized Mesh を生成します。(要 `pip install 'plateaukit[quantized_mesh]'`)
    """

    generators.triangles_from_gml(infiles)


# @cli.command("generate-gpkg")
# @click.argument("infiles", nargs=-1, required=True)
# @click.argument("outfile", nargs=1, required=True)
# def generate_gpkg(infiles, outfile):
#     """Generate GeoPackage from PLATEAU GeoJSON."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     generators.utils.geojson_to_gpkg(expanded_infiles, outfile)

# @cli.command("generate-heightmap")
# @click.argument("infiles", nargs=-1)
# @click.argument("outfile", nargs=1, required=True)
# def generate_heightmap(infiles, outfile):
#     """Generate GeoTIFF heightmap from PLATEAU CityGML."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     generators.triangles_from_gml(expanded_infiles)


# @cli.command("extract-properties")
# @click.argument("infiles", nargs=-1, required=True)
# @click.argument("outfile", nargs=1, required=True)
# def extract_properties(infiles, outfile):
#     """Extract properties from PLATEAU CityGML."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     run_async(extractors.commands.extract_properties(expanded_infiles, outfile))


@cli.command("config")
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


@cli.command("info")
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
        console.print(f"[b]Installed Files:[/b]\n  (None)")
        return

    console.print(f"[b]Installed Files:[/b]")
    for format, path in record.items():
        console.print(f"  {format}: {path}")

    dataset = CityGMLDataset(dataset_id)
    udx_dirs = dataset.udx_dirs()

    console.print(f"[b]Data Types:[/b]")
    for udx_type, path in udx_dirs.items():
        type_name = constants.data_type_display_names.get(udx_type, {}).get(
            "ja", udx_type
        )
        console.print(f"  {type_name} ({udx_type}): {path}")

    console.print(f"[b]Attributes:[/b]")

    with console.status("[bold]Processing...", spinner="simpleDotsScrolling") as status:
        for udx_type in udx_dirs.keys():
            type_name = constants.data_type_display_names.get(udx_type, {}).get(
                "ja", udx_type
            )
            console.print(f"  [b]{type_name} ({udx_type}):[/b]")
            for attr in dataset.scan_attributes(udx_type):
                console.print(f"    {attr.get('name')} ({attr['tag']})")


if __name__ == "__main__":
    cli()
