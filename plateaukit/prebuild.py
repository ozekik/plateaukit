import glob
import tempfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
from rich import get_console

from plateaukit.config import Config
from plateaukit.core.dataset import load_dataset


def prebuild(dataset_id: str, *, split: int = 10, simple_output=False) -> None:
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
        for type in types:
            outfile = Path(tdir, f"{dataset_id}.{type}.geojson")

            if dataset_id:
                dataset = load_dataset(dataset_id)
                dataset.to_geojson(
                    outfile,
                    types=types,
                    altitude=False,  # TODO: Check this
                    include_type=True,
                    split=split,
                    progress={"description": "Generating GeoJSON files..."},
                    simple_output=simple_output,
                )
            else:
                raise NotImplementedError()
                # generators.geojson.geojson_from_citygml(
                #     infiles,
                #     outfile,
                #     dataset_id,
                #     types=types,
                #     split=split,
                #     progress={"description": "Generating GeoJSON files..."},
                # )

        with console.status("Writing GeoPackage...") as status:
            df = gpd.GeoDataFrame()

            for filename in glob.glob(str(Path(tdir, "*.geojson"))):
                subdf = read_dataframe(filename)
                df = pd.concat([df, subdf])

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

        console.print("Writing GeoPackage... [green]Done")

        # click.echo(f"\nCreated: {dest_path}")
