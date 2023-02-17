import glob
import json
from collections import defaultdict
from pathlib import Path

import click
from prettytable import PrettyTable
from pydantic import BaseModel, PrivateAttr
from tortoise import run_async
from xdg import (
    xdg_cache_home,
    xdg_config_dirs,
    xdg_config_home,
    xdg_data_dirs,
    xdg_data_home,
    xdg_runtime_dir,
    xdg_state_home,
)

# print(xdg_config_home(), xdg_data_home())

from plateaukit import extractors, generators


class Config(BaseModel):
    _path: str = PrivateAttr()
    data = defaultdict(dict)

    def __init__(self, path=None):
        # Set path
        if path is None:
            config_dir = Path(xdg_config_home(), "plateaukit")
            if not config_dir.exists():
                config_dir.mkdir(parents=True)
            path = Path(config_dir, "config.json")
        self._path = str(Path(path).resolve())
        # Load on init
        with open(self._path, "r") as f:
            data = json.load(f)
        super().__init__(**data)

    def save(self):
        with open(self._path, "w") as f:
            data = self.json(indent=2, ensure_ascii=False)
            print(data)
            f.write(data)


def setup_property_db(infiles, db_filename):
    expanded_infiles = []
    for infile in infiles:
        expanded_infiles.extend(glob.glob(infile))
    run_async(extractors.commands.extract_properties(expanded_infiles, db_filename))


@click.group()
def cli():
    pass


# @cli.command("config")

# TODO: Uninstall


@cli.command("install")
@click.argument("dataset_id", nargs=1, required=False)
@click.option(
    "--format",
    type=click.Choice(["citygml", "3dtiles"], case_sensitive=False),
    default="citygml",
)
@click.option("--local", help="Install local file. (without copying)")
@click.option("--download-only", is_flag=True, default=False)
@click.option("-l", "--list", is_flag=True, help="List all available datasets.")
def install(dataset_id, format, local, download_only, list):
    """Download and install PLATEAU datasets."""
    from plateaukit.download import city_list

    if not dataset_id and not list:
        raise Exception("Missing argument")

    if list:
        table = PrettyTable()
        table.field_names = ["id", "name", "homepage"]
        table.add_row(["all", "(全都市)", ""])
        for city in city_list:
            table.add_row([city["dataset_id"], city["city_name"], city["homepage"]])
        print(table)
        return

    if dataset_id:
        city = next(filter(lambda x: x["dataset_id"] == dataset_id, city_list), None)

        if not city:
            raise Exception("Invalid dataset name")

        if local:
            local = Path(local).resolve()
            if not local.exists():
                raise Exception("Local file not found")
            # print(local)
            config = Config()
            config.data[dataset_id][format] = local
            config.save()
            return
        else:
            resource_id = city[format]
            print(dataset_id, resource_id)
            pass
            # download.downloader.download_resource(resource_id)


@cli.command("list")
def cmd_list():
    """List installed PLATEAU datasets."""
    from plateaukit.download import city_list

    config = Config()

    table = PrettyTable()
    table.field_names = ["id", "name", "homepage", "formats"]
    for dataset_id, record in config.data.items():
        city = next(filter(lambda x: x["dataset_id"] == dataset_id, city_list), None)
        if not city:
            continue
        table.add_row(
            [
                dataset_id,
                city["city_name"],
                city["homepage"],
                " ".join([x for x in ["citygml", "3dtiles"] if x in record]),
            ]
        )
    print(table)
    return


@cli.command("generate-cityjson")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
# @click.option("--dataset")
# @click.option("--split", default=10)
# # @click.option(
# #     "--precision",
# #     help="Number of decimal places to keep for geometry vertices (default: 16).",
# )
def generate_cityjson(infiles, outfile):
    """Generate CityJSON from PLATEAU CityGML."""
    # print(files)

    params = {}

    # if precision:
    #     params["precision"] = precision

    data = generators.simplecityjson.cityjson_from_gml(infiles, **params)
    with open(outfile, "w") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


