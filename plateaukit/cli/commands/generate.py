from __future__ import annotations

import click

from plateaukit import generators
from plateaukit.core.dataset import load_dataset


@click.command("generate-cityjson")
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
@click.option("--seq", is_flag=True, default=False, help="Generate CityJSONSeq")
@click.option(
    "--target-epsg", default=None, help="EPSG code for the output CityJSON file"
)
# # @click.option(
# #     "--precision",
# #     help="Number of decimal places to keep for geometry vertices (default: 16).",
# )
def generate_cityjson_cmd(
    infiles, outfile, dataset_id, types, split, ground, seq, target_epsg
):
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
            seq=seq,
            ground=ground,
            target_epsg=target_epsg,
            **params,
        )

    else:
        generators.cityjson.cityjson_from_citygml(infiles, outfile, **params)


def _generate_geojson(
    infiles, outfile, dataset_id: str, types: list[str], seq: bool, split: int, **kwargs
):
    """Generate GeoJSON from PLATEAU datasets."""

    if not infiles and not dataset_id:
        raise click.UsageError("Missing argument: infiles or dataset")

    if infiles and dataset_id:
        raise click.UsageError("Too many arguments")

    if dataset_id:
        dataset = load_dataset(dataset_id)
        dataset.to_geojson(outfile, types=types, seq=seq, split=split, **kwargs)
    else:
        generators.geojson.geojson_from_citygml(
            infiles, outfile, types=types, seq=seq, split=split, **kwargs
        )


@click.command("generate-geojson")
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
@click.option("--seq", is_flag=True, default=False, help="Generate GeoJSONSeq")
@click.option("--split", default=1)
def generate_geojson_cmd(
    infiles, outfile, dataset_id: str, types: list[str], seq: bool, split: int
):
    """Generate GeoJSON from PLATEAU datasets.

    PLATEAU データセットから GeoJSON を生成します。
    """

    _generate_geojson(infiles, outfile, dataset_id, types=types, seq=seq, split=split)


@click.command("generate-qmesh")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
def generate_qmesh_cmd(infiles, outfile):
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
