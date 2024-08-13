from __future__ import annotations

import click

from plateaukit import exporters
from plateaukit.cli.base import cli
from plateaukit.core.dataset import load_dataset
from plateaukit.exporters.cityjson.parallel_writer import ParallelWriter
from plateaukit.exporters.cityjson.writer import CityJSONWriter
from plateaukit.logger import set_log_level
from plateaukit.readers.citygml.reader import CityGMLReader
from plateaukit.transformers.filter_lod import LODFilteringTransformer
from plateaukit.transformers.reprojection import ReprojectionTransformer


@cli.command(name="export-cityjson", aliases=["generate-cityjson"])
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
    "--lod-mode",
    "lod_mode",
    type=click.Choice(["highest", "all"], case_sensitive=True),
    default="highest",
    help="LOD filtering mode: 'highest' (default), 'all'",
)
@click.option("--seq", is_flag=True, default=False, help="Export CityJSONSeq")
@click.option(
    "--target-epsg", default=None, help="EPSG code for the output CityJSON file"
)
# # @click.option(
# #     "--precision",
# #     help="Number of decimal places to keep for geometry vertices (default: 16).",
# )
def export_cityjson_cmd(
    infiles,
    outfile,
    dataset_id,
    types,
    split,
    ground,
    lod_mode,
    seq,
    target_epsg,
):
    """Export CityJSON from PLATEAU datasets.

    PLATEAU データセットから CityJSON を出力します。
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

    if dataset_id:
        dataset = load_dataset(dataset_id)
        dataset.to_cityjson(
            outfile,
            types=types,
            split=split,
            seq=seq,
            lod_mode=lod_mode,
            ground=ground,
            target_epsg=target_epsg,
            **params,
        )

    else:
        reader = CityGMLReader()
        readable = reader.scan_files(
            infiles,
            codelist_infiles=None,
            # codelist_infiles=codelist_infiles, # TODO: Fix this
            # zipfile=file_path,  # TODO: Fix this
        )

        # transformers = [LODFilteringTransformer(mode=lod_mode)]

        # TODO: Fix typing
        transformers: list = [
            LODFilteringTransformer(mode=lod_mode),
        ]

        if target_epsg:
            transformers.append(ReprojectionTransformer(target_epsg=target_epsg))

        for transformer in transformers:
            readable = transformer.transform(readable)

        parallel_writer = ParallelWriter(CityJSONWriter)
        parallel_writer.transform(readable, str(outfile), seq=seq, split=split)

        # NOTE: Old implementation
        # exporters.cityjson.cityjson_from_citygml(
        #     infiles,
        #     outfile,
        #     split=split,
        #     seq=seq,
        #     use_highest_lod=use_highest_lod,
        #     ground=ground,
        #     target_epsg=target_epsg,
        #     **params,
        # )


def _export_geojson(
    infiles, outfile, dataset_id: str, types: list[str], seq: bool, split: int, **kwargs
):
    """Export GeoJSON from PLATEAU datasets."""

    if not infiles and not dataset_id:
        raise click.UsageError("Missing argument: infiles or dataset")

    if infiles and dataset_id:
        raise click.UsageError("Too many arguments")

    if dataset_id:
        dataset = load_dataset(dataset_id)
        dataset.to_geojson(outfile, types=types, seq=seq, split=split, **kwargs)
    else:
        exporters.geojson.geojson_from_citygml(
            infiles, outfile, types=types, seq=seq, split=split, **kwargs
        )


# @click.command("generate-geojson")
@cli.command(name="export-geojson", aliases=["generate-geojson"])
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
@click.option("--seq", is_flag=True, default=False, help="Export GeoJSONSeq")
@click.option("--split", default=1)
@click.option("-v", "verbose", count=True, default=0, help="Verbose")
def export_geojson_cmd(
    infiles,
    outfile,
    dataset_id: str,
    types: list[str],
    seq: bool,
    split: int,
    verbose: int,
):
    """Export GeoJSON from PLATEAU datasets.

    PLATEAU データセットから GeoJSON を出力します。
    """

    if verbose >= 2:
        set_log_level("DEBUG")

    _export_geojson(infiles, outfile, dataset_id, types=types, seq=seq, split=split)


@click.command("export-qmesh")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
def export_qmesh_cmd(infiles, outfile):
    """Export Quantized Mesh from PLATEAU datasets. (Requires `pip install 'plateaukit[quantized_mesh]'`)

    PLATEAU データセットから Quantized Mesh を出力します。(要 `pip install 'plateaukit[quantized_mesh]'`)
    """
    raise NotImplementedError()

    # exporters.triangles_from_gml(infiles)


# @cli.command("generate-gpkg")
# @click.argument("infiles", nargs=-1, required=True)
# @click.argument("outfile", nargs=1, required=True)
# def generate_gpkg(infiles, outfile):
#     """Generate GeoPackage from PLATEAU GeoJSON."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     exporters.utils.geojson_to_gpkg(expanded_infiles, outfile)


# @cli.command("generate-heightmap")
# @click.argument("infiles", nargs=-1)
# @click.argument("outfile", nargs=1, required=True)
# def generate_heightmap(infiles, outfile):
#     """Generate GeoTIFF heightmap from PLATEAU CityGML."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     exporters.triangles_from_gml(expanded_infiles)


# @cli.command("extract-properties")
# @click.argument("infiles", nargs=-1, required=True)
# @click.argument("outfile", nargs=1, required=True)
# def extract_properties(infiles, outfile):
#     """Extract properties from PLATEAU CityGML."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     run_async(extractors.commands.extract_properties(expanded_infiles, outfile))
