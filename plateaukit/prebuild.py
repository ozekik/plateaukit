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


def prebuild(
    dataset_id: str,
    *,
    split: int = 10,
    simple_output=False,
    format: Literal["gpkg", "parquet"] = "parquet",
) -> None:
    """Prebuild PLATEAU datasets."""

    try:
        from pyogrio import read_dataframe, write_dataframe
    except ImportError:
        raise ImportError(
            "Package pyogrio is required. Please install it using `pip install pyogrio`."
        ) from None

    console = get_console()

    if not dataset_id:
        raise Exception("Missing argument: dataset_id")

    config = Config()
    record = config.datasets.get(dataset_id)
    # print(dataset_id, record)

    # TODO: All types
    types = ["bldg"]

    with tempfile.TemporaryDirectory() as tdir:
        logger.debug(f"Temporary directory: {tdir}")

        for type in types:
            outfile = Path(tdir, f"{dataset_id}.{type}.geojsonl")

            if dataset_id:
                dataset = load_dataset(dataset_id)
                dataset.to_geojson(
                    outfile,
                    types=types,
                    altitude=False,  # TODO: Check this
                    include_type=True,
                    seq=True,
                    split=split,
                    progress={"description": "Generating GeoJSONSeq files..."},
                    simple_output=simple_output,
                )
            else:
                raise NotImplementedError()

        if format == "parquet":
            display_name = "Parquet files"
        elif format == "gpkg":
            display_name = "GeoPackage files"
        else:
            raise NotImplementedError()

        with console.status(f"Writing {display_name}...") as status:
            if format == "gpkg":
                df = gpd.GeoDataFrame()

                for filename in glob.glob(str(Path(tdir, "*.geojsonl"))):
                    subdf = read_dataframe(filename)
                    # NOTE: set ignore_index True for re-indexing
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
                tmp_file_paths = []

                for filename in glob.glob(str(Path(tdir, "*.geojsonl"))):
                    df = gpd.read_file(filename)

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
                    raise RuntimeError

                dest_path = Path(config.data_dir, f"{dataset_id}.parquet")
                df.to_parquet(dest_path, compression="zstd")

                config.datasets[dataset_id]["parquet"] = dest_path
                config.save()

            else:
                raise NotImplementedError()

        console.print(f"Writing {display_name}... [green]Done")

        # click.echo(f"\nCreated: {dest_path}")
