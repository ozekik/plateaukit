import glob
import tempfile
from pathlib import Path
from typing import Literal

import geopandas as gpd
import pandas as pd
from rich import get_console

from plateaukit.config import Config
from plateaukit.core.dataset import load_dataset
from plateaukit.logger import logger

_supported_types = ["bldg", "brid", "tran"]
# _supported_types = ["bldg", "tran"]


def prebuild(
    dataset_id: str,
    *,
    split: int = 10,
    simple_output=False,
    format: Literal["gpkg", "parquet"] = "parquet",
    types=["bldg"],
) -> None:
    """Prebuild a PLATEAU dataset for PlateauKit."""

    try:
        from pyogrio import read_dataframe, write_dataframe
    except ImportError:
        raise ImportError(
            "Package `pyogrio` is required for prebuild. Please install it using `pip install pyogrio`."
        ) from None

    console = get_console()

    if not dataset_id:
        raise Exception("Missing argument: dataset_id")

    config = Config()
    # record = config.datasets.get(dataset_id)
    # print(dataset_id, record)

    # Check if all types are supported
    if not set(types).issubset(set(_supported_types)):
        raise ValueError(f"Unsupported types: {set(types) - set(_supported_types)}")

    with tempfile.TemporaryDirectory() as tdir:
        logger.debug(f"Temporary directory: {tdir}")

        for type in types:
            outfile_geojsonl = Path(tdir, f"{dataset_id}.{type}.geojsonl")

            dataset = load_dataset(dataset_id)
            dataset.to_geojson(
                outfile_geojsonl,
                types=[type],
                altitude=False,  # TODO: Check this
                include_type=True,
                seq=True,
                split=split,
                progress={"description": f"Generating GeoJSONSeq files: {type}"},
                simple_output=simple_output,
            )

        if format == "parquet":
            display_name = "Parquet files"
        elif format == "gpkg":
            display_name = "GeoPackage files"
        else:
            raise ValueError(f"Invalid format: {format}")

        with console.status(f"Writing {display_name}...") as status:
            if format == "gpkg":
                if types != ["bldg"]:
                    raise NotImplementedError(
                        "GeoPackage mode supports `bldg` type only."
                    )

                df = gpd.GeoDataFrame()

                for filename in glob.glob(str(Path(tdir, "*.geojsonl"))):
                    # Filter by type
                    subdf = read_dataframe(filename)
                    # NOTE: Setting ignore_index True for re-indexing
                    df = pd.concat([df, subdf], ignore_index=True)

                # TODO: Use more accurate CRS
                mercator = df.to_crs(3857)
                centroid_mercator = mercator.centroid
                centroid = centroid_mercator.to_crs(4326)

                df["longitude"] = centroid.x
                df["latitude"] = centroid.y

                dest_path = Path(config.data_dir, f"{dataset_id}.gpkg")
                write_dataframe(df, dest_path, driver="GPKG")

                config.datasets[dataset_id]["gpkg"] = dest_path
                config.save()

            elif format == "parquet":
                dest_path_map = {}

                for type in types:
                    tmp_file_paths = []

                    for filename in glob.glob(str(Path(tdir, "*.geojsonl"))):
                        # Filter by type
                        if f".{type}." not in filename:
                            continue

                        try:
                            df = gpd.read_file(filename)
                        except Exception:
                            raise RuntimeError(f"Failed to read {filename}")
                            # import shutil

                            # # copy dir to /tmp for debugging:
                            # shutil.copytree(tdir, "/tmp/failed")
                            # raise

                        # TODO: Use more accurate CRS
                        mercator = df.to_crs(3857)
                        centroid_mercator = mercator.centroid
                        centroid = centroid_mercator.to_crs(4326)

                        df["longitude"] = centroid.x
                        df["latitude"] = centroid.y

                        tmp_dest_path = str(Path(tdir, f"{filename}.parquet"))
                        df.to_parquet(tmp_dest_path, index=False)

                        tmp_file_paths.append(tmp_dest_path)

                    df = None
                    for filename in tmp_file_paths:
                        subdf = gpd.read_parquet(filename)
                        # NOTE: set ignore_index True for re-indexing
                        df = (
                            pd.concat([df, subdf], ignore_index=True)
                            if df is not None
                            else subdf
                        )

                    if df is None:
                        raise RuntimeError("Data is empty")

                    # NOTE: For backward compatibility
                    if type == "bldg":
                        dest_filename = f"{dataset_id}.parquet"
                    else:
                        dest_filename = f"{dataset_id}.{type}.parquet"

                    dest_path = Path(config.data_dir, dest_filename)
                    df.to_parquet(dest_path, compression="zstd")

                    dest_path_map[type] = dest_path

                config.datasets[dataset_id]["parquet"] = dest_path_map
                config.save()

        console.print(f"Writing {display_name}... [green]Done")

        # click.echo(f"\nCreated: {dest_path}")