@cli.command("generate-geojson")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
@click.option("--dataset")
@click.option(
    "--type",
    "-t",
    type=click.Choice(
        ["bldg", "brid", "dem", "fld", "frn", "lsld", "luse", "tran", "urf"],
        case_sensitive=True,
    ),
)
@click.option("--split", default=10)
def generate_geojson(infiles, outfile, dataset, type, split):
    """Generate GeoJSON from PLATEAU CityGML."""
    if not infiles and not dataset:
        raise Exception("Missing argument")

    if infiles and dataset:
        raise Exception("Too many argument")

    if dataset:
        if not type:
            raise Exception("Missing type")
        config = Config()
        record = config.data[dataset]
        if "citygml" not in record:
            raise Exception("Missing CityGML data")
        infiles = [str(Path(record["citygml"], "udx", type, "*.gml"))]
        print(infiles, outfile)

    expanded_infiles = []
    for infile in infiles:
        expanded_infiles.extend(glob.glob(infile))

    if type == "bldg":
        generators.geojson_from_gml(
            expanded_infiles,
            outfile,
            split=split,
            lod=[0],
            altitude=True,
            allow_geometry_collection=False,
        )
    elif type == "brid":
        generators.geojson_from_gml(
            expanded_infiles,
            outfile,
            split=split,
            lod=[1],
            attributes=[],
            altitude=True,
            allow_geometry_collection=True,
        )
    elif type == "dem":
        # TODO: implement
        raise NotImplementedError("dem")
    elif type == "fld":
        raise NotImplementedError("fld")
    elif type == "lsld":
        raise NotImplementedError("lsld")
    elif type == "luse":
        raise NotImplementedError("luse")
        # generate.geojson_from_gml(
        #     expanded_infiles,
        #     outfile,
        #     split=split,
        #     lod=[1],
        #     attributes=[],
        #     altitude=True,
        #     allow_geometry_collection=True,
        # )
    elif type == "tran":
        generators.geojson_from_gml(
            expanded_infiles,
            outfile,
            split=split,
            lod=[1],
            attributes=[],
            altitude=True,  # TODO: can be False
            allow_geometry_collection=True,
        )
    elif type == "urf":
        raise NotImplementedError("urf")
        # generate.geojson_from_gml(
        #     expanded_infiles,
        #     outfile,
        #     split=split,
        #     lod=[0],
        #     attributes=[],
        #     altitude=True,
        #     allow_geometry_collection=False,
        # )
    else:
        raise NotImplementedError(type)


# @cli.command("generate-gpkg")
# @click.argument("infiles", nargs=-1, required=True)
# @click.argument("outfile", nargs=1, required=True)
# def generate_gpkg(infiles, outfile):
#     """Generate GeoPackage from PLATEAU GeoJSON."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     generators.utils.geojson_to_gpkg(expanded_infiles, outfile)


@cli.command("generate-qmesh")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
def generate_qmesh(infiles, outfile):
    """Generate Quantified Mesh from PLATEAU CityGML."""
    generators.triangles_from_gml(infiles)


# @cli.command("generate-heightmap")
# @click.argument("infiles", nargs=-1)
# @click.argument("outfile", nargs=1, required=True)
# def generate_heightmap(infiles, outfile):
#     """Generate GeoTIFF heightmap from PLATEAU CityGML."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     generators.triangles_from_gml(expanded_infiles)


@cli.command("extract-properties")
@click.argument("infiles", nargs=-1, required=True)
@click.argument("outfile", nargs=1, required=True)
def extract_properties(infiles, outfile):
    """Extract properties from PLATEAU CityGML."""
    expanded_infiles = []
    for infile in infiles:
        expanded_infiles.extend(glob.glob(infile))
    run_async(extractors.commands.extract_properties(expanded_infiles, outfile))


# @cli.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo(f"Hello {name}!")

if __name__ == "__main__":
    cli()
