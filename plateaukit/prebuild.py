import glob
import tempfile
from pathlib import Path

from rich import get_console

from plateaukit.config import Config
from plateaukit.dataset import load_dataset


def prebuild(dataset_id: str) -> None:
    """Prebuild PLATEAU datasets."""

    import geopandas as gpd
    import pandas as pd
    from pyogrio import read_dataframe, write_dataframe

    console = get_console()

    if not dataset_id:
        raise Exception("Missing argument: dataset_id")

    config = Config()
    record = config.datasets.get(dataset_id)
    # print(dataset_id, record)

    # TODO: All types
    types = ["bldg"]
    split = 10

    with tempfile.TemporaryDirectory() as tdir:
        for type in types:
            outfile = Path(tdir, f"{dataset_id}.{type}.geojson")

            if dataset_id:
                dataset = load_dataset(dataset_id)
                dataset.to_geojson(
                    outfile,
                    types=types,
                    split=split,
                    progress={"description": "Generating GeoJSON files..."},
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

            dest_path = Path(config.data_dir, f"{dataset_id}.gpkg")
            write_dataframe(df, dest_path, driver="GPKG")

            config.datasets[dataset_id]["gpkg"] = dest_path
            config.save()

        console.print("Writing GeoPackage... [green]Done")

        # click.echo(f"\nCreated: {dest_path}")